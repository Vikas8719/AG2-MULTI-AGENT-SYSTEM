# AG2 Multi-Agent System with Streamlit UI

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      STREAMLIT UI LAYER                         │
│  (CSV Upload | Text Input | Cloud Config | Real-time Logs)     │
└────────────────────────┬────────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────────┐
│                   AG2 ORCHESTRATION LAYER                       │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   AGENT 1    │  │   AGENT 2    │  │   AGENT 3    │         │
│  │   ANALYZER   │─▶│     CODE     │─▶│   REVIEWER   │         │
│  │   & PLANNER  │  │  GENERATOR   │  │              │         │
│  └──────────────┘  └──────────────┘  └──────┬───────┘         │
│                                              │                  │
│  ┌──────────────┐  ┌──────────────┐        │                  │
│  │   AGENT 5    │◀─│   AGENT 4    │◀───────┘                  │
│  │  VALIDATOR   │  │   DEVOPS     │                            │
│  │  & RELEASE   │  │   ENGINEER   │                            │
│  └──────┬───────┘  └──────────────┘                            │
│         │                                                       │
└─────────┼───────────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────────────┐
│              HUMAN-IN-THE-LOOP APPROVAL GATE                    │
└─────────┬───────────────────────────────────────────────────────┘
          │
┌─────────▼───────────────────────────────────────────────────────┐
│           DEPLOYMENT PIPELINE (GitHub + K8s)                    │
│  Git Init → Commit → Push → CI/CD → Deploy → Monitor           │
└─────────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
ag2-multi-agent-system/
├── README.md
├── requirements.txt
├── .env.example
├── setup.sh
├── Dockerfile
├── docker-compose.yml
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── logging_config.py
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── analyzer_agent.py
│   ├── code_generator_agent.py
│   ├── code_reviewer_agent.py
│   ├── devops_agent.py
│   └── validator_agent.py
├── orchestrator/
│   ├── __init__.py
│   ├── workflow_manager.py
│   └── state_manager.py
├── services/
│   ├── __init__.py
│   ├── file_handler.py
│   ├── git_service.py
│   └── deployment_service.py
├── ui/
│   ├── __init__.py
│   ├── streamlit_app.py
│   └── components.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── validators.py
├── templates/
│   ├── dockerfile.j2
│   ├── github_actions.j2
│   ├── k8s_deployment.j2
│   └── terraform.j2
├── projects/
│   └── .gitkeep
└── tests/
    ├── __init__.py
    ├── test_agents.py
    └── test_workflow.py
```

## 🚀 Features

- **5-Agent Collaborative Workflow**: Specialized agents for analysis, coding, review, DevOps, and validation
- **Multi-Input Support**: CSV data or plain text tasks
- **Human-in-the-Loop**: Approval gates before deployment
- **Real-time Monitoring**: Live agent execution logs in Streamlit UI
- **Cloud Agnostic**: Support for AWS, GCP, and Azure
- **Full CI/CD Pipeline**: Automated GitHub Actions workflows
- **Kubernetes Ready**: Complete K8s manifests and Helm charts
- **Production Grade**: Error handling, logging, security, and scalability

## 📋 Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Git
- GitHub Account with Personal Access Token
- Kubernetes cluster (for deployment)
- Cloud provider CLI (AWS/GCP/Azure)

## 🔧 Installation

1. **Clone Repository**
```bash
git clone <your-repo>
cd ag2-multi-agent-system
```

2. **Setup Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Run Setup Script**
```bash
chmod +x setup.sh
./setup.sh
```

## 🎯 Quick Start

### Running with Streamlit

```bash
streamlit run ui/streamlit_app.py
```

### Running with Docker

```bash
docker-compose up --build
```

## 📖 Usage Guide

### 1. CSV Input Mode

1. Upload CSV file with project requirements
2. Select cloud provider (AWS/GCP/Azure)
3. Click "Start Agent Workflow"
4. Monitor real-time agent logs
5. Review generated artifacts
6. Approve deployment

### 2. Text Task Mode

1. Enter task description in text area
2. Configure deployment settings
3. Start workflow
4. Review and approve

### 3. Agent Workflow

**AGENT 1: Analyzer & Planner**
- Analyzes input data/task
- Creates project architecture
- Generates folder structure
- Defines tech stack

**AGENT 2: Code Generator**
- Creates working code
- Follows best practices
- Adds logging & error handling
- Generates configs

**AGENT 3: Code Reviewer**
- Reviews codebase
- Identifies issues
- Refactors code
- Ensures quality

**AGENT 4: DevOps Engineer**
- Creates Dockerfile
- Sets up CI/CD
- Generates K8s manifests
- Configures cloud resources

**AGENT 5: Validator & Release Manager**
- Cross-checks everything
- Requests human approval
- Pushes to GitHub
- Triggers deployment

## 🔐 Environment Variables

```env
# AG2 Configuration
OPENAI_API_KEY=your_openai_api_key
AG2_MODEL=gpt-4-turbo-preview

# GitHub Configuration
GITHUB_TOKEN=your_github_pat
GITHUB_USERNAME=your_username
GITHUB_REPO_PREFIX=ag2-generated

# Cloud Provider (aws/gcp/azure)
CLOUD_PROVIDER=aws
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=us-east-1

# Kubernetes
KUBECONFIG_PATH=/path/to/kubeconfig
K8S_NAMESPACE=default

# Deployment
DOCKER_REGISTRY=docker.io
DOCKER_USERNAME=your_docker_username

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_agents.py -v

# With coverage
pytest --cov=. tests/
```

## 📊 Monitoring & Logging

Logs are stored in:
- Console output (real-time in Streamlit)
- File: `logs/app.log`
- Agent-specific logs: `logs/agents/`

## 🔄 CI/CD Pipeline

Automatically generated for each project:

1. **GitHub Actions Workflow**
   - Lint & Test
   - Build Docker image
   - Push to registry
   - Deploy to K8s

2. **ArgoCD Integration**
   - GitOps deployment
   - Auto-sync enabled
   - Health monitoring

## 🐳 Docker Deployment

```bash
# Build image
docker build -t ag2-multi-agent:latest .

# Run container
docker run -p 8501:8501 \
  --env-file .env \
  ag2-multi-agent:latest
```

## ☸️ Kubernetes Deployment

```bash
# Apply manifests
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Check status
kubectl get pods -n ag2-system
kubectl logs -f <pod-name> -n ag2-system
```

## 🛠️ Troubleshooting

### Common Issues

1. **AG2 Import Error**
```bash
pip install pyautogen
```

2. **GitHub Push Failed**
- Verify GitHub token has repo permissions
- Check repository exists and is accessible

3. **Kubernetes Connection Failed**
- Verify kubeconfig is correct
- Check cluster connectivity: `kubectl cluster-info`

## 📚 API Reference

### Workflow Manager

```python
from orchestrator.workflow_manager import WorkflowManager

manager = WorkflowManager()
result = manager.execute_workflow(
    input_data="Create a REST API",
    input_type="text",
    cloud_provider="aws"
)
```

### State Manager

```python
from orchestrator.state_manager import StateManager

state = StateManager()
state.update("agent_1", "completed", {"output": "..."})
current_state = state.get_current_state()
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file

## 🔗 Resources

- [AG2 Documentation](https://microsoft.github.io/autogen/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Kubernetes Docs](https://kubernetes.io/docs/)

## 📧 Support

For issues and questions:
- GitHub Issues: [Create Issue]
- Email: support@example.com

---

**Built with ❤️ using AG2, Streamlit, and Kubernetes**
