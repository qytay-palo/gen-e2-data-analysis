"""
Orchestration Module

Provides utilities for coordinating multi-agent data analysis pipelines.
"""

from .pipeline_orchestrator import (
    MultiAgentOrchestrator,
    AgentContext,
    AgentResult
)

__all__ = [
    "MultiAgentOrchestrator",
    "AgentContext",
    "AgentResult"
]
