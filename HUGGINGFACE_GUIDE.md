# 🤗 Hugging Face API Integration Guide - AG2 Multi-Agent System

## ✅ Successfully Configured!

Aapka project ab Hugging Face API use kar sakta hai! Yeh OpenAI se **FREE ya bahut sasta** alternative hai.

---

## 🆕 What's New

Maine aapke project mein ye changes kiye hain:

### **1. Configuration Files Updated:**
- ✅ `config/settings.py` - LLM provider selection added
- ✅ `agents/base_agent.py` - Multi-provider support
- ✅ `utils/huggingface_helper.py` - HuggingFace API client **(NEW)**
- ✅ `.streamlit/secrets.toml` - HuggingFace configuration

---

## 🚀 How to Use Hugging Face API

### **Step 1: Get FREE HuggingFace API Key**

1. Visit: **https://huggingface.co/settings/tokens**
2. Login/Signup (free!)
3. Click "New token"
4. Name: "AG2-Multi-Agent"
5. Type: "Read"
6. Copy your token: `hf_xxxxxxxxxxxxx`

### **Step 2: Configure Secrets**

Edit `.streamlit/secrets.toml`:

```toml
# Choose Hugging Face as provider
LLM_PROVIDER = "huggingface"

# Add your HF API key
HUGGINGFACE_API_KEY = "hf_your_real_key_here"

# Choose model (ye default hai, best hai)
HUGGINGFACE_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
```

### **Step 3: Test Locally**

```powershell
# Run the app
streamlit run app.py
```

---

## 📊 Recommended Models

Maine aapke liye best models ki list ready kar di hai:

### **FREE Models (Recommended):**

| Model | Best For | Speed | Quality |
|-------|----------|-------|---------|
| `mistralai/Mixtral-8x7B-Instruct-v0.1` | **General Purpose** ⭐ | Fast | Excellent |
| `mistralai/Mistral-7B-Instruct-v0.2` | Quick Tasks | Very Fast | Good |
| `codellama/CodeLlama-34b-Instruct-hf` | **Code Generation** | Medium | Excellent |
| `meta-llama/Llama-2-70b-chat-hf` | Complex Tasks | Slow | Excellent |

### **Serverless (Super Fast & Free):**

| Model | Best For |
|-------|----------|
| `microsoft/Phi-3-mini-4k-instruct` | Quick responses |
| `HuggingFaceH4/zephyr-7b-beta` | Chat applications |
| `google/flan-t5-xxl` | Q&A tasks |

### **Pro Models (HuggingFace Pro Required):**

| Model | Cost |
|-------|------|
| `meta-llama/Meta-Llama-3-70B-Instruct` | $9/month |
| `mistralai/Mistral-Large-Instruct-2411` | $9/month |

**Pro tip:** Free models are more than enough for most use cases!

---

## 🎯 Model Selection Guide

### **Change Model in secrets.toml:**

```toml
# For Code Generation (Best for DevOps agent):
HUGGINGFACE_MODEL = "codellama/CodeLlama-34b-Instruct-hf"

# For Fast Responses (Best for quick testing):
HUGGINGFACE_MODEL = "microsoft/Phi-3-mini-4k-instruct"

# For Complex Analysis (Best for Analyzer agent):
HUGGINGFACE_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # DEFAULT

# For Maximum Quality (Slower but best results):
HUGGINGFACE_MODEL = "meta-llama/Llama-2-70b-chat-hf"
```

---

## 💰 Cost Comparison

### **Hugging Face vs OpenAI:**

| Feature | Hugging Face (FREE) | OpenAI (PAID) |
|---------|---------------------|---------------|
| **API Key** | ✅ Free | ❌ Paid only |
| **Cost per 1M tokens** | ✅ $0 (free tier) | ❌ $10-$60 |
| **Rate Limits** | Moderate | High |
| **Model Quality** | Excellent | Excellent |
| **Best Model** | Mixtral-8x7B | GPT-4 Turbo |

**Result:** Hugging Face is **MUCH CHEAPER** for development and testing!

---

## 🔧 Advanced Configuration

### **Custom Inference Endpoint:**

Agar aap apna own endpoint use karna chahte ho:

```toml
# In secrets.toml
HUGGINGFACE_ENDPOINT = "https://your-custom-endpoint.huggingface.cloud"
```

### **Multiple Provider Support:**

Aap easily switch kar sakte ho providers ke beech:

```toml
# Use OpenAI
LLM_PROVIDER = "openai"

# Use HuggingFace  
LLM_PROVIDER = "huggingface"

# Use Anthropic
LLM_PROVIDER = "anthropic"
```

---

## 📝 Code Examples

### **Using HuggingFace Helper:**

```python
from utils.huggingface_helper import HuggingFaceClient

# Initialize client
hf_client = HuggingFaceClient(
    api_key="hf_your_key",
    model="mistralai/Mixtral-8x7B-Instruct-v0.1"
)

# Generate text
response = hf_client.generate(
    prompt="Write a Python function to sort a list",
    max_tokens=500,
    temperature=0.7
)

print(response['text'])
```

### **Chat Format:**

```python
# Chat completion
messages = [
    {"role": "system", "content": "You are a helpful AI assistant"},
    {"role": "user", "content": "Explain async/await in Python"}
]

response = hf_client.chat(messages)
print(response['text'])
```

---

## ⚠️ Important Notes

### **Rate Limits:**

- **Free Tier:** ~1000 requests/day
- **Pro Tier:** ~100,000 requests/day
- **Enterprise:** Unlimited

### **Model Loading:**

Pehli request slow ho sakti hai (model loading time). Helper automatically handle karega:

```python
# Automatically retries and waits for model loading
response = hf_client.generate(prompt, retry_count=3)
```

### **Error Handling:**

```python
response = hf_client.generate(prompt)

if response['success']:
    print(response['text'])
else:
    print(f"Error: {response.get('error')}")
```

---

## 🐛 Troubleshooting

### **Problem 1: "Model is loading"**

**Solution:** Wait karo, automatically retry hoga. Ya faster model use karo:
```toml
HUGGINGFACE_MODEL = "microsoft/Phi-3-mini-4k-instruct"
```

### **Problem 2: "Invalid API Key"**

**Solution:**
1. Check key format: `hf_xxxxxxxxxxxxx`
2. Verify at: https://huggingface.co/settings/tokens
3. Make sure "Read" permission hai

### **Problem 3: "Rate limit exceeded"**

**Solution:**
- Wait for 1 hour, ya
- Upgrade to HuggingFace Pro ($9/month)

### **Problem 4: "Timeout"**

**Solution:**
```python
# Increase timeout
response = hf_client.generate(prompt, timeout=600)  # 10 minutes
```

---

## 📋 Deployment Checklist

### **For Streamlit Cloud:**

- [ ] HuggingFace API key copied
- [ ] `.streamlit/secrets.toml` updated with HF key
- [ ] `LLM_PROVIDER = "huggingface"` set
- [ ] Model selected (recommend Mixtral-8x7B)
- [ ] Tested locally
- [ ] Secrets added to Streamlit Cloud dashboard

---

## 🎉 Benefits of Using Hugging Face

1. ✅ **FREE** for most use cases
2. ✅ **Open Source** models
3. ✅ **Privacy** - can self-host
4. ✅ **Variety** - 100+ models to choose from
5. ✅ **Community** - Active support
6. ✅ **No Credit Card** required for free tier

---

## 🔄 Switching Back to OpenAI

Agar kabhi OpenAI use karna ho:

```toml
# In secrets.toml
LLM_PROVIDER = "openai"
OPENAI_API_KEY = "sk-your-key"
```

That's it! Configuration automatically switch ho jayega.

---

## 📚 Additional Resources

- **HuggingFace Docs:** https://huggingface.co/docs/api-inference/
- **Model Hub:** https://huggingface.co/models
- **Pricing:** https://huggingface.co/pricing
- **API Reference:** https://huggingface.co/docs/huggingface_hub/package_reference/inference_client

---

## 💡 Pro Tips

1. **Start with Mixtral-8x7B** - Best balance of speed and quality
2. **Use Code Llama** for code generation tasks
3. **Enable caching** in Streamlit for faster responses
4. **Monitor usage** on HuggingFace dashboard
5. **Test different models** to find best fit for your use case

---

## ✅ Quick Start Command

```powershell
# 1. Set your HF API key in .streamlit/secrets.toml
# 2. Run:
streamlit run app.py
```

---

**Enjoy FREE AI-powered agents! 🎉**

**Questions?** Check the HuggingFace documentation or ask in the community forum!

---

*Guide created: 2026-02-14*  
*Status: ✅ Ready to use*
