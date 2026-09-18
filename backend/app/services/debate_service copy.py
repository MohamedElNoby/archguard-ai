import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)

BACKEND_DIR = Path(__file__).resolve().parents[2]
LOCAL_REFERENCE_DIR = BACKEND_DIR / "reference_outputs"


def _find_reference_file(filename: str) -> Path | None:
    local_path = LOCAL_REFERENCE_DIR / filename
    if local_path.is_file():
        return local_path

    cwd_path = Path.cwd() / "reference_outputs" / filename
    if cwd_path.is_file():
        return cwd_path

    return None


def _load_reference_fallback(primary_risk: Dict[str, Any]) -> Dict[str, Any]:
    file_path = _find_reference_file("multi_agent_debate.json")
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON file at {file_path}: {e}")

    return {
        "primary_risk": primary_risk,
        "agents": {
            "CyberSec": {
                "agent": "CyberSec",
                "risk_level": primary_risk.get("level", "HIGH"),
                "security_impact": "Identified DoS and resource cascade risk.",
                "attack_scenarios": ["Cascading denial of service attack."],
                "mitigations": ["Deploy circuit breakers and rate limits."],
            },
            "SRE": {
                "agent": "SRE",
                "risk_level": primary_risk.get("level", "HIGH"),
                "reliability_impact": "Compound availability degradation.",
                "failure_scenarios": ["Downstream service latency storm."],
                "mitigations": ["Decouple services using event-driven async queues."],
            },
            "FinOps": {
                "agent": "FinOps",
                "risk_level": primary_risk.get("level", "HIGH"),
                "cost_impact": "Idle thread compute waste and auto-scaling cost spikes.",
                "cost_scenarios": ["Excessive unbudgeted scaling due to thread blocks."],
                "mitigations": ["Enforce strict concurrency thresholds."],
            },
        },
        "debate": {
            "primary_risk": primary_risk,
            "agent_positions": [
                {"agent": "CyberSec", "position": "Critical attack surface vector."},
                {"agent": "SRE", "position": "Cascading availability compound fault."},
                {"agent": "FinOps", "position": "High compute resource expenditure waste."},
            ],
            "agreements": ["All agents agree on immediate async decoupling."],
            "differences": ["CyberSec focuses on attacks, SRE on latency, FinOps on billing."],
            "final_consensus": "Immediate architectural refactor required.",
            "recommended_actions": ["Deploy circuit breakers", "Transition to async messaging"],
        },
    }


def run_multi_agent_debate(
    architecture_data: Dict[str, Any], primary_risk: Dict[str, Any]
) -> Dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.warning("GEMINI_API_KEY not found. Using fallback debate JSON.")
        return _load_reference_fallback(primary_risk)

    prompt = f"""
You are an orchestrator of an adversarial Software Architecture Review Jury.
Conduct an intense Multi-Agent debate analyzing this architecture and primary risk.

Architecture Context:
{json.dumps(architecture_data, indent=2)}

Primary Risk:
{json.dumps(primary_risk, indent=2)}

Task:
Simulate 3 specialized AI agents debating this specific system:
1. CyberSec: Focus on vulnerabilities, authentication bypass, data exposure, DoS vectors.
2. SRE (Site Reliability Engineer): Focus on bottlenecks, cascade failures, latency spikes, single points of failure.
3. FinOps: Focus on unbudgeted compute/storage costs, over-provisioning, redundant egress/calls.

Return ONLY a valid JSON object matching this EXACT structure:
{{
  "primary_risk": {json.dumps(primary_risk)},
  "agents": {{
    "CyberSec": {{
      "agent": "CyberSec",
      "risk_level": "CRITICAL",
      "security_impact": "Detailed security impact statement.",
      "attack_scenarios": ["Attack scenario 1", "Attack scenario 2"],
      "mitigations": ["Mitigation 1", "Mitigation 2"]
    }},
    "SRE": {{
      "agent": "SRE",
      "risk_level": "CRITICAL",
      "reliability_impact": "Detailed reliability impact statement.",
      "failure_scenarios": ["Failure scenario 1", "Failure scenario 2"],
      "mitigations": ["Mitigation 1", "Mitigation 2"]
    }},
    "FinOps": {{
      "agent": "FinOps",
      "risk_level": "HIGH",
      "cost_impact": "Detailed financial impact statement.",
      "cost_scenarios": ["Cost scenario 1"],
      "mitigations": ["Mitigation 1"]
    }}
  }},
  "debate": {{
    "primary_risk": {json.dumps(primary_risk)},
    "agent_positions": [
      {{"agent": "CyberSec", "position": "Concise stance on this system's risk."}},
      {{"agent": "SRE", "position": "Concise stance on this system's risk."}},
      {{"agent": "FinOps", "position": "Concise stance on this system's risk."}}
    ],
    "agreements": ["Key area where all 3 agents agree."],
    "differences": ["Contrasting priorities between the 3 agents."],
    "final_consensus": "Actionable consensus summary for the engineering team.",
    "recommended_actions": ["Action item 1", "Action item 2"]
  }}
}}
"""

    max_retries = 2
    for attempt in range(max_retries):
        try:
            logger.info(f"Calling Gemini for live multi-agent debate (Attempt {attempt + 1})...")
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.3,
                ),
            )
            return json.loads(response.text)

        except Exception as e:
            logger.warning(f"Debate attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            else:
                logger.error("Live Gemini debate failed. Falling back to reference JSON.")
                return _load_reference_fallback(primary_risk)