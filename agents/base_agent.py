"""
Base Agent Class for AG2 Multi-Agent System
Provides common functionality for all agents
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime
import json
from config import get_logger


class BaseAgent(ABC):
    """
    Abstract Base Class for all AG2 Agents
    Defines common interface and shared functionality
    """
    
    def __init__(
        self,
        name: str,
        role: str,
        system_message: str,
        config: Any,
        llm_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize Base Agent
        
        Args:
            name: Agent name
            role: Agent role/responsibility
            system_message: System prompt for the agent
            config: Application configuration
            llm_config: LLM configuration for AG2
        """
        self.name = name
        self.role = role
        self.system_message = system_message
        self.config = config
        self.llm_config = llm_config or self._get_default_llm_config()
        
        # Setup agent-specific logger
        self.logger = get_logger(f"agent.{name}")
        
        # Agent state
        self.state = {
            'status': 'initialized',
            'start_time': None,
            'end_time': None,
            'input': None,
            'output': None,
            'errors': [],
            'metrics': {}
        }
        
        # Execution history
        self.history = []
        
        self.logger.info(f"Agent {name} initialized with role: {role}")
    
    def _get_default_llm_config(self) -> Dict[str, Any]:
        """Get default LLM configuration from app config based on selected provider"""
        provider = self.config.ag2.llm_provider
        
        base_config = {
            "temperature": self.config.ag2.ag2_temperature,
            "max_tokens": self.config.ag2.ag2_max_tokens,
            "timeout": self.config.timeouts.agent_timeout,
            "provider": provider
        }
        
        if provider == "openai":
            base_config.update({
                "model": self.config.ag2.ag2_model or "gpt-4-turbo-preview",
                "api_key": self.config.ag2.openai_api_key,
                "api_type": "openai"
            })
        elif provider == "huggingface":
            base_config.update({
                "model": self.config.ag2.huggingface_model,
                "api_key": self.config.ag2.huggingface_api_key,
                "base_url": self.config.ag2.huggingface_endpoint or "https://api-inference.huggingface.co/models",
                "api_type": "huggingface"
            })
        elif provider == "anthropic":
            base_config.update({
                "model": self.config.ag2.anthropic_model,
                "api_key": self.config.ag2.anthropic_api_key,
                "api_type": "anthropic"
            })
        
        return base_config

    
    @abstractmethod
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute agent's main task
        Must be implemented by subclasses
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Dict containing execution results
        """
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """
        Validate input data
        Must be implemented by subclasses
        
        Args:
            input_data: Input data to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @abstractmethod
    def generate_output(self, processed_data: Any) -> Dict[str, Any]:
        """
        Generate formatted output
        Must be implemented by subclasses
        
        Args:
            processed_data: Processed data to format
            
        Returns:
            Formatted output dictionary
        """
        pass
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method with error handling and logging
        
        Args:
            input_data: Input data for the agent
            
        Returns:
            Execution results
        """
        self.logger.info(f"Starting execution for agent: {self.name}")
        self.state['status'] = 'running'
        self.state['start_time'] = datetime.now().isoformat()
        self.state['input'] = input_data
        
        try:
            # Validate input
            is_valid, error_msg = self.validate_input(input_data)
            if not is_valid:
                raise ValueError(f"Input validation failed: {error_msg}")
            
            # Execute main task
            result = self.execute(input_data)
            
            # Update state
            self.state['status'] = 'completed'
            self.state['end_time'] = datetime.now().isoformat()
            self.state['output'] = result
            
            # Add to history
            self._add_to_history('execution', result)
            
            self.logger.info(f"Successfully completed execution for agent: {self.name}")
            
            return {
                'success': True,
                'agent': self.name,
                'result': result,
                'state': self.state
            }
            
        except Exception as e:
            self.logger.error(f"Execution failed for agent {self.name}: {str(e)}", exc_info=True)
            
            self.state['status'] = 'failed'
            self.state['end_time'] = datetime.now().isoformat()
            self.state['errors'].append({
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'type': type(e).__name__
            })
            
            self._add_to_history('error', {'error': str(e)})
            
            return {
                'success': False,
                'agent': self.name,
                'error': str(e),
                'state': self.state
            }
    
    def _add_to_history(self, action: str, data: Any):
        """Add entry to execution history"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'data': data
        })
    
    def get_state(self) -> Dict[str, Any]:
        """Get current agent state"""
        return self.state.copy()
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self.history.copy()
    
    def reset(self):
        """Reset agent state"""
        self.logger.info(f"Resetting agent: {self.name}")
        self.state = {
            'status': 'initialized',
            'start_time': None,
            'end_time': None,
            'input': None,
            'output': None,
            'errors': [],
            'metrics': {}
        }
        self.history = []
    
    def log_metric(self, metric_name: str, value: Any):
        """Log a metric"""
        self.state['metrics'][metric_name] = value
        self.logger.info(f"Metric recorded - {metric_name}: {value}")
    
    def update_status(self, status: str, message: Optional[str] = None):
        """Update agent status"""
        self.state['status'] = status
        log_msg = f"Status updated to: {status}"
        if message:
            log_msg += f" - {message}"
        self.logger.info(log_msg)
    
    def create_system_prompt(self, additional_context: Optional[str] = None) -> str:
        """
        Create complete system prompt
        
        Args:
            additional_context: Additional context to add to prompt
            
        Returns:
            Complete system prompt
        """
        prompt = f"{self.system_message}\n\n"
        prompt += f"You are {self.name}, responsible for {self.role}.\n"
        
        if additional_context:
            prompt += f"\nAdditional Context:\n{additional_context}\n"
        
        return prompt
    
    def format_output_for_next_agent(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format output for next agent in workflow
        
        Args:
            output: Raw output from agent
            
        Returns:
            Formatted output
        """
        return {
            'from_agent': self.name,
            'timestamp': datetime.now().isoformat(),
            'data': output,
            'metadata': {
                'execution_time': self._calculate_execution_time(),
                'status': self.state['status']
            }
        }
    
    def _calculate_execution_time(self) -> Optional[float]:
        """Calculate execution time in seconds"""
        if self.state['start_time'] and self.state['end_time']:
            start = datetime.fromisoformat(self.state['start_time'])
            end = datetime.fromisoformat(self.state['end_time'])
            return (end - start).total_seconds()
        return None
    
    def save_output_to_file(self, output: Any, file_path: str):
        """
        Save output to file
        
        Args:
            output: Output data to save
            file_path: Path to save file
        """
        try:
            with open(file_path, 'w') as f:
                if isinstance(output, (dict, list)):
                    json.dump(output, f, indent=2)
                else:
                    f.write(str(output))
            
            self.logger.info(f"Output saved to: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to save output to {file_path}: {str(e)}")
            raise
    
    def load_input_from_file(self, file_path: str) -> Any:
        """
        Load input from file
        
        Args:
            file_path: Path to input file
            
        Returns:
            Loaded data
        """
        try:
            with open(file_path, 'r') as f:
                if file_path.endswith('.json'):
                    return json.load(f)
                else:
                    return f.read()
                    
        except Exception as e:
            self.logger.error(f"Failed to load input from {file_path}: {str(e)}")
            raise
    
    def __repr__(self) -> str:
        """String representation of agent"""
        return f"{self.__class__.__name__}(name='{self.name}', role='{self.role}', status='{self.state['status']}')"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert agent to dictionary representation"""
        return {
            'name': self.name,
            'role': self.role,
            'state': self.state,
            'history_count': len(self.history)
        }


__all__ = ['BaseAgent']
