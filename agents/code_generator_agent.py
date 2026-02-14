"""Agent 2: Code Generator - Creates working code"""
from typing import Dict, Any, Optional
from pathlib import Path
import os
from .base_agent import BaseAgent

class CodeGeneratorAgent(BaseAgent):
    def __init__(self, config: Any):
        system_message = """You are an expert software developer. Generate production-ready code with:
        - Clean architecture
        - Proper error handling
        - Comprehensive logging
        - Type hints
        - Docstrings
        - Configuration files"""
        super().__init__("CodeGeneratorAgent", "Code Generation", system_message, config)
    
    def validate_input(self, input_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        if not input_data.get('project_plan'):
            return False, "Project plan missing"
        if not input_data.get('folder_structure'):
            return False, "Folder structure missing"
        return True, None
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Starting code generation...")
        project_plan = input_data['project_plan']
        folder_structure = input_data['folder_structure']
        tech_stack = input_data.get('tech_stack', {})
        
        project_path = Path('projects') / project_plan['project_name']
        self._create_project_structure(project_path, folder_structure)
        generated_files = self._generate_code_files(project_path, project_plan, tech_stack)
        
        return {
            'project_path': str(project_path),
            'generated_files': generated_files,
            'tech_stack': tech_stack
        }
    
    def _create_project_structure(self, project_path: Path, structure: Dict):
        project_path.mkdir(parents=True, exist_ok=True)
        for dir_name in structure.get('directories', []):
            (project_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    def _generate_code_files(self, project_path: Path, plan: Dict, tech_stack: Dict) -> list:
        files = []
        # Generate main application file
        main_file = project_path / 'src' / 'main.py'
        main_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(main_file, 'w') as f:
            f.write(self._generate_main_code(plan, tech_stack))
        files.append(str(main_file))
        
        # Generate requirements.txt
        req_file = project_path / 'requirements.txt'
        with open(req_file, 'w') as f:
            f.write(self._generate_requirements(tech_stack))
        files.append(str(req_file))
        
        # Generate README
        readme = project_path / 'README.md'
        with open(readme, 'w') as f:
            f.write(self._generate_readme(plan))
        files.append(str(readme))
        
        return files
    
    def _generate_main_code(self, plan: Dict, tech_stack: Dict) -> str:
        return f'''"""
{plan.get('project_name', 'Application')}
{plan.get('description', 'Generated application')}
"""
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Application:
    def __init__(self):
        self.config = self._load_config()
        logger.info("Application initialized")
    
    def _load_config(self) -> dict:
        return {{"app_name": "{plan.get('project_name', 'app')}"}}
    
    def run(self):
        logger.info("Application starting...")
        # Main application logic here
        pass

if __name__ == "__main__":
    app = Application()
    app.run()
'''
    
    def _generate_requirements(self, tech_stack: Dict) -> str:
        reqs = ['python-dotenv==1.0.0', 'pydantic==2.5.0']
        framework = tech_stack.get('framework', '').lower()
        if 'fastapi' in framework:
            reqs.extend(['fastapi==0.109.0', 'uvicorn==0.25.0'])
        if 'flask' in framework:
            reqs.append('flask==3.0.0')
        return '\n'.join(reqs)
    
    def _generate_readme(self, plan: Dict) -> str:
        return f'''# {plan.get('project_name', 'Project')}

## Description
{plan.get('description', 'Generated project')}

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python src/main.py
```
'''
    
    def generate_output(self, processed_data: Any) -> Dict[str, Any]:
        return {'status': 'completed', 'code_generated': True, 'data': processed_data}
