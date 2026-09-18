from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AgentOutput(BaseModel):
    agent: str
    risk_level: str
    security_impact: Optional[str] = None
    reliability_impact: Optional[str] = None
    cost_impact: Optional[str] = None
    attack_scenarios: Optional[List[str]] = None
    failure_scenarios: Optional[List[str]] = None
    cost_scenarios: Optional[List[str]] = None
    mitigations: List[str]


class AgentPosition(BaseModel):
    agent: str
    position: str


class DebateSummary(BaseModel):
    primary_risk: Dict[str, str]
    agent_positions: List[AgentPosition]
    agreements: List[str]
    differences: List[str]
    final_consensus: str
    recommended_actions: List[str]


class DebateReportCreate(BaseModel):
    primary_risk: Dict[str, Any]
    agents: Dict[str, Any]
    debate_summary: Dict[str, Any]


class DebateReportRead(BaseModel):
    id: str
    project_id: str
    primary_risk: Dict[str, Any]
    agents: Dict[str, Any]
    debate_summary: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)