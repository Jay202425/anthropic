# Deploy to Streamlit Cloud

## Quick Deployment Steps

### 1. **Streamlit Cloud Setup**

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Connect your GitHub repository: `https://github.com/Jay202425/anthropic`
4. Select:
   - **Repository**: Jay202425/anthropic
   - **Branch**: main
   - **Main file path**: streamlit_app.py

### 2. **Set API Key Secret**

After deployment, add your API key as a secret:

1. Go to your app settings (⚙️ in the top right)
2. Click "Secrets"
3. Add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-your-actual-key-here"
   ```

### 3. **Verify Deployment**

Once deployed, your app will be available at your custom URL.

## File Structure

```
anthropic/
├── streamlit_app.py           # ← Main app file (Streamlit)
├── financial_analyzer.py      # Analysis engine
├── app.py                     # Flask version (optional)
├── requirements.txt           # Python dependencies
├── .streamlit/
│   └── config.toml           # Streamlit config
├── templates/
│   └── index.html            # Flask HTML (optional)
├── .gitignore                # Git ignore rules
└── README.md                 # Documentation
```

## Local Testing

Before deploying, test locally:

```bash
cd c:\Users\Administrator\Anthropic

# Set API key
$env:ANTHROPIC_API_KEY="sk-ant-your-key"

# Run Streamlit
streamlit run streamlit_app.py
```

Open: `http://localhost:8501`

## Environment Variables

For Streamlit Cloud, use **Secrets** instead of `.env`:

1. Click "Manage app" → "Secrets"
2. Add:
   ```
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```

## Troubleshooting

### App Crashes
- Check logs in Streamlit Cloud dashboard
- Verify API key is set in Secrets
- Check Python version compatibility

### ModuleNotFoundError
- Ensure `requirements.txt` is in root directory
- Verify all imports are listed

### API Key Error
- Use Streamlit Secrets, NOT .env
- Key must be in format: `ANTHROPIC_API_KEY = "sk-ant-..."`

## Features

✅ Beautiful responsive interface
✅ Real-time financial analysis
✅ Instant risk assessment
✅ AI-powered recommendations
✅ Download reports
✅ Mobile-friendly

## Security Notes

- ✅ API key stored in Streamlit Secrets (encrypted)
- ✅ .env file with secrets is gitignored
- ✅ No sensitive data in repository
- ✅ Only placeholder in .env.example

## Support

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Cloud: https://streamlit.io/cloud
- Anthropic Docs: https://docs.anthropic.com

---

**Your Streamlit app is ready to deploy! 🚀**
