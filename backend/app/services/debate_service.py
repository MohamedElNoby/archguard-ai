import json
import logging
import os
import time
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)


def _generate_dynamic_debate_fallback(primary_risk: Dict[str, Any]) -> Dict[str, Any]:
    risk_title = primary_risk.get("title", "Single Point of Failure")
    risk_desc = primary_risk.get("description", "Identified architectural vulnerability.")
    risk_level = primary_risk.get("level", "CRITICAL")

    return {
        "primary_risk": primary_risk,
        "agents": {
            "CyberSec": {
                "agent": "CyberSec",
                "risk_level": risk_level,
                "security_impact": (
                    f"A failure or compromise in '{risk_title}' exposes the architecture boundary to denial-of-service, "
                    "eavesdropping on unsegmented traffic, and localized isolation of downstream subnets."
                ),
                "attack_scenarios": [
                    f"Targeted L2/L3 denial of service directly against {risk_title}.",
                    "Ad-hoc network disruption preventing authentication and security synchronization."
                ],
                "mitigations": [
                    "Deploy edge ingress filtering and segment local node subnets.",
                    "Enforce authenticated mutual handshake between edge nodes and gateway routers."
                ],
            },
            "SRE": {
                "agent": "SRE",
                "risk_level": risk_level,
                "reliability_impact": (
                    f"Operating without active redundancy for '{risk_title}' causes complete service disruption. "
                    "Uplink sync, ingest queues, and node discovery stall immediately upon hardware or link faults."
                ),
                "failure_scenarios": [
                    f"Single interface saturation on {risk_title} stalling asynchronous packet delivery.",
                    "Network partition isolating local processing nodes from core components."
                ],
                "mitigations": [
                    "Implement CARP/VRRP gateway clustering or multi-path mesh routing.",
                    "Introduce local persistent buffering on edge nodes during uplink disconnects."
                ],
            },
            "FinOps": {
                "agent": "FinOps",
                "risk_level": "MEDIUM",
                "cost_impact": (
                    f"Unplanned outages at '{risk_title}' result in operational downtime and manual maintenance overhead. "
                    "Unthrottled retry storms after link restoration will cause bandwidth billing spikes."
                ),
                "cost_scenarios": [
                    "Repeated unbuffered retries consuming metered uplink bandwidth.",
                    "Emergency technician dispatches due to lack of remote out-of-band management."
                ],
                "mitigations": [
                    "Leverage cost-effective dual consumer-grade edge nodes with automated failover.",
                    "Enforce rate-limiting and exponential backoff on reconnect."
                ],
            },
        },
        "debate": {
            "primary_risk": primary_risk,
            "agent_positions": [
                {"agent": "CyberSec", "position": f"Boundary exposure and isolation attack vectors on {risk_title}."},
                {"agent": "SRE", "position": f"Availability zero-point without multi-link or dual-router redundancy."},
                {"agent": "FinOps", "position": "High operational recovery overhead and unmetered sync surge."}
            ],
            "agreements": [
                f"All agents agree that '{risk_title}' must not remain an unmitigated single point of failure."
            ],
            "differences": [
                "SRE demands instant dual-hardware failover; FinOps prioritizes edge-node local caching to minimize costs."
            ],
            "final_consensus": (
                f"Mitigate '{risk_title}' using multi-path gossip synchronization and a secondary fallback gateway."
            ),
            "recommended_actions": [
                "Implement gateway failover protocol (e.g. VRRP).",
                "Deploy store-and-forward local queues on edge endpoints."
            ],
        },
    }


def run_multi_agent_debate(
    architecture_data: Dict[str, Any], primary_risk: Dict[str, Any]
) -> Dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.warning("GEMINI_API_KEY not found. Generating dynamic fallback debate.")
        return _generate_dynamic_debate_fallback(primary_risk)

    risk_title = primary_risk.get("title", "Single Point of Failure")
    risk_desc = primary_risk.get("description", "")

    prompt = f"""
You are an orchestrator of an adversarial Software & Infrastructure Architecture Review Jury.
Conduct an intense Multi-Agent debate analyzing this SPECIFIC system and the detected primary risk.

Detected Primary Risk:
- Title: {risk_title}
- Details: {risk_desc}
- Level: {primary_risk.get("level", "HIGH")}

Architecture Context:
{json.dumps(architecture_data, indent=2)}

CRITICAL INSTRUCTIONS:
- Ground the debate EXCLUSIVELY on the entities present in the primary risk (e.g., Routers, Mesh networks, Edge nodes, Gateways, Queues, etc.).
- DO NOT invent generic eCommerce microservices (Order, Payment, Cart) unless they are explicitly in the risk details.
- Provide concrete, technical arguments for each specialist agent.

Return ONLY a valid JSON object matching this EXACT structure:
{{
  "primary_risk": {json.dumps(primary_risk)},
  "agents": {{
    "CyberSec": {{
      "agent": "CyberSec",
      "risk_level": "CRITICAL",
      "security_impact": "string",
      "attack_scenarios": ["scenario 1", "scenario 2"],
      "mitigations": ["mitigation 1", "mitigation 2"]
    }},
    "SRE": {{
      "agent": "SRE",
      "risk_level": "CRITICAL",
      "reliability_impact": "string",
      "failure_scenarios": ["scenario 1", "scenario 2"],
      "mitigations": ["mitigation 1", "mitigation 2"]
    }},
    "FinOps": {{
      "agent": "FinOps",
      "risk_level": "HIGH",
      "cost_impact": "string",
      "cost_scenarios": ["scenario 1"],
      "mitigations": ["mitigation 1"]
    }}
  }},
  "debate": {{
    "primary_risk": {json.dumps(primary_risk)},
    "agent_positions": [
      {{"agent": "CyberSec", "position": "string"}},
      {{"agent": "SRE", "position": "string"}},
      {{"agent": "FinOps", "position": "string"}}
    ],
    "agreements": ["string"],
    "differences": ["string"],
    "final_consensus": "string",
    "recommended_actions": ["string", "string"]
  }}
}}
"""

    candidate_models = ["gemini-2.5-flash", "gemini-1.5-flash"]
    client = genai.Client(api_key=api_key)

    for model_name in candidate_models:
        for attempt in range(2):
            try:
                logger.info(f"Calling Gemini ({model_name}) for live debate (Attempt {attempt + 1})...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.2,
                    ),
                )
                result = json.loads(response.text)
                result["primary_risk"] = primary_risk
                return result

            except Exception as e:
                logger.warning(f"Debate attempt {attempt + 1} with {model_name} failed: {e}")
                time.sleep(1.2)

    logger.error("All live LLM attempts failed. Generating dynamic context-aware debate.")
    return _generate_dynamic_debate_fallback(primary_risk)