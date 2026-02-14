# AG2 Multi-Agent System - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.9+
- Docker (optional)
- OpenAI API Key
- GitHub Personal Access Token

---

## Step 1: Installation

```bash
# Clone or download the project
cd ag2-multi-agent-system

# Run setup script
chmod +x setup.sh
./setup.sh
```

---

## Step 2: Configuration

Edit `.env` file with your credentials:

```bash
# Minimum required configuration
OPENAI_API_KEY=sk-your-openai-key-here
GITHUB_TOKEN=ghp_your-github-token
GITHUB_USERNAME=your-username
CLOUD_PROVIDER=aws
```

---

## Step 3: Run the Application

### Option A: Direct Python
```bash
source venv/bin/activate
streamlit run ui/streamlit_app.py
```

### Option B: Docker
```bash
docker-compose up -d
```

Access the UI at: **http://localhost:8501**

---

## Step 4: Create Your First Project

1. **Select Input Mode**
   - Text Task: Describe your project in plain English
   - CSV Upload: Upload structured data

2. **Enter Project Details**
   ```
   Example: "Create a REST API for a todo list application 
   with user authentication, CRUD operations, and PostgreSQL 
   database"
   ```

3. **Configure Settings**
   - Project Name: `my-todo-api`
   - Cloud Provider: `aws` / `gcp` / `azure`

4. **Start Workflow**
   - Click "🚀 Start Workflow"
   - Watch real-time agent execution
   - Monitor logs in the UI

5. **Review & Approve**
   - Review generated code and infrastructure
   - Click "✅ Approve & Deploy"
   - System pushes to GitHub and triggers CI/CD

---

## 🎯 Example Workflows

### Example 1: REST API
**Input**: "Create a FastAPI REST API for user management with JWT authentication"

**Output**:
- ✅ Complete FastAPI application
- ✅ JWT authentication
- ✅ PostgreSQL database integration
- ✅ Docker configuration
- ✅ Kubernetes manifests
- ✅ CI/CD pipeline
- ✅ Documentation

### Example 2: ML Application
**Input**: CSV with housing prices data

**Output**:
- ✅ Data analysis notebook
- ✅ ML model training pipeline
- ✅ Prediction API
- ✅ MLflow integration
- ✅ Model deployment
- ✅ Monitoring dashboard

### Example 3: Web Application
**Input**: "Build a blog platform with user posts, comments, and likes"

**Output**:
- ✅ Backend API (FastAPI/Flask)
- ✅ Frontend (React/Vue)
- ✅ Database schema
- ✅ Authentication system
- ✅ Full deployment stack

---

## 📊 Understanding the Workflow

### The 5 Agents

```
1. ANALYZER → Analyzes requirements, creates project plan
2. CODE GENERATOR → Writes production-ready code
3. CODE REVIEWER → Reviews and improves code quality
4. DEVOPS ENGINEER → Creates deployment infrastructure
5. VALIDATOR → Final checks and deployment
```

### Execution Flow

```
Input → Agent 1 → Agent 2 → Agent 3 → Agent 4 → Agent 5
  ↓         ↓         ↓         ↓         ↓         ↓
 CSV/    Project   Working   Reviewed  Infra    Human
 Text     Plan      Code      Code      Ready   Approval
                                                    ↓
                                              Deployment
```

---

## 🎨 UI Guide

### Main Dashboard
- **Left Panel**: Configuration and settings
- **Center**: Input area and workflow controls
- **Right Panel**: Status and logs
- **Bottom**: Detailed execution logs

### Real-time Monitoring
- ✅ Agent execution progress
- 📝 Live log streaming
- 🔄 Workflow state visualization
- ⚠️ Error notifications

---

## 🔧 Common Use Cases

### 1. Quick Prototype
```
Input: "Create a URL shortener service"
Time: ~5 minutes
Output: Production-ready URL shortener with API
```

### 2. Data Analysis
```
Input: Upload sales_data.csv
Time: ~10 minutes
Output: Analysis report + visualization dashboard
```

### 3. Microservice
```
Input: "Create a payment processing microservice"
Time: ~15 minutes
Output: Complete microservice with K8s deployment
```

---

## 🐛 Troubleshooting

### Issue: "OpenAI API Error"
**Solution**: Check your API key in `.env` file

### Issue: "GitHub Push Failed"
**Solution**: Verify GitHub token has `repo` permissions

### Issue: "Port 8501 already in use"
**Solution**: 
```bash
# Find and kill process
lsof -ti:8501 | xargs kill -9
# Or use different port
streamlit run ui/streamlit_app.py --server.port=8502
```

---

## 📚 Next Steps

1. **Read Full Documentation**
   - [README.md](README.md) - Overview
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide

2. **Explore Examples**
   - Check `projects/` folder for generated projects
   - Review agent logs in `logs/agents/`

3. **Customize**
   - Modify agent prompts in `agents/`
   - Add custom templates in `templates/`
   - Extend workflow in `orchestrator/`

4. **Deploy to Production**
   - Follow [DEPLOYMENT.md](DEPLOYMENT.md)
   - Setup monitoring
   - Configure autoscaling

---

## 🤝 Getting Help

- **Documentation**: Read full docs in this folder
- **Logs**: Check `logs/` directory
- **GitHub Issues**: Report bugs or request features
- **Community**: Join our Discord/Slack

---

## ⚡ Pro Tips

1. **Use Specific Descriptions**: More detail = better results
2. **Start Simple**: Test with small projects first
3. **Review Output**: Always review before deploying
4. **Monitor Costs**: Watch cloud resource usage
5. **Version Control**: Keep track of generated projects

---

## 🎯 Success Checklist

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`./setup.sh`)
- [ ] `.env` configured with API keys
- [ ] Can access Streamlit UI (http://localhost:8501)
- [ ] Successfully ran test workflow
- [ ] Reviewed generated project
- [ ] Approved and deployed

---

## 🚦 What's Next?

Now that you're set up:
1. Try the example workflows above
2. Create your own custom project
3. Explore the agent capabilities
4. Deploy to your cloud provider
5. Monitor and iterate

**Welcome to AI-Powered Development! 🎉**

---

**Quick Start Guide v1.0**
**Last Updated: 2024**
