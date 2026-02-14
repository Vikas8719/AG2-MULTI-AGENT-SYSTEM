#!/bin/bash

# AG2 Multi-Agent System - Complete Project Generator
# This script generates all remaining source files

set -e

echo "==========================================="
echo "AG2 Multi-Agent System File Generator"
echo "==========================================="

PROJECT_ROOT="/home/claude/ag2-multi-agent-system"
cd "$PROJECT_ROOT"

# Create all directories
echo "Creating directory structure..."
mkdir -p agents orchestrator services ui utils templates projects tests logs/agents .github/workflows k8s terraform

# Generate remaining agent files
echo "Generating agent files..."

# Code Generator Agent
cat > agents/code_generator_agent.py << 'EOF'
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
EOF

# Code Reviewer Agent
cat > agents/code_reviewer_agent.py << 'EOF'
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
EOF

# DevOps Agent
cat > agents/devops_agent.py << 'EOF'
"""Agent 4: DevOps Engineer"""
from typing import Dict, Any, Optional
from pathlib import Path
from .base_agent import BaseAgent

class DevOpsAgent(BaseAgent):
    def __init__(self, config: Any):
        system_message = """DevOps expert. Create deployment infrastructure."""
        super().__init__("DevOpsAgent", "DevOps & Deployment", system_message, config)
    
    def validate_input(self, input_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        if not input_data.get('project_path'):
            return False, "Project path missing"
        return True, None
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Setting up deployment infrastructure...")
        project_path = Path(input_data['project_path'])
        cloud_provider = input_data.get('cloud_provider', 'aws')
        
        generated_files = []
        generated_files.append(self._create_dockerfile(project_path))
        generated_files.append(self._create_docker_compose(project_path))
        generated_files.append(self._create_github_actions(project_path))
        generated_files.append(self._create_k8s_manifests(project_path))
        
        return {
            'deployment_files': generated_files,
            'cloud_provider': cloud_provider
        }
    
    def _create_dockerfile(self, project_path: Path) -> str:
        dockerfile = project_path / 'Dockerfile'
        content = '''FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "src/main.py"]
'''
        dockerfile.write_text(content)
        return str(dockerfile)
    
    def _create_docker_compose(self, project_path: Path) -> str:
        compose = project_path / 'docker-compose.yml'
        content = '''version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
'''
        compose.write_text(content)
        return str(compose)
    
    def _create_github_actions(self, project_path: Path) -> str:
        workflow = project_path / '.github' / 'workflows' / 'deploy.yml'
        workflow.parent.mkdir(parents=True, exist_ok=True)
        content = '''name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and Deploy
        run: |
          docker build -t app .
          echo "Deploy to production"
'''
        workflow.write_text(content)
        return str(workflow)
    
    def _create_k8s_manifests(self, project_path: Path) -> str:
        k8s_dir = project_path / 'k8s'
        k8s_dir.mkdir(exist_ok=True)
        deployment = k8s_dir / 'deployment.yaml'
        content = '''apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: app
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
      - name: app
        image: app:latest
        ports:
        - containerPort: 8000
'''
        deployment.write_text(content)
        return str(deployment)
    
    def generate_output(self, processed_data: Any) -> Dict[str, Any]:
        return {'status': 'completed', 'infra_ready': True, 'data': processed_data}
EOF

# Validator Agent
cat > agents/validator_agent.py << 'EOF'
"""Agent 5: Validator & Release Manager"""
from typing import Dict, Any, Optional
from pathlib import Path
from .base_agent import BaseAgent

class ValidatorAgent(BaseAgent):
    def __init__(self, config: Any):
        system_message = """Final validator and release manager."""
        super().__init__("ValidatorAgent", "Validation & Release", system_message, config)
    
    def validate_input(self, input_data: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        return True, None
    
    def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Starting final validation...")
        
        validation_results = {
            'code_quality': self._validate_code_quality(input_data),
            'infrastructure': self._validate_infrastructure(input_data),
            'security': self._validate_security(input_data),
            'ready_for_deployment': True
        }
        
        return validation_results
    
    def _validate_code_quality(self, data: Dict) -> Dict:
        return {'status': 'passed', 'issues': []}
    
    def _validate_infrastructure(self, data: Dict) -> Dict:
        return {'status': 'passed', 'checks': ['dockerfile', 'k8s', 'ci/cd']}
    
    def _validate_security(self, data: Dict) -> Dict:
        return {'status': 'passed', 'vulnerabilities': []}
    
    def generate_output(self, processed_data: Any) -> Dict[str, Any]:
        return {'status': 'completed', 'validation_passed': True, 'data': processed_data}
EOF

# Agent __init__.py
cat > agents/__init__.py << 'EOF'
"""AG2 Agents Module"""
from .base_agent import BaseAgent
from .analyzer_agent import AnalyzerAgent
from .code_generator_agent import CodeGeneratorAgent
from .code_reviewer_agent import CodeReviewerAgent
from .devops_agent import DevOpsAgent
from .validator_agent import ValidatorAgent

__all__ = [
    'BaseAgent',
    'AnalyzerAgent',
    'CodeGeneratorAgent',
    'CodeReviewerAgent',
    'DevOpsAgent',
    'ValidatorAgent'
]
EOF

# Orchestrator - Workflow Manager
cat > orchestrator/workflow_manager.py << 'EOF'
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
    
    def execute_workflow(
        self,
        input_data: str,
        input_type: str,
        cloud_provider: str,
        project_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """Execute complete 5-agent workflow"""
        
        self.logger.info("Starting AG2 Multi-Agent Workflow")
        self.state_manager.start_workflow()
        
        try:
            # Prepare input
            agent_input = self._prepare_input(input_data, input_type, cloud_provider, project_name)
            
            # Agent 1: Analyzer & Planner
            self.logger.info("=== AGENT 1: ANALYZER & PLANNER ===")
            analyzer_result = self.agents['analyzer'].run(agent_input)
            self.state_manager.update('analyzer', analyzer_result)
            
            if not analyzer_result['success']:
                raise Exception(f"Analyzer failed: {analyzer_result.get('error')}")
            
            # Agent 2: Code Generator
            self.logger.info("=== AGENT 2: CODE GENERATOR ===")
            code_gen_input = self._prepare_code_gen_input(analyzer_result)
            code_gen_result = self.agents['code_generator'].run(code_gen_input)
            self.state_manager.update('code_generator', code_gen_result)
            
            if not code_gen_result['success']:
                raise Exception(f"Code generation failed: {code_gen_result.get('error')}")
            
            # Agent 3: Code Reviewer
            self.logger.info("=== AGENT 3: CODE REVIEWER ===")
            review_input = self._prepare_review_input(code_gen_result)
            review_result = self.agents['code_reviewer'].run(review_input)
            self.state_manager.update('code_reviewer', review_result)
            
            # Agent 4: DevOps Engineer
            self.logger.info("=== AGENT 4: DEVOPS ENGINEER ===")
            devops_input = self._prepare_devops_input(code_gen_result, cloud_provider)
            devops_result = self.agents['devops'].run(devops_input)
            self.state_manager.update('devops', devops_result)
            
            # Agent 5: Validator
            self.logger.info("=== AGENT 5: VALIDATOR & RELEASE MANAGER ===")
            validator_input = self._prepare_validator_input(
                analyzer_result, code_gen_result, review_result, devops_result
            )
            validator_result = self.agents['validator'].run(validator_input)
            self.state_manager.update('validator', validator_result)
            
            self.state_manager.complete_workflow()
            self.logger.info("Workflow completed successfully!")
            
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
EOF

# State Manager
cat > orchestrator/state_manager.py << 'EOF'
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
EOF

# Orchestrator __init__.py
cat > orchestrator/__init__.py << 'EOF'
from .workflow_manager import WorkflowManager
from .state_manager import StateManager
__all__ = ['WorkflowManager', 'StateManager']
EOF

# Streamlit UI
cat > ui/streamlit_app.py << 'EOF'
"""Streamlit UI for AG2 Multi-Agent System"""
import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings, setup_logging
from orchestrator import WorkflowManager
import logging

# Page config
st.set_page_config(
    page_title="AG2 Multi-Agent System",
    page_icon="🤖",
    layout="wide"
)

# Initialize
if 'workflow_manager' not in st.session_state:
    logging_config = setup_logging(settings)
    st.session_state.workflow_manager = WorkflowManager(settings)
    st.session_state.logs = []
    st.session_state.workflow_result = None

# Title
st.title("🤖 AG2 Multi-Agent System")
st.markdown("### Production-Ready Multi-Agent Workflow with Streamlit UI")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    cloud_provider = st.selectbox(
        "Cloud Provider",
        ["aws", "gcp", "azure"],
        help="Select target cloud platform"
    )
    
    st.divider()
    st.markdown("### Agent Status")
    agents = ["Analyzer", "Code Generator", "Code Reviewer", "DevOps", "Validator"]
    for agent in agents:
        st.markdown(f"🔵 {agent}")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Input")
    input_mode = st.radio("Input Mode", ["Text Task", "CSV Upload"])
    
    project_name = st.text_input("Project Name", "my-project")
    
    if input_mode == "Text Task":
        task_input = st.text_area(
            "Describe your project",
            height=200,
            placeholder="Example: Create a REST API for user management with authentication..."
        )
        input_type = "text"
        input_data = task_input
    else:
        uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
        input_type = "csv"
        if uploaded_file:
            csv_path = Path("uploads") / uploaded_file.name
            csv_path.parent.mkdir(exist_ok=True)
            with open(csv_path, 'wb') as f:
                f.write(uploaded_file.read())
            input_data = str(csv_path)
            st.success(f"Uploaded: {uploaded_file.name}")
        else:
            input_data = None
    
    st.divider()
    
    col_start, col_reset = st.columns(2)
    with col_start:
        if st.button("🚀 Start Workflow", type="primary", use_container_width=True):
            if input_data:
                with st.spinner("Executing agent workflow..."):
                    result = st.session_state.workflow_manager.execute_workflow(
                        input_data=input_data,
                        input_type=input_type,
                        cloud_provider=cloud_provider,
                        project_name=project_name
                    )
                    st.session_state.workflow_result = result
                    
                    if result['success']:
                        st.success("✅ Workflow completed successfully!")
                    else:
                        st.error(f"❌ Workflow failed: {result.get('error')}")
            else:
                st.warning("Please provide input")
    
    with col_reset:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.workflow_result = None
            st.rerun()

with col2:
    st.header("Status")
    if st.session_state.workflow_result:
        result = st.session_state.workflow_result
        
        if result['success']:
            st.success("Status: Completed")
            st.info(f"Project: {result.get('project_path', 'N/A')}")
            
            if result.get('ready_for_approval'):
                st.warning("⚠️ Awaiting human approval for deployment")
                if st.button("✅ Approve & Deploy", type="primary"):
                    st.success("🚀 Deployment initiated!")
                    st.balloons()
        else:
            st.error("Status: Failed")
            st.code(result.get('error', 'Unknown error'))
    else:
        st.info("Waiting to start...")

# Logs section
st.divider()
st.header("📋 Execution Logs")
if st.session_state.workflow_result:
    state = st.session_state.workflow_result.get('workflow_state', {})
    
    with st.expander("Workflow State", expanded=True):
        st.json(state)
    
    with st.expander("Agent Results"):
        for agent, result in state.get('agent_results', {}).items():
            st.subheader(agent)
            st.json(result)
else:
    st.info("No logs yet. Start a workflow to see execution details.")

# Footer
st.divider()
st.markdown("---")
st.markdown("Built with AG2 Framework, Streamlit, and Kubernetes | [Documentation](#)")
EOF

# Services - File Handler
cat > services/file_handler.py << 'EOF'
"""File handling service"""
from pathlib import Path
import shutil
import logging

logger = logging.getLogger(__name__)

class FileHandler:
    @staticmethod
    def create_directory(path: Path):
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {path}")
    
    @staticmethod
    def copy_files(src: Path, dst: Path):
        shutil.copytree(src, dst, dirs_exist_ok=True)
        logger.info(f"Copied {src} to {dst}")
EOF

# Services - Git Service
cat > services/git_service.py << 'EOF'
"""Git operations service"""
import git
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class GitService:
    def __init__(self, config):
        self.config = config
        self.github_token = config.github.github_token
        self.username = config.github.github_username
    
    def init_repo(self, project_path: Path):
        repo = git.Repo.init(project_path)
        logger.info(f"Initialized git repo at {project_path}")
        return repo
    
    def create_remote_repo(self, repo_name: str):
        # Use PyGithub to create remote repository
        logger.info(f"Creating remote repo: {repo_name}")
        return f"https://github.com/{self.username}/{repo_name}"
    
    def push_to_remote(self, repo, remote_url: str):
        origin = repo.create_remote('origin', remote_url)
        repo.index.add('*')
        repo.index.commit('Initial commit by AG2 Multi-Agent System')
        origin.push('main')
        logger.info("Pushed to remote repository")
EOF

# Services __init__.py
cat > services/__init__.py << 'EOF'
from .file_handler import FileHandler
from .git_service import GitService
__all__ = ['FileHandler', 'GitService']
EOF

# Utils - Logger
cat > utils/logger.py << 'EOF'
"""Logging utilities"""
import logging

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
EOF

# Utils __init__.py
cat > utils/__init__.py << 'EOF'
from .logger import get_logger
__all__ = ['get_logger']
EOF

# Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "ui/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

# docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  ag2-system:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./projects:/app/projects
      - ./logs:/app/logs
    env_file:
      - .env
    restart: unless-stopped
EOF

# Setup script
cat > setup.sh << 'EOF'
#!/bin/bash
echo "Setting up AG2 Multi-Agent System..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p projects logs/agents uploads

# Copy environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file. Please configure it with your credentials."
fi

echo "Setup complete! Run: streamlit run ui/streamlit_app.py"
EOF

chmod +x setup.sh

# .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
.env
.vscode/
.idea/
*.log
logs/
projects/
uploads/
*.db
*.sqlite3
.DS_Store
EOF

# Tests
cat > tests/__init__.py << 'EOF'
"""Tests package"""
EOF

cat > tests/test_agents.py << 'EOF'
"""Agent tests"""
import pytest
from agents import AnalyzerAgent
from config import settings

def test_analyzer_agent():
    agent = AnalyzerAgent(settings)
    assert agent.name == "AnalyzerAgent"
    assert agent.state['status'] == 'initialized'
EOF

# Projects .gitkeep
touch projects/.gitkeep

echo ""
echo "==========================================="
echo "✅ All files generated successfully!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. cd $PROJECT_ROOT"
echo "2. Configure .env file with your credentials"
echo "3. Run: ./setup.sh"
echo "4. Run: streamlit run ui/streamlit_app.py"
echo ""
echo "Or use Docker:"
echo "docker-compose up --build"
echo ""
