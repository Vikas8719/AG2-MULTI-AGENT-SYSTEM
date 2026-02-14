# 🚀 Streamlit Cloud Deployment Guide - AG2 Multi-Agent System

## ✅ Files Created/Fixed for Deployment

Maine aapke project mein ye files create/fix ki hain:

1. ✓ `.streamlit/config.toml` - Streamlit configuration
2. ✓ `.streamlit/secrets.toml` - Secrets template (configure karna hoga)
3. ✓ `app.py` - Main entry point for deployment
4. ✓ `.gitignore` - Git ke liye sensitive files exclude karne ke liye
5. ✓ `runtime.txt` - Python version specification (3.11.7)
6. ✓ `packages.txt` - System-level dependencies

---

## 📋 Pre-Deployment Checklist

### ✅ **Step 1: Environment Configuration**

**Important:** `.streamlit/secrets.toml` file mein apni actual credentials daaliye:

```toml
OPENAI_API_KEY = "sk-your-actual-key"
GITHUB_TOKEN = "ghp_your-actual-token"
GITHUB_USERNAME = "your-username"
# ... aur bhi values
```

⚠️ **Warning:** `secrets.toml` file ko Git mein commit NAHI karna hai! Already .gitignore mein add hai.

### ✅ **Step 2: Test Local Deployment**

Pehle local machine par test karein:

```powershell
# Virtual environment activate karein
venv\Scripts\activate

# Dependencies install/update karein
pip install -r requirements.txt

# Streamlit app run karein
streamlit run app.py
```

Browser mein `http://localhost:8501` khulna chahiye.

### ✅ **Step 3: Git Repository Setup**

```powershell
# Git initialize karein (agar nahi hai)
git init

# Files add karein
git add .

# Commit karein
git commit -m "Initial commit for Streamlit deployment"

# GitHub repository banayein aur push karein
git remote add origin https://github.com/your-username/ag2-multi-agent-system.git
git branch -M main
git push -u origin main
```

---

## 🌐 Streamlit Cloud Deployment Steps

### **Method 1: Streamlit Community Cloud (FREE)**

1. **Streamlit Cloud Account Banayein:**
   - Visit: https://share.streamlit.io/
   - "Sign up" with GitHub account

2. **New App Deploy Karein:**
   - Click "New app"
   - Repository select karein: `your-username/ag2-multi-agent-system`
   - Main file path: `app.py`
   - Python version: 3.11 (automatically runtime.txt se detect hoga)

3. **Secrets Configure Karein:**
   - App settings mein jaayein
   - "Secrets" section mein `.streamlit/secrets.toml` ki content copy karein
   - Actual API keys daalein
   - Save karein

4. **Deploy Button Click Karein:**
   - App automatically build aur deploy hoga
   - 5-10 minutes lag sakta hai

5. **Access Your App:**
   - URL milega: `https://your-app-name.streamlit.app`

---

## 🔐 Important Security Notes

### **Secrets Management:**

Streamlit Cloud par secrets add karne ke liye:

1. Dashboard → Your App → Settings → Secrets
2. Ye format mein secrets add karein:

```toml
OPENAI_API_KEY = "sk-proj-xxxx"
GITHUB_TOKEN = "ghp_xxxx"
GITHUB_USERNAME = "your-username"
CLOUD_PROVIDER = "aws"
AWS_ACCESS_KEY_ID = "your-key"
AWS_SECRET_ACCESS_KEY = "your-secret"
```

3. **Never commit** `.streamlit/secrets.toml` to Git!

---

## 🛠️ Troubleshooting Common Issues

### **Issue 1: Import Errors**

**Problem:** `ModuleNotFoundError` errors

**Solution:**
```powershell
# requirements.txt ko verify karein
# Sabhi dependencies listed honi chahiye
pip freeze > requirements.txt
```

### **Issue 2: Build Fails**

**Problem:** Deployment build fail ho raha hai

**Solutions:**
- Check `requirements.txt` - sabhi versions compatible hain?
- Check `runtime.txt` - Python version supported hai?
- Streamlit Cloud logs check karein

### **Issue 3: Config Import Error**

**Problem:** `from config import settings` fail ho raha hai

**Solution:** 
- Verify ki `config/__init__.py` proper exports kar raha hai
- Check path issues in imports

### **Issue 4: Secrets Not Found**

**Problem:** App runs but secrets not accessible

**Solution:**
```python
# streamlit_app.py mein, secrets access karne ka sahi tarika:
import streamlit as st

# Access secrets
api_key = st.secrets["OPENAI_API_KEY"]
github_token = st.secrets["GITHUB_TOKEN"]
```

---

## 📊 Monitoring & Updates

### **View Logs:**
- Streamlit Cloud Dashboard → Your App → Logs
- Real-time logs dekh sakte hain

### **Update Deployed App:**
```powershell
# Code changes karein
git add .
git commit -m "Update feature X"
git push origin main

# Streamlit Cloud automatically redeploy karega
```

### **Restart App:**
- Dashboard → Your App → Menu → Reboot app
- Ya settings → "Always rerun on save"

---

## 🎯 Deployment Configurations

### **Recommended Resource Settings:**

```toml
# .streamlit/config.toml (already created)
[server]
maxUploadSize = 200  # MB
maxMessageSize = 200  # MB
enableStaticServing = false

[browser]
serverAddress = "0.0.0.0"
gatherUsageStats = false

[runner]
fastReruns = true
```

---

## 🚀 Performance Optimization

### **1. Caching Strategy:**

```python
# streamlit_app.py mein add karein
import streamlit as st

@st.cache_data(ttl=3600)  # 1 hour cache
def load_workflow_manager():
    from orchestrator import WorkflowManager
    from config import settings
    return WorkflowManager(settings)

# Use cached version
workflow_manager = load_workflow_manager()
```

### **2. Lazy Loading:**

```python
# Heavy imports ko conditional load karein
if st.button("Start Workflow"):
    from orchestrator import WorkflowManager
    # ... execute workflow
```

---

## 📞 Support & Resources

### **Streamlit Documentation:**
- https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app
- https://docs.streamlit.io/library/advanced-features/secrets-management

### **Common Commands:**

```powershell
# Local testing
streamlit run app.py

# Check Streamlit version
streamlit --version

# Clear cache
streamlit cache clear

# Run with custom port
streamlit run app.py --server.port 8502
```

---

## 🎉 Final Checklist Before Deployment

- [ ] `.streamlit/secrets.toml` configured with real API keys (locally)
- [ ] Local testing successful (`streamlit run app.py`)
- [ ] Code committed to GitHub (WITHOUT secrets.toml)
- [ ] GitHub repository is public (for free tier) or private (with paid plan)
- [ ] Streamlit Cloud account created
- [ ] Secrets added in Streamlit Cloud dashboard
- [ ] App deployed successfully
- [ ] URL accessible and app working

---

## 🔄 Update Workflow

```powershell
# Development cycle:
1. Code changes karein locally
2. Test karein: streamlit run app.py
3. Commit karein: git commit -am "Your message"
4. Push karein: git push origin main
5. Streamlit Cloud automatically redeploy karega (2-3 minutes)
```

---

## 💡 Pro Tips

1. **Use Streamlit Session State** properly to avoid re-initialization
2. **Add @st.cache_data** for expensive operations
3. **Monitor Usage** in Streamlit Cloud dashboard
4. **Check Logs** regularly for errors
5. **Keep requirements.txt** minimal and updated

---

**Deployment Date:** 2026-02-14
**Status:** Ready for Deployment ✅

---

## 📧 Need Help?

- Streamlit Community Forum: https://discuss.streamlit.io/
- GitHub Issues: [Your Repository]
- Streamlit Docs: https://docs.streamlit.io/

---

**Happy Deploying! 🚀**
