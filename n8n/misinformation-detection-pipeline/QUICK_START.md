# Quick Start Guide - 5 Minutes to Running

Get your misinformation detection pipeline running in 5 minutes!

---

## Prerequisites

✅ N8N installed and running (http://localhost:5678)  
✅ Google Gemini API key  
✅ OpenAI API key (or Claude)

---

## Step 1: Get API Keys (2 minutes)

### Google Gemini
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Copy the key

### OpenAI
1. Go to: https://platform.openai.com/api-keys
2. Create new secret key
3. Copy the key

---

## Step 2: Add Credentials to N8N (1 minute)

1. Open N8N → **Settings** → **Credentials**
2. Click **Add Credential**
3. Add "Google Gemini" → Paste API key → Name: "Google Gemini API" → Save
4. Add "OpenAI" → Paste API key → Name: "OpenAI API" → Save

---

## Step 3: Import Workflows (1 minute)

1. In N8N, go to **Workflows** → **Import from File**
2. Import `workflow-twitter-webhook.json`
3. Import `workflow-whatsapp-manual.json` (optional)

---

## Step 4: Activate & Test (1 minute)

### For Twitter Webhook:

1. Open "Misinformation Detection - Twitter Webhook" workflow
2. Toggle **Active** switch (top right)
3. Click "Webhook Trigger" node → Copy webhook URL
4. Test with curl:

```bash
curl -X POST YOUR_WEBHOOK_URL \
  -H "Content-Type: application/json" \
  -d '{
    "tweets": [{
      "tweetText": "Breaking: Scientists discover cure for common cold",
      "tweetSource": "https://example.com",
      "tweetMetadata": {
        "account_handle": "@testuser",
        "account_created_date": "2020-01-15",
        "follower_count": 5000,
        "following_count": 500,
        "tweet_count": 12000,
        "bio": "Science journalist",
        "verified": false
      }
    }]
  }'
```

### For WhatsApp Manual:

1. Configure WhatsApp credentials first (see SETUP_GUIDE.md)
2. Open "Misinformation Detection - WhatsApp Manual" workflow
3. Toggle **Active** switch
4. Send a test message to your WhatsApp number

---

## Expected Result

You should get a JSON response like:

```json
{
  "final_assessment": {
    "risk_level": "MEDIUM",
    "composite_score": 55,
    "confidence": "MEDIUM"
  },
  "summary": "Extraordinary health claim requires verification..."
}
```

---

## What's Next?

✅ **Working?** Great! Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for production deployment  
✅ **Not working?** Check [Troubleshooting](#troubleshooting) below  
✅ **Want to customize?** See [AGENT_PROMPTS.md](AGENT_PROMPTS.md)  
✅ **Need examples?** Check [EXAMPLES.md](EXAMPLES.md)

---

## Troubleshooting

### "Invalid API key"
→ Double-check credentials in N8N Settings → Credentials

### "Webhook not found"
→ Make sure workflow is **Active** (toggle switch)

### "Agent returned empty response"
→ Check N8N Executions tab for detailed error logs

### "Timeout error"
→ LLM taking too long, try again or use faster model

---

## Architecture Overview

```
Input (Tweet/WhatsApp)
    ↓
Agent 1 (Fact Check) ─┐
Agent 2 (Credibility) ─┤→ Combine
Agent 3 (Twitter) ─────┘
    ↓
[If uncertain] → Agent 1B & 2B (Backup)
    ↓
Agent 4 (Decision)
    ↓
Output (Risk Assessment)
```

---

## Key Features

✅ **Multi-Agent System** - 6 AI agents working together  
✅ **Backup Agents** - Second opinion when uncertain  
✅ **Two Input Methods** - Twitter webhook or WhatsApp manual  
✅ **Risk Scoring** - HIGH/MEDIUM/LOW classification  
✅ **Source Verification** - Checks MBFC, NewsGuard, fact-checkers  
✅ **Bot Detection** - Identifies automated/suspicious accounts  

---

## Cost Estimate

**Per Analysis:**
- Without backup: ~$0.015
- With backup: ~$0.085

**Monthly (1000 analyses):**
- ~$15-85 depending on backup trigger rate

---

## File Structure

```
n8n-misinformation-detection-pipeline/
├── README.md                          # Overview
├── QUICK_START.md                     # This file
├── SETUP_GUIDE.md                     # Detailed setup
├── AGENT_PROMPTS.md                   # All agent prompts
├── EXAMPLES.md                        # Test cases & examples
├── workflow-twitter-webhook.json      # Twitter workflow
└── workflow-whatsapp-manual.json      # WhatsApp workflow
```

---

## Support

📖 **Full Documentation:** See [README.md](README.md)  
🔧 **Detailed Setup:** See [SETUP_GUIDE.md](SETUP_GUIDE.md)  
💬 **N8N Community:** https://community.n8n.io/  
🐛 **Issues:** Check execution logs in N8N

---

## Quick Reference

### Risk Levels

| Level | Score | Meaning |
|-------|-------|---------|
| HIGH | 0-40 | Likely misinformation, flag/remove |
| MEDIUM | 41-70 | Uncertain, add context label |
| LOW | 71-100 | Appears reliable, no action |

### Agent Roles

| Agent | Role | LLM |
|-------|------|-----|
| Agent 1 | Fact Check | Gemini |
| Agent 2 | Credibility | Gemini |
| Agent 3 | Twitter Check | Gemini |
| Agent 4 | Decision | Gemini |
| Agent 1B | Backup Fact Check | OpenAI/Claude |
| Agent 2B | Backup Credibility | OpenAI/Claude |

### Scoring Weights (Agent 4)

```
Risk Score = (Fact × 50%) + (Source × 30%) + (Account × 20%)
```

---

## Next Steps

1. ✅ Test with examples from [EXAMPLES.md](EXAMPLES.md)
2. ✅ Customize agent prompts in [AGENT_PROMPTS.md](AGENT_PROMPTS.md)
3. ✅ Set up monitoring and alerts
4. ✅ Deploy to production (see [SETUP_GUIDE.md](SETUP_GUIDE.md))

---

**You're all set! 🚀**

Start sending tweets or messages to your pipeline and watch the AI agents work their magic!

