# Quick Start Guide - 5 Minutes

Get your misinformation detection pipeline running in 5 minutes!

**Updated:** December 9, 2025 - v3.3 Simplified Single-Item Processing & Google Sheets ⭐

---

## ✅ Prerequisites

- n8n installed and running
- 5 minutes of your time

---

## 🚀 Step 1: Install n8n (if needed)

### Option A: Using npm
```bash
npm install n8n -g
n8n start
```

### Option B: Using Docker
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

Access n8n at: **http://localhost:5678**

---

## 🔑 Step 2: Get API Keys (2 minutes)

### Groq API (Primary Agents - FREE TIER!)
1. Go to: https://console.groq.com/
2. Sign up / Log in
3. Go to **API Keys**
4. Click **Create API Key**
5. Copy the key ✅

### Google Gemini API (Backup + Decision Agents)
1. Go to: https://makersuite.google.com/app/apikey
2. Click **Get API Key**
3. Copy the key ✅

### Google Sheets API (Results Logging)
1. In n8n, go to **Credentials** → **Add Credential**
2. Search for **Google Sheets OAuth2 API**
3. Click **Connect my account**
4. Follow OAuth flow to authorize
5. Create a Google Sheet for logging results ✅

### Supabase (WhatsApp Data Storage)
1. Go to: https://supabase.com/
2. Create new project
3. Go to **Settings** → **API**
4. Copy **URL** and **anon/public** key ✅
5. Create table:
```sql
CREATE TABLE "false-news" (
  id INTEGER PRIMARY KEY,
  text TEXT NOT NULL,
  title TEXT,
  subject TEXT,
  date TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### WhatsApp Business API
1. Go to: https://business.whatsapp.com/
2. Follow setup instructions
3. Get API credentials ✅

---

## 📥 Step 3: Import Workflow (1 minute)

1. Open n8n: **http://localhost:5678**
2. Go to **Workflows** (left sidebar)
3. Click **Import from File**
4. Select: `workflow-twitter-whatsapp-combined.json`
5. Click **Import**

---

## 🔐 Step 4: Add Credentials (1 minute)

### Add Groq API:
1. In n8n, go to **Credentials** (left sidebar)
2. Click **Add Credential**
3. Search for **Groq**
4. Paste your Groq API key
5. Click **Save**

### Add Google Gemini API:
1. Click **Add Credential**
2. Search for **Google PaLM** (Gemini)
3. Paste your Gemini API key
4. Click **Save**

### Add Supabase:
1. Click **Add Credential**
2. Search for **Supabase**
3. Enter:
   - Host: Your Supabase URL
   - Service Role Secret: Your anon key
4. Click **Save**

### Add WhatsApp:
1. Click **Add Credential**
2. Search for **WhatsApp**
3. Follow the OAuth flow
4. Click **Save**

---

## ✨ Step 5: Activate Workflow (30 seconds)

1. Open the imported workflow
2. Click **Active** toggle (top-right)
3. Workflow should show green "Active" status ✅

---

## 🧪 Step 6: Test It! (1 minute)

### Test WhatsApp Flow:

1. **Add test data to Supabase:**
```sql
INSERT INTO "false-news" (id, text, title, subject, date)
VALUES (
  600,
  'This week''s chaotic news cycle was mostly dominated by Donald Trump''s disgraceful response to violence...',
  'Charlottesville News',
  'Politics',
  '2017-08-18'
);
```

2. **Send WhatsApp message:**
```
600
```

3. **Check execution in n8n:**
   - Go to **Executions** tab
   - Click on latest execution
   - Verify all nodes succeeded ✅

4. **Expected output:**
```json
{
  "final_assessment": {
    "risk_level": "MEDIUM",
    "composite_score": 55,
    "confidence": "MEDIUM",
    "data_completeness": "PARTIAL"
  },
  "summary": "Analysis based on fact-checking and source credibility..."
}
```

---

## 🎯 What to Check

### ✅ Verify These Nodes Executed:

1. **WhatsApp Trigger** - Received message
2. **Code in JavaScript** - Extracted ID (600)
3. **Get a row in Supabase** - Retrieved data
4. **Format WhatsApp Data** - Formatted to unified structure
5. **Agent 1 - Fact Check** - Analyzed claims
6. **Agent 2 - Credibility** - Checked source
7. **Agent 3 - Twitter Check** - Returned NOT_APPLICABLE (expected!)
8. **Agent 4 - Decision** - Final risk assessment
9. **Respond to Webhook** - Returned JSON

### ✅ Verify Agent 3 Output:

Click on **Agent 3 - Twitter Check** node, should see:
```json
{
  "bot_probability": "NOT_APPLICABLE",
  "authenticity_score": 50,
  "data_available": false,
  "recommendation": "Account analysis not available - manual/WhatsApp input"
}
```

This is **correct** - WhatsApp has no Twitter account data!

### ✅ Verify Agent 4 Weighting:

Agent 4 should use **70/30 weighting** (Fact/Source) for WhatsApp:
```json
{
  "data_completeness": "PARTIAL"
}
```

---

## 🐛 Troubleshooting

### Issue: "Supabase connection failed"
**Fix:**
- Check Supabase credentials in n8n
- Verify table "false-news" exists
- Test connection in Supabase settings

### Issue: "WhatsApp trigger not working"
**Fix:**
- Check WhatsApp credentials
- Verify webhook is active
- Check WhatsApp Business API status

### Issue: "Agent returns error"
**Fix:**
- Check API keys are valid
- Verify API rate limits not exceeded
- Check agent prompts are complete

### Issue: "No data returned"
**Fix:**
- Verify ID exists in Supabase
- Check "Get a row in Supabase" output
- Ensure "Format WhatsApp Data" node has correct code

---

## 🎓 Understanding the Flow

### Data Transformation:

**1. WhatsApp Message:**
```
"600"
```

**2. After Supabase Lookup:**
```json
{
  "id": 600,
  "text": "This week's chaotic news cycle...",
  "title": "Charlottesville News",
  "subject": "Politics",
  "date": "2017-08-18"
}
```

**3. After Format WhatsApp Data:**
```json
{
  "tweetText": "This week's chaotic news cycle...",
  "tweetSource": "Charlottesville News",
  "sourceType": "whatsapp",
  "tweetMetadata": {},
  "accountData": {},
  "supabase_id": 600
}
```

**4. After Agents:**
```json
{
  "final_assessment": {
    "risk_level": "HIGH/MEDIUM/LOW",
    "composite_score": 0-100,
    "confidence": "HIGH/MEDIUM/LOW"
  }
}
```

---

## 📊 Monitoring

### Key Metrics to Watch:

1. **Execution Time:**
   - Target: 5-15 seconds (without backups)
   - With backups: 15-30 seconds

2. **Backup Trigger Rate:**
   - Target: 20-30%
   - If >50%: Agents may need better prompts
   - If <10%: Agents may be overconfident

3. **Error Rate:**
   - Target: <1%
   - Common: Supabase timeouts, API rate limits

4. **Cost per Message:**
   - WhatsApp: ~$0.003 (without backups)
   - WhatsApp: ~$0.018 (with backups)

### View Execution Logs:

1. Go to **Executions** tab
2. Click on any execution
3. See each node's input/output
4. Check execution time per node

---

## 🚀 Next Steps

### For Production:

1. **Add More Test Data:**
```sql
INSERT INTO "false-news" (id, text, title, subject, date)
VALUES 
  (601, 'Another test message...', 'Source', 'Topic', '2024-01-01'),
  (602, 'More test data...', 'Source', 'Topic', '2024-01-02');
```

2. **Test Different Scenarios:**
   - True claims from reliable sources
   - False claims from unreliable sources
   - Mixed/unverifiable claims
   - Different topics (health, politics, science)

3. **Monitor Performance:**
   - Track execution times
   - Monitor API costs
   - Review backup trigger rates
   - Check accuracy vs ground truth

4. **Tune Prompts:**
   - Adjust confidence thresholds
   - Modify risk level boundaries
   - Add domain-specific knowledge
   - Update fact-checking sources

### For Twitter Support:

1. **Get Twitter API Credentials:**
   - Apply for Elevated access
   - Get API keys

2. **Add Twitter Credentials to n8n:**
   - Go to Credentials
   - Add Twitter API v2
   - Paste keys

3. **Test Twitter Webhook:**
```bash
curl -X POST http://localhost:5678/webhook/misinformation-check-twitter \
  -H "Content-Type: application/json" \
  -d '{
    "tweets": [{
      "tweetText": "Breaking news: Scientists discover...",
      "tweetSource": "https://example.com/article",
      "tweetMetadata": {
        "account_handle": "@username",
        "follower_count": 5000,
        "tweet_count": 12000
      }
    }]
  }'
```

4. **Verify Full Data Flow:**
   - Agent 1: Fact-check ✅
   - Agent 2: Source + Bot check ✅
   - Agent 3: Full account analysis ✅
   - Agent 4: 50/30/20 weighting ✅

---

## 📚 Additional Resources

### Documentation:
- **README.md** - Complete overview
- **AI_CONTEXT.md** - Context for AI assistants
- **AGENT_PROMPTS.md** - All agent prompts
- **EXAMPLES.md** - Test cases

### External Links:
- n8n Docs: https://docs.n8n.io/
- Groq Docs: https://console.groq.com/docs
- Gemini Docs: https://ai.google.dev/docs
- Supabase Docs: https://supabase.com/docs

### Community:
- n8n Community: https://community.n8n.io/
- n8n Discord: https://discord.gg/n8n

---

## ✨ You're Done!

Your misinformation detection pipeline is now:
- ✅ Installed
- ✅ Configured
- ✅ Tested
- ✅ Ready to use!

**Send a WhatsApp message and watch the magic happen!** 🚀

---

## 💡 Pro Tips

1. **Use Groq Free Tier** - Save costs on primary agents
2. **Monitor Backup Triggers** - Tune prompts if too high/low
3. **Cache Results** - Avoid re-analyzing identical content
4. **Add Rate Limiting** - Prevent API abuse
5. **Log Everything** - Track performance and accuracy
6. **Human Review** - Always verify high-risk cases
7. **Update Prompts** - Improve based on feedback
8. **Test Regularly** - Ensure accuracy over time

---

**Need help?** Check [README.md](README.md) or [AI_CONTEXT.md](AI_CONTEXT.md)

**Questions?** Review [EXAMPLES.md](EXAMPLES.md) for test cases

**Ready for more?** See [AGENT_PROMPTS.md](AGENT_PROMPTS.md) to customize agents
