import os
import json
import re
import asyncio
import PIL.Image
import google.generativeai as genai

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.architecture import ArchitectureSpec
from app.models.risk import RiskAssessment
from app.models.project import Project
from app.crud.debate import create_or_update_debate_report, get_debate_report_by_project_id
from app.schemas.debate import DebateReportCreate, DebateReportRead
from app.services.debate_service import run_multi_agent_debate

router = APIRouter(prefix="/projects", tags=["Multi-Agent Debate"])


def _extract_json_block(text: str) -> dict:
    """Safely extracts JSON even if markdown wrapping or leading/trailing text exists."""
    text = text.strip()
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    return json.loads(text)


def _resolve_primary_risk_and_arch(project_id: str, db: Session):
    """Helper to extract or infer the primary risk and architecture components."""
    arch = db.query(ArchitectureSpec).filter(ArchitectureSpec.project_id == project_id).first()
    risk_record = db.query(RiskAssessment).filter(RiskAssessment.project_id == project_id).first()

    if risk_record and risk_record.risks:
        top_risk = risk_record.risks[0]
        primary_risk = {
            "level": top_risk.get("severity", "CRITICAL"),
            "title": top_risk.get("title", "Primary Architecture Risk"),
            "description": top_risk.get("description", "")
        }
        architecture_data = {
            "components": arch.components if arch else [],
            "routes": arch.routes if arch else []
        }
        return primary_risk, architecture_data

    # Fallback to direct Gemini Vision analysis if not in DB
    project_record = db.query(Project).filter(Project.id == project_id).first()
    if not project_record or not project_record.diagram_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project or diagram path not found for project '{project_id}'"
        )

    raw_path = project_record.diagram_path
    image_path = raw_path if os.path.isabs(raw_path) else os.path.join(os.getcwd(), raw_path)

    if not os.path.exists(image_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Diagram image file does not exist on disk at '{image_path}'"
        )

    try:
        with PIL.Image.open(image_path) as img:
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = """
            Analyze this system architecture diagram. Identify the SINGLE most critical architectural risk (e.g., SPOF, bottleneck, security flaw, scaling issue).
            Return ONLY a valid JSON string with this exact structure, do not add markdown formatting or conversational filler:
            {
                "level": "CRITICAL",
                "title": "Short Risk Title Here",
                "description": "Detailed explanation based on visual components."
            }
            """
            response = model.generate_content([prompt, img])
            primary_risk = _extract_json_block(response.text)
            architecture_data = {
                "components": ["Auto-detected components via Vision"],
                "routes": []
            }
    except Exception as e:
        primary_risk = {
            "level": "CRITICAL",
            "title": "Single Point of Failure and Bottleneck Vulnerabilities",
            "description": f"Fallback risk analysis generated. Root cause: {str(e)}"
        }
        architecture_data = {
            "components": ["Gateway", "Service Core", "Database"],
            "routes": []
        }

    return primary_risk, architecture_data


@router.post(
    "/{project_id}/debate",
    response_model=DebateReportRead,
    summary="Trigger and persist Multi-Agent Debate"
)
def trigger_debate(project_id: str, db: Session = Depends(get_db)):
    primary_risk, architecture_data = _resolve_primary_risk_and_arch(project_id, db)

    # Execute multi-agent debate session
    debate_result = run_multi_agent_debate(
        architecture_data=architecture_data,
        primary_risk=primary_risk
    )

    # Construct payload and persist the debate report
    payload = DebateReportCreate(
        primary_risk=debate_result.get("primary_risk", primary_risk),
        agents=debate_result.get("agents", {}),
        debate_summary=debate_result.get("debate", {})
    )

    saved_report = create_or_update_debate_report(
        db=db, project_id=project_id, payload=payload
    )

    return saved_report


@router.get(
    "/{project_id}/debate/stream",
    summary="Stream Multi-Agent Debate in real-time via Server-Sent Events (SSE)"
)
async def stream_debate(project_id: str, db: Session = Depends(get_db)):
    primary_risk, architecture_data = _resolve_primary_risk_and_arch(project_id, db)

    async def event_generator():
        # 1. إرسال الخطر الأساسي فوراً
        yield f"event: risk\ndata: {json.dumps(primary_risk)}\n\n"
        await asyncio.sleep(0.4)

        # 2. تشغيل المناظرة في thread منفصل لتجنب حظر مسار async
        loop = asyncio.get_running_loop()
        debate_result = await loop.run_in_executor(
            None, run_multi_agent_debate, architecture_data, primary_risk
        )

        # 3. حفظ النتيجة في قاعدة البيانات
        payload = DebateReportCreate(
            primary_risk=debate_result.get("primary_risk", primary_risk),
            agents=debate_result.get("agents", {}),
            debate_summary=debate_result.get("debate", {})
        )
        create_or_update_debate_report(db=db, project_id=project_id, payload=payload)

        # 4. بث رسائل الوكلاء تتابعياً بفارق زمني لمحاكاة المناظرة الحية
        agents_data = debate_result.get("agents", {})
        agent_order = ["cybersec", "sre", "finops"]

        for agent_key in agent_order:
            agent_payload = agents_data.get(agent_key)
            if agent_payload:
                formatted_message = {
                    "agent": agent_payload.get("agent", agent_key.capitalize()),
                    "message": (
                        agent_payload.get("security_impact")
                        or agent_payload.get("reliability_impact")
                        or agent_payload.get("cost_impact")
                        or agent_payload.get("message", "")
                    ),
                    "timestamp": "now"
                }
                yield f"event: agent_message\ndata: {json.dumps(formatted_message)}\n\n"
                await asyncio.sleep(1.2)

        # 5. إشعار اكتمال البث
        yield f"event: complete\ndata: {json.dumps({'status': 'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get(
    "/{project_id}/debate",
    response_model=DebateReportRead,
    summary="Get saved debate report for a project"
)
def get_debate(project_id: str, db: Session = Depends(get_db)):
    report = get_debate_report_by_project_id(db=db, project_id=project_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Debate report not found for project '{project_id}'"
        )
    return report