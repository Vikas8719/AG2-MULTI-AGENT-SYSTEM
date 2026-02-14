# 🚀 Quick Deployment Reference - AG2 Multi-Agent System

## ⚡ 5-Minute Deployment Guide

### **Step 1: Configure Secrets** (2 min)

Edit `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-your-real-key-here"
GITHUB_TOKEN = "ghp_your-real-token-here"
GITHUB_USERNAME = "your-actual-username"
```

### **Step 2: Test Locally** (1 min)

```powershell
# Activate venv (if not activated)
venv\Scripts\activate

# Run app
streamlit run app.py
```

Visit: http://localhost:8501

### **Step 3: Push to GitHub** (1 min)

```powershell
git init
git add .
git commit -m "Ready for deployment"
git remote add origin https://github.com/YOUR-USERNAME/ag2-multi-agent-system.git
git push -u origin main
```

### **Step 4: Deploy on Streamlit Cloud** (1 min)

1. Go to: https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `YOUR-USERNAME/ag2-multi-agent-system`
5. Main file: `app.py`
6. Click "Deploy"

### **Step 5: Add Secrets in Cloud** (30 sec)

1. Go to app settings → Secrets
2. Copy-paste content from `.streamlit/secrets.toml`
3. Replace with your actual keys
4. Save

**Done! 🎉**

---

## 📁 Files Created for You

| File | Purpose | Action Required |
|------|---------|-----------------|
| `app.py` | Entry point | ✅ None - Ready |
| `.streamlit/config.toml` | Config | ✅ None - Ready |
| `.streamlit/secrets.toml` | Secrets template | ⚠️ **ADD YOUR KEYS** |
| `.gitignore` | Git ignore | ✅ None - Ready |
| `runtime.txt` | Python version | ✅ None - Ready |
| `packages.txt` | System deps | ✅ None - Ready |

---

## 🔑 Required API Keys

You need these before deployment:

1. **OpenAI API Key**
   - Get from: https://platform.openai.com/api-keys
   - Format: `sk-proj-xxxx`

2. **GitHub Personal Access Token**
   - Get from: https://github.com/settings/tokens
   - Permissions: `repo`, `workflow`
   - Format: `ghp_xxxx`

3. **Cloud Provider Credentials** (Optional for testing)
   - AWS/GCP/Azure credentials
   - Only needed if using deployment features

---

## ⚠️ Important Warnings

1. **NEVER** commit `.streamlit/secrets.toml` with real keys
2. **ALWAYS** use `.gitignore` (already added)
3. **TEST** locally before deploying to cloud
4. **CHECK** logs after deployment for errors

---

## 🐛 Quick Troubleshooting

### Problem: "ModuleNotFoundError"
**Solution:** Check `requirements.txt` has all dependencies

### Problem: "Secrets not found"
**Solution:** Add secrets in Streamlit Cloud dashboard (Settings → Secrets)

### Problem: "App won't load"
**Solution:** Check logs in Streamlit Cloud dashboard

### Problem: "Import error from config"
**Solution:** Ensure all `__init__.py` files exist in folders

---

## 📞 Quick Commands

```powershell
# Run locally
streamlit run app.py

# Run on custom port
streamlit run app.py --server.port 8502

# Clear cache
streamlit cache clear

# Check version
streamlit --version

# Install/update requirements
pip install -r requirements.txt
```

---

## 🎯 Next Steps After Deployment

1. ✅ Test all features on deployed app
2. ✅ Monitor logs for errors
3. ✅ Share URL with team/users
4. ✅ Setup custom domain (optional)
5. ✅ Monitor usage in Streamlit dashboard

---

## 📊 Expected Result

After deployment, you'll get a URL like:
```
https://your-app-name.streamlit.app
```

Your app will have:
- ✅ AG2 Multi-Agent interface
- ✅ Text/CSV input modes
- ✅ Cloud provider selection
- ✅ Real-time workflow execution
- ✅ Agent status monitoring
- ✅ Human approval workflow

---

## 💪 Pro Tips

1. **First deployment takes 5-10 minutes** - Be patient!
2. **Updates are automatic** - Just push to GitHub
3. **Free tier is limited** - Monitor usage
4. **Use caching** - Improves performance
5. **Check logs regularly** - Catch errors early

---

**Ready to deploy? Follow Step 1! 🚀**

For detailed guide, see: `STREAMLIT_DEPLOYMENT.md`  
For full review, see: `CODE_REVIEW_SUMMARY.md`
