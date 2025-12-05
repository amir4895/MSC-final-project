# N8N Misinformation Detection Pipeline

**Last Updated:** December 5, 2025  
**Version:** 2.1 - Optimized WhatsApp Flow  
**Status:** WhatsApp Active ✅ | Twitter Ready ⏳

---

## 📋 Quick Links

- **Get Started:** See [QUICK_START.md](QUICK_START.md) (5 minutes)
- **AI Context:** See [AI_CONTEXT.md](AI_CONTEXT.md) (for AI assistants)
- **Agent Prompts:** See [AGENT_PROMPTS.md](AGENT_PROMPTS.md)
- **Test Cases:** See [EXAMPLES.md](EXAMPLES.md)
- **Workflow File:** `workflow-twitter-whatsapp-combined.json`

---

## 📁 File Guide

### 📋 File Guide Summary:

| File | Size | Purpose | When to Use |
|------|------|---------|-------------|
| **workflow-twitter-whatsapp-combined.json** | 36K | n8n workflow definition | Import into n8n to set up |
| **README.md** | 9.0K | Project overview (this file) | First time reading about project |
| **QUICK_START.md** | 8.9K | 5-minute setup guide | Installing and testing |
| **AI_CONTEXT.md** | 19K | Context for AI assistants | Starting new AI chat sessions |
| **AGENT_PROMPTS.md** | 19K | All 6 agent prompts | Customizing agent behavior |
| **EXAMPLES.md** | 16K | Test cases & validation | Testing and validation |

**Navigation:**
- 🆕 **First time?** → Start here (README.md)
- 🚀 **Want to set up?** → [QUICK_START.md](QUICK_START.md)
- 🤖 **Using AI assistant?** → Share [AI_CONTEXT.md](AI_CONTEXT.md)
- 🧪 **Need test data?** → [EXAMPLES.md](EXAMPLES.md)
- ⚙️ **Want to customize?** → [AGENT_PROMPTS.md](AGENT_PROMPTS.md)

---

## 🎯 What This Does

A **multi-agent AI system** that detects misinformation in:
- **WhatsApp messages** (manual input - currently active)
- **Twitter/X tweets** (webhook - ready for testing)

### How It Works:

```
Input (WhatsApp/Twitter)
    ↓
6 AI Agents analyze in parallel
    ↓
Risk Assessment: HIGH/MEDIUM/LOW
    ↓
Detailed JSON report
```

---

## 🤖 The 6 AI Agents

### Primary Agents (Groq LLM):
1. **Agent 1 - Fact Check** → Verifies claims using fact-checking sites
2. **Agent 2 - Credibility** → Evaluates source trustworthiness + bot detection
3. **Agent 3 - Twitter Check** → Analyzes account behavior (Twitter only)

### Backup Agents (Google Gemini):
4. **Agent 1B** → Second opinion on fact-checking (if confidence low)
5. **Agent 2B** → Second opinion on credibility (if confidence low)

### Decision Agent (Google Gemini):
6. **Agent 4 - Decision** → Synthesizes all outputs with adaptive weighting

---

## 🔄 Workflow Flow

### WhatsApp Flow (Active):
```
WhatsApp Message (ID number)
    ↓
Fetch from Supabase ("false-news" table)
    ↓
Format to unified structure
    ↓
Agents 1, 2, 3 analyze (parallel)
    ↓
[Backup agents if needed]
    ↓
Agent 4 decides (70% fact + 30% source)
    ↓
Return risk assessment
```

### Twitter Flow (Ready):
```
Twitter Webhook (POST)
    ↓
Parse tweet + metadata
    ↓
Agents 1, 2, 3 analyze (parallel)
    ↓
[Backup agents if needed]
    ↓
Agent 4 decides (50% fact + 30% source + 20% account)
    ↓
Return risk assessment
```

---

## 🎨 Key Features

✅ **Adaptive Weighting** - Adjusts scoring based on available data  
✅ **Graceful Degradation** - Works with partial data (WhatsApp has no account info)  
✅ **Backup Agents** - Second opinions when confidence is low  
✅ **Unified Input** - Same structure for WhatsApp and Twitter  
✅ **Cost Optimized** - Uses Groq (fast/cheap) for primary agents  
✅ **JSON Output** - Structured data for easy integration  

---

## 💰 Cost Estimate

| Flow | Without Backups | With Backups |
|------|----------------|--------------|
| **WhatsApp** | ~$0.003 | ~$0.018 |
| **Twitter** | ~$0.015 | ~$0.085 |

**Monthly (1000 messages):**
- WhatsApp: $3-18
- Twitter: $15-85
- Mixed: $9-50

*Using Groq free tier can reduce costs to near-zero for primary agents*

---

## 🚀 Quick Start

### 1. Prerequisites:
- n8n installed and running
- Groq API key (free tier available)
- Google Gemini API key
- Supabase account (for WhatsApp)
- WhatsApp Business API (for WhatsApp)

### 2. Import Workflow:
```bash
# In n8n:
Workflows → Import from File → workflow-twitter-whatsapp-combined.json
```

### 3. Configure Credentials:
- Groq API (Agents 1, 2, 3)
- Google Gemini API (Agents 1B, 2B, 4)
- Supabase (WhatsApp data)
- WhatsApp Business API

### 4. Test:
Send WhatsApp message with ID number (e.g., "600")

**Full instructions:** See [QUICK_START.md](QUICK_START.md)

---

## 📊 Output Format

```json
{
  "final_assessment": {
    "risk_level": "HIGH/MEDIUM/LOW",
    "composite_score": 45,
    "confidence": "HIGH/MEDIUM/LOW",
    "data_completeness": "FULL/PARTIAL/FACT_CHECK_ONLY"
  },
  "contributing_factors": {
    "fact_check_verdict": "MOSTLY_FALSE",
    "fact_check_score": 25,
    "source_credibility": "LOW",
    "source_score": 30,
    "account_authenticity": "MODERATE_RISK",
    "account_score": 60
  },
  "key_concerns": [
    "Core claims contradicted by fact-checkers",
    "Source flagged as low credibility"
  ],
  "recommended_action": {
    "primary_action": "Flag for review and add warning label",
    "rationale": "False claims from unreliable source",
    "urgency": "within_24h"
  },
  "human_review_needed": true,
  "summary": "Tweet contains false claims from unreliable source..."
}
```

---

## 🗄️ Data Structure

### Supabase Table: "false-news"
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

### Unified Input Format:
```javascript
{
  tweetText: "content to analyze",
  tweetSource: "source URL or title",
  sourceType: "whatsapp" | "twitter",
  tweetMetadata: {},  // Twitter only
  accountData: {}     // Twitter only
}
```

---

## 🎓 Academic Context

### Research Focus:
- Multi-agent AI systems for misinformation detection
- Adaptive scoring with partial data availability
- Cost-effective LLM orchestration
- Graceful degradation strategies

### Original Proposal (5 Agents):
1. ~~Scout Agent~~ - Automated Twitter monitoring (future)
2. **Fact-Check Agent** ✅ → Agent 1
3. **Credibility Agent** ✅ → Agent 2
4. **Decision Agent** ✅ → Agent 4
5. ~~Responder Agent~~ - Automated replies (future)

*Agent 3 (Twitter Check) was added for account behavior analysis*

---

## 🔧 Recent Updates (Dec 5, 2025)

### What Changed:
- ✅ Removed redundant AI Agent for WhatsApp data extraction
- ✅ Replaced with simple JavaScript code node
- ✅ Unified input format for both WhatsApp and Twitter
- ✅ 60% cost reduction for WhatsApp flow
- ✅ Cleaned up documentation (removed 10 duplicate files)

### Why:
- AI Agent was using expensive LLM call for simple data formatting
- JavaScript is faster, cheaper, and more reliable
- Simpler workflow with fewer dependencies

---

## 📁 Project Files

### Essential Files:
- `workflow-twitter-whatsapp-combined.json` - Main workflow (import this)
- `README.md` - This file
- `QUICK_START.md` - 5-minute setup guide
- `AI_CONTEXT.md` - Context for AI assistants
- `AGENT_PROMPTS.md` - All agent prompts
- `EXAMPLES.md` - Test cases

### For Development:
- `AI_CONTEXT.md` - Share this with AI assistants in new chats

---

## 🐛 Troubleshooting

### Common Issues:

**"Supabase node failed"**
→ Check credentials, verify table exists, ensure ID exists

**"Agent returns NOT_APPLICABLE"**
→ Expected for WhatsApp (no Twitter data available)

**"Backup agents trigger too often"**
→ Agents may be underconfident, review prompts

**"Wrong weighting in Agent 4"**
→ Verify sourceType is set correctly

---

## 🚀 Future Roadmap

### Short-term:
- [ ] Test Twitter webhook flow
- [ ] Add more test cases
- [ ] Tune agent prompts

### Medium-term:
- [ ] Implement Scout Agent (automated monitoring)
- [ ] Add caching layer
- [ ] Build analytics dashboard
- [ ] Multi-language support

### Long-term:
- [ ] Implement Responder Agent
- [ ] Fine-tune custom models
- [ ] Image/video analysis
- [ ] Coordinated campaign detection

---

## 📞 Support & Resources

### Documentation:
- **Quick Start:** [QUICK_START.md](QUICK_START.md)
- **AI Context:** [AI_CONTEXT.md](AI_CONTEXT.md)
- **Agent Prompts:** [AGENT_PROMPTS.md](AGENT_PROMPTS.md)
- **Examples:** [EXAMPLES.md](EXAMPLES.md)

### External Resources:
- n8n Docs: https://docs.n8n.io/
- Groq Docs: https://console.groq.com/docs
- Google Gemini: https://ai.google.dev/docs
- Supabase: https://supabase.com/docs

### Fact-Checking Resources:
- Snopes: https://www.snopes.com/
- PolitiFact: https://www.politifact.com/
- FactCheck.org: https://www.factcheck.org/
- MBFC: https://mediabiasfactcheck.com/

---

## 📝 License

MIT License - Feel free to modify and adapt for your use case.

---

## 🎯 TL;DR

**What:** Multi-agent misinformation detection in n8n  
**Input:** WhatsApp (active) or Twitter (ready)  
**Agents:** 6 AI agents (3 Groq + 2 Gemini backups + 1 Gemini decision)  
**Output:** Risk level + detailed analysis  
**Cost:** ~$0.003-0.085 per message  
**Status:** Ready to use!  

**Get started:** Import `workflow-twitter-whatsapp-combined.json` into n8n

---

**Built with ❤️ for fighting misinformation**

*This system assists human moderators, not replaces them. Always combine AI insights with human judgment.*
