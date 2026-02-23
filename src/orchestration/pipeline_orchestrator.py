"""
Multi-Agent Pipeline Orchestrator

This module coordinates the execution of specialized agents in the data analysis pipeline.
Each agent performs a specific stage of the analysis workflow and hands off results to the next agent.
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from loguru import logger

# Configure logger
logger.add(
    "logs/orchestration/orchestrator_{time}.log",
    rotation="1 day",
    retention="30 days",
    level="INFO"
)


@dataclass
class AgentContext:
    """Context passed to an agent during execution."""
    
    problem_statement_num: str
    problem_statement_title: str
    timestamp: str
    stage: int
    agent_name: str
    instructions: List[str]
    inputs: Dict[str, str] = field(default_factory=dict)
    previous_findings: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        """Convert context to dictionary for template population."""
        return {
            "problem_statement_num": self.problem_statement_num,
            "problem_statement_title": self.problem_statement_title,
            "timestamp": self.timestamp,
            "stage": self.stage,
            "agent_name": self.agent_name,
            **self.inputs,
            **self.previous_findings
        }


@dataclass
class AgentResult:
    """Result returned by an agent after execution."""
    
    agent_name: str
    stage: int
    validation_status: str  # "passed", "warning", "failed"
    outputs: Dict[str, Any]
    findings: Dict[str, Any]
    recommended_next_step: str
    execution_time_seconds: float
    handoff_file: Optional[Path] = None


class MultiAgentOrchestrator:
    """Orchestrates multi-agent data analysis pipeline."""
    
    def __init__(self, config_path: str = ".agents/config.yml"):
        """Initialize orchestrator with configuration."""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.registry = self._load_registry()
        self.execution_history: List[AgentResult] = []
        
        logger.info(f"Initialized MultiAgentOrchestrator with pipeline type: {self.config['orchestrator']['pipeline_type']}")
    
    def _load_config(self) -> dict:
        """Load orchestration configuration."""
        with open(self.config_path) as f:
            return yaml.safe_load(f)
    
    def _load_registry(self) -> dict:
        """Load agent registry."""
        registry_path = Path(".agents/registry.yml")
        with open(registry_path) as f:
            return yaml.safe_load(f)
    
    def _load_agent_template(self, agent_id: str) -> str:
        """Load agent prompt template."""
        agent_config = self.config['agents'][agent_id]
        template_path = Path(agent_config['prompt_template'])
        
        with open(template_path) as f:
            return f.read()
    
    def _populate_template(self, template: str, context: AgentContext) -> str:
        """Populate template with context variables."""
        context_dict = context.to_dict()
        
        for key, value in context_dict.items():
            placeholder = f"{{{key}}}"
            template = template.replace(placeholder, str(value))
        
        return template
    
    def _read_handoff(self, handoff_file: Path) -> dict:
        """Read handoff file from previous agent."""
        if not handoff_file.exists():
            raise FileNotFoundError(f"Handoff file not found: {handoff_file}")
        
        with open(handoff_file) as f:
            return json.load(f)
    
    def _create_handoff(
        self,
        agent_name: str,
        stage: int,
        problem_statement: str,
        outputs: dict,
        findings: dict,
        next_step: str,
        validation_status: str = "passed"
    ) -> Path:
        """Create handoff file for next agent."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        handoff_data = {
            "agent_name": agent_name,
            "timestamp": timestamp,
            "stage": stage,
            "problem_statement": problem_statement,
            "outputs": outputs,
            "validation_status": validation_status,
            "findings": findings,
            "recommended_next_step": next_step
        }
        
        # Create handoff file
        handoff_dir = Path("data/3_interim/agent_handoffs")
        handoff_dir.mkdir(parents=True, exist_ok=True)
        
        handoff_file = handoff_dir / f"{agent_name.lower()}_to_{next_step}_{timestamp}.json"
        
        with open(handoff_file, 'w') as f:
            json.dump(handoff_data, f, indent=2)
        
        logger.info(f"Created handoff file: {handoff_file}")
        return handoff_file
    
    def _validate_outputs(self, outputs: dict) -> bool:
        """Validate that all output files exist."""
        for output_type, file_path in outputs.items():
            if isinstance(file_path, str):
                if not Path(file_path).exists():
                    logger.error(f"{output_type} file not found: {file_path}")
                    return False
            elif isinstance(file_path, list):
                for fp in file_path:
                    if not Path(fp).exists():
                        logger.error(f"{output_type} file not found: {fp}")
                        return False
        return True
    
    def execute_agent(
        self,
        agent_id: str,
        context: AgentContext,
        previous_handoff: Optional[Path] = None
    ) -> AgentResult:
        """
        Execute a single agent.
        
        Args:
            agent_id: Agent identifier (e.g., "extraction", "profiling")
            context: Execution context for the agent
            previous_handoff: Path to handoff file from previous agent
        
        Returns:
            AgentResult with execution details
        """
        start_time = datetime.now()
        logger.info(f"Starting {context.agent_name} (Stage {context.stage})")
        
        # Load previous agent's findings if available
        if previous_handoff:
            previous_data = self._read_handoff(previous_handoff)
            context.previous_findings = previous_data.get('findings', {})
            context.inputs.update(previous_data.get('outputs', {}))
        
        # Load and populate agent template
        template = self._load_agent_template(agent_id)
        agent_prompt = self._populate_template(template, context)
        
        # THIS IS WHERE YOU WOULD INVOKE THE ACTUAL AI AGENT
        # For now, this is a placeholder for the orchestration logic
        logger.info(f"Agent prompt prepared for {context.agent_name}")
        logger.info(f"Instructions: {', '.join(context.instructions)}")
        
        # Placeholder result - in real implementation, this comes from agent execution
        # You would integrate with your AI agent framework here
        result = AgentResult(
            agent_name=context.agent_name,
            stage=context.stage,
            validation_status="passed",
            outputs={},  # Agent would populate this
            findings={},  # Agent would populate this
            recommended_next_step="",  # Agent would determine this
            execution_time_seconds=(datetime.now() - start_time).total_seconds()
        )
        
        logger.info(f"Completed {context.agent_name} in {result.execution_time_seconds:.2f}s")
        
        self.execution_history.append(result)
        return result
    
    def run_sequential_pipeline(
        self,
        problem_statement_num: str,
        problem_statement_title: str,
        agents: Optional[List[str]] = None
    ) -> List[AgentResult]:
        """
        Run agents sequentially in pipeline order.
        
        Args:
            problem_statement_num: Problem statement number (e.g., "001")
            problem_statement_title: Problem statement title
            agents: List of agent IDs to run (default: all in config order)
        
        Returns:
            List of agent results
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if agents is None:
            agents = list(self.config['agents'].keys())
        
        logger.info(f"Starting sequential pipeline for PS-{problem_statement_num}")
        logger.info(f"Agents: {' → '.join(agents)}")
        
        results = []
        previous_handoff = None
        
        for agent_id in agents:
            agent_config = self.config['agents'][agent_id]
            
            # Create agent context
            context = AgentContext(
                problem_statement_num=problem_statement_num,
                problem_statement_title=problem_statement_title,
                timestamp=timestamp,
                stage=agent_config['scope']['stages'][0],
                agent_name=agent_config['name'],
                instructions=agent_config['instructions']
            )
            
            # Execute agent
            result = self.execute_agent(agent_id, context, previous_handoff)
            results.append(result)
            
            # Check validation status
            if result.validation_status == "failed":
                logger.error(f"{result.agent_name} validation failed. Stopping pipeline.")
                break
            
            # Create handoff for next agent
            if result.recommended_next_step and result.recommended_next_step != "complete":
                previous_handoff = self._create_handoff(
                    agent_name=result.agent_name,
                    stage=result.stage,
                    problem_statement=problem_statement_num,
                    outputs=result.outputs,
                    findings=result.findings,
                    next_step=result.recommended_next_step,
                    validation_status=result.validation_status
                )
                result.handoff_file = previous_handoff
        
        logger.info(f"Pipeline completed. Executed {len(results)} agents.")
        return results
    
    def run_parallel_pipeline(
        self,
        problem_statement_num: str,
        problem_statement_title: str,
        parallel_tasks: List[str]
    ) -> List[AgentResult]:
        """
        Run multiple agents in parallel (for independent tasks).
        
        Args:
            problem_statement_num: Problem statement number
            problem_statement_title: Problem statement title
            parallel_tasks: List of agent IDs to run in parallel
        
        Returns:
            List of agent results
        """
        logger.info(f"Starting parallel execution for tasks: {', '.join(parallel_tasks)}")
        
        # In a real implementation, you would use threading/async here
        # For now, this is a sequential placeholder
        results = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for agent_id in parallel_tasks:
            agent_config = self.config['agents'][agent_id]
            
            context = AgentContext(
                problem_statement_num=problem_statement_num,
                problem_statement_title=problem_statement_title,
                timestamp=timestamp,
                stage=agent_config['scope']['stages'][0],
                agent_name=agent_config['name'],
                instructions=agent_config['instructions']
            )
            
            result = self.execute_agent(agent_id, context)
            results.append(result)
        
        logger.info(f"Parallel execution completed. {len(results)} tasks finished.")
        return results
    
    def generate_pipeline_report(self) -> str:
        """Generate execution report for the pipeline."""
        if not self.execution_history:
            return "No pipeline execution history available."
        
        total_time = sum(r.execution_time_seconds for r in self.execution_history)
        
        report = f"""
# Pipeline Execution Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Agents Executed: {len(self.execution_history)}
- Total Execution Time: {total_time:.2f} seconds
- Pipeline Type: {self.config['orchestrator']['pipeline_type']}

## Agent Execution Details
"""
        
        for i, result in enumerate(self.execution_history, 1):
            report += f"""
### {i}. {result.agent_name} (Stage {result.stage})
- Validation Status: {result.validation_status}
- Execution Time: {result.execution_time_seconds:.2f}s
- Next Step: {result.recommended_next_step}
"""
        
        return report


def main():
    """Example usage of the orchestrator."""
    orchestrator = MultiAgentOrchestrator()
    
    # Example: Run sequential pipeline for Problem Statement 001
    results = orchestrator.run_sequential_pipeline(
        problem_statement_num="001",
        problem_statement_title="Workforce Capacity Mismatch",
        agents=["extraction", "profiling", "cleaning", "eda"]
    )
    
    # Generate report
    report = orchestrator.generate_pipeline_report()
    print(report)
    
    # Save report
    report_path = Path("logs/orchestration/pipeline_report.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report)


if __name__ == "__main__":
    main()
