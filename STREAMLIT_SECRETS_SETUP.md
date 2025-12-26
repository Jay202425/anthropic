# 🔑 Add API Key to Streamlit Cloud

## Quick Fix for "API Key Not Configured" Error

Your Streamlit app is deployed but needs the API key configured. Follow these steps:

### Step 1: Open App Settings
1. Go to your Streamlit app: https://anthropic-t4vcnfccrff77rwmkxubu.streamlit.app
2. Click the **⚙️ (gear icon)** in the top right
3. Select **Settings**

### Step 2: Add the Secret
1. Click **Secrets** in the left sidebar
2. Copy and paste this into the text area:

```
ANTHROPIC_API_KEY = "your-api-key-here"
```

3. Replace `your-api-key-here` with your actual Anthropic API key (starts with `sk-ant-`)
4. Click **Save** (CTRL+S or CMD+S)

### Step 3: Rerun the App
The app will automatically rerun with the API key. You should see:
- ✅ "API Key Configured" (in green)

### Step 4: Test It
1. Fill in your financial information:
   - Annual Income: 85000
   - Total Savings: 25000
   - Total Loans: 40000
   - Monthly Expenses: 3200
   - Investment Amount: 8000

2. Click the **📈 Analyze** button
3. Wait for the analysis to complete (takes 5-10 seconds)

## Where to Find Your API Key
1. Go to https://console.anthropic.com
2. Log in with your account
3. Navigate to API Keys section
4. Copy your key (it starts with `sk-ant-`)
5. Paste it in Streamlit Secrets (Step 2 above)

## Troubleshooting

### Still showing "API Key Not Configured"?
- Refresh the page (F5)
- Clear browser cache
- Wait 30 seconds for the secret to sync

### Getting API errors?
- Check that API key is pasted exactly as shown (starts with `sk-ant-`)
- Verify you clicked Save in the Secrets section
- Check Streamlit app logs (bottom right)

### App still crashes?
- Go to Settings → Manage app
- Click "Reboot app"
- Try again

## Security Note
⚠️ **Important**: The `.streamlit/secrets.toml` file is automatically ignored by git and won't be pushed to GitHub. Only Streamlit Cloud stores the actual secret key securely.

---

**After adding the secret, your app will be fully functional!** 🎉
