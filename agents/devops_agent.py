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
