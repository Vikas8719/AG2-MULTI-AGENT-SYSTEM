"""Workflow Manager - Orchestrates the 5-agent workflow"""
from typing import Dict, Any, Optional
import logging
from agents import (
    AnalyzerAgent,
    CodeGeneratorAgent,
    CodeReviewerAgent,
    DevOpsAgent,
    ValidatorAgent
)
from .state_manager import StateManager

class WorkflowManager:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("workflow_manager")
        self.state_manager = StateManager()
        
        # Initialize agents
        self.agents = {
            'analyzer': AnalyzerAgent(config),
            'code_generator': CodeGeneratorAgent(config),
            'code_reviewer': CodeReviewerAgent(config),
            'devops': DevOpsAgent(config),
            'validator': ValidatorAgent(config)
        }
        

        self.logger.info("Workflow Manager initialized with 5 agents")
        
        # Initialize Vector DB
        try:
            from utils.vector_db import VectorDB
            self.vector_db = VectorDB()
            self.logger.info("Vector DB initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize Vector DB: {e}")
            self.vector_db = None
    
    def execute_workflow(
        self,
        input_data: str,
        input_type: str,
        cloud_provider: str,
        project_name: Optional[str] = None,
        status_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Execute complete 5-agent workflow"""
        
        self.logger.info("Starting AG2 Multi-Agent Workflow")
        self.state_manager.start_workflow()
        
        if status_callback:
            status_callback("🚀 Starting workflow...", "init")
        
        try:
            # Prepare input
            agent_input = self._prepare_input(input_data, input_type, cloud_provider, project_name)
            
            # Agent 1: Analyzer & Planner
            if status_callback:
                status_callback("🔍 Agent 1: Analyzer & Planner is analyzing requirements...", "analyzer")
            self.logger.info("=== AGENT 1: ANALYZER & PLANNER ===")
            analyzer_result = self.agents['analyzer'].run(agent_input)
            self.state_manager.update('analyzer', analyzer_result)
            

            if not analyzer_result['success']:
                raise Exception(f"Analyzer failed: {analyzer_result.get('error')}")
            
            # Store Memory
            self._store_agent_memory('analyzer', analyzer_result)
            
            # Agent 2: Code Generator
            if status_callback:
                status_callback("💻 Agent 2: Code Generator is building the application...", "code_gen")
            self.logger.info("=== AGENT 2: CODE GENERATOR ===")
            code_gen_input = self._prepare_code_gen_input(analyzer_result)
            code_gen_result = self.agents['code_generator'].run(code_gen_input)
            self.state_manager.update('code_generator', code_gen_result)
            

            if not code_gen_result['success']:
                raise Exception(f"Code generation failed: {code_gen_result.get('error')}")
            
            # Store Memory
            self._store_agent_memory('code_generator', code_gen_result)
            
            # Agent 3: Code Reviewer
            if status_callback:
                status_callback("👀 Agent 3: Code Reviewer is inspecting the code...", "reviewer")
            self.logger.info("=== AGENT 3: CODE REVIEWER ===")
            review_input = self._prepare_review_input(code_gen_result)

            review_result = self.agents['code_reviewer'].run(review_input)
            self.state_manager.update('code_reviewer', review_result)
            
            # Store Memory
            self._store_agent_memory('code_reviewer', review_result)
            
            # Agent 4: DevOps Engineer
            if status_callback:
                status_callback("☁️ Agent 4: DevOps Engineer is preparing deployment configs...", "devops")
            self.logger.info("=== AGENT 4: DEVOPS ENGINEER ===")
            devops_input = self._prepare_devops_input(code_gen_result, cloud_provider)

            devops_result = self.agents['devops'].run(devops_input)
            self.state_manager.update('devops', devops_result)
            
            # Store Memory
            self._store_agent_memory('devops', devops_result)
            
            # Agent 5: Validator
            if status_callback:
                status_callback("✅ Agent 5: Validator is verifying everything...", "validator")
            self.logger.info("=== AGENT 5: VALIDATOR & RELEASE MANAGER ===")
            validator_input = self._prepare_validator_input(
                analyzer_result, code_gen_result, review_result, devops_result
            )

            validator_result = self.agents['validator'].run(validator_input)
            self.state_manager.update('validator', validator_result)
            
            # Store Memory
            self._store_agent_memory('validator', validator_result)
            
            self.state_manager.complete_workflow()
            self.state_manager.complete_workflow()
            self.logger.info("Workflow completed successfully!")
            
            if status_callback:
                status_callback("✨ Workflow completed successfully!", "complete")
            
            return {
                'success': True,
                'workflow_state': self.state_manager.get_state(),
                'project_path': code_gen_result['result']['project_path'],
                'ready_for_approval': True
            }
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}", exc_info=True)
            self.state_manager.fail_workflow(str(e))
            return {
                'success': False,
                'error': str(e),
                'workflow_state': self.state_manager.get_state()
            }
    
    def _prepare_input(self, data: str, input_type: str, cloud: str, name: str) -> Dict:
        if input_type == 'csv':
            return {'type': 'csv', 'csv_path': data, 'cloud_provider': cloud, 'project_name': name}
        else:
            return {'type': 'text', 'task_description': data, 'cloud_provider': cloud, 'project_name': name}
    
    def _prepare_code_gen_input(self, analyzer_result: Dict) -> Dict:
        return analyzer_result['result']
    
    def _prepare_review_input(self, code_gen_result: Dict) -> Dict:
        return code_gen_result['result']
    
    def _prepare_devops_input(self, code_gen_result: Dict, cloud: str) -> Dict:
        return {**code_gen_result['result'], 'cloud_provider': cloud}
    
    def _prepare_validator_input(self, *results) -> Dict:
        return {'all_results': results}
    

    def get_workflow_state(self) -> Dict:
        return self.state_manager.get_state()

    def _store_agent_memory(self, agent_name: str, result: Dict[str, Any]):
        """Store agent result in Vector DB memory"""
        try:
            if result.get('success'):
                memory_text = str(result.get('result', ''))
                if memory_text:
                    metadata = {
                        'agent': agent_name,
                        'timestamp': self.state_manager.state['start_time'],
                        'workflow_id': self.state_manager.state['workflow_id']
                    }
                    if self.vector_db:
                        self.vector_db.add_memory(
                            text=memory_text[:1000],  # Store first 1000 chars of result as summary
                            metadata=metadata,
                            memory_id=f"{self.state_manager.state['workflow_id']}_{agent_name}"
                        )
        except Exception as e:
            self.logger.error(f"Failed to store memory for {agent_name}: {e}")
