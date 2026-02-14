"""State Manager for workflow state tracking"""
from typing import Dict, Any, Optional
from datetime import datetime
import json

class StateManager:
    def __init__(self):
        self.state = {
            'workflow_id': None,
            'status': 'not_started',
            'start_time': None,
            'end_time': None,
            'current_agent': None,
            'agents_completed': [],
            'agent_results': {},
            'errors': []
        }
    
    def start_workflow(self):
        self.state['workflow_id'] = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.state['status'] = 'running'
        self.state['start_time'] = datetime.now().isoformat()
    
    def update(self, agent_name: str, result: Dict[str, Any]):
        self.state['current_agent'] = agent_name
        self.state['agent_results'][agent_name] = result
        if result.get('success'):
            self.state['agents_completed'].append(agent_name)
    
    def complete_workflow(self):
        self.state['status'] = 'completed'
        self.state['end_time'] = datetime.now().isoformat()
    
    def fail_workflow(self, error: str):
        self.state['status'] = 'failed'
        self.state['end_time'] = datetime.now().isoformat()
        self.state['errors'].append({'timestamp': datetime.now().isoformat(), 'error': error})
    
    def get_state(self) -> Dict[str, Any]:
        return self.state.copy()
