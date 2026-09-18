"""Pydantic schemas for the RiskAssessment entity.

`RiskIngest` is the STABLE JSON CONTRACT the AI/orchestration teammate's
Gemini layer (or any future LLM provider: Claude, OpenAI, etc.) must send to
this backend to persist a set of discovered risks for a project.
"""
from __future__ import annotations

import datetime as dt
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskItem(BaseModel):
    """A single risk finding produced by one of the AI red-team agents."""

    title: str = Field(..., min_length=1, max_length=255)
    category: str = Field(
        ..., min_length=1, max_length=100, description="e.g. CyberSecurity, SRE, FinOps"
    )
    severity: Severity = Field(..., description="LOW | MEDIUM | HIGH | CRITICAL")
    description: str = Field(..., min_length=1)
    evidence: str = Field(default="", description="Evidence supporting the finding")
    recommendation: str = Field(default="", description="Suggested remediation")
    agent: str = Field(
        ..., min_length=1, max_length=100, description="Name of the AI agent, e.g. 'SRE'"
    )


class RiskIngest(BaseModel):
    """
    Payload accepted from the AI/orchestration layer (or mock fixtures) to
    create/replace the RiskAssessment for a project.

    Example:
    {
        "provider": "gemini",
        "model": "gemini-2.5-pro",
        "risks": [
            {
                "title": "Single Point of Failure",
                "category": "SRE",
                "severity": "CRITICAL",
                "description": "The architecture depends on a single backend server.",
                "evidence": "Only one backend instance is present.",
                "recommendation": "Use multiple instances behind a load balancer.",
                "agent": "SRE"
            }
        ],
        "raw_analysis": { ... optional full AI response ... }
    }
    """

    provider: Optional[str] = Field(default=None, max_length=100)
    model: Optional[str] = Field(default=None, max_length=150)
    risks: list[RiskItem] = Field(default_factory=list)
    raw_analysis: Optional[dict[str, Any]] = Field(default=None)


class RiskUpdate(BaseModel):
    """Payload for partially updating an existing RiskAssessment."""

    provider: Optional[str] = Field(default=None, max_length=100)
    model: Optional[str] = Field(default=None, max_length=150)
    risks: Optional[list[RiskItem]] = None
    raw_analysis: Optional[dict[str, Any]] = None


class RiskAssessmentRead(BaseModel):
    """Full RiskAssessment representation returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: str
    risks: list[RiskItem]
    raw_analysis: Optional[dict[str, Any]] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    created_at: dt.datetime
    updated_at: dt.datetime
