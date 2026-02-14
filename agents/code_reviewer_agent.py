"""Agent 3: Code Reviewer"""
from typing import Dict, Any, Optional
from pathlib import Path
from .base_agent import BaseAgent

class CodeReviewerAgent(BaseAgent):
    def __init__(self, config: Any):
        system_message = """Expert code reviewer. Check for:
        - Syntax errors
        - Logic errors
        - Security vulnerabilities
        - Performance issues
        - Best practices"""
        super().__init__("CodeReviewerAgent", "Code Review", system_message, config)
    
    def validate_input(self, input_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        if not input_data.get('project_path'):
            return False, "Project path missing"
        return True, None
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Starting code review...")
        project_path = Path(input_data['project_path'])
        
        review_results = {
            'issues_found': [],
            'suggestions': [],
            'security_warnings': [],
            'performance_tips': []
        }
        
        # Scan Python files
        for py_file in project_path.rglob('*.py'):
            issues = self._review_file(py_file)
            if issues:
                review_results['issues_found'].extend(issues)
        
        self.logger.info(f"Review complete. Found {len(review_results['issues_found'])} issues")
        
        return review_results
    
    def _review_file(self, file_path: Path) -> list:
        issues = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Basic checks
                if 'import *' in content:
                    issues.append({'file': str(file_path), 'issue': 'Avoid wildcard imports'})
                if 'eval(' in content:
                    issues.append({'file': str(file_path), 'issue': 'Security: eval() usage detected'})
        except Exception as e:
            issues.append({'file': str(file_path), 'error': str(e)})
        return issues
    
    def generate_output(self, processed_data: Any) -> Dict[str, Any]:
        return {'status': 'completed', 'review_complete': True, 'data': processed_data}
