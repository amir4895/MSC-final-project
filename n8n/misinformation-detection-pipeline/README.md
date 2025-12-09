# N8N Misinformation Detection Pipeline

**Last Updated:** December 9, 2025  
**Version:** 3.1 - Fixed Twitter Integration & Individual Processing  
**Status:** WhatsApp Active ✅ | Twitter Fixed ✅

---

## 📋 Quick Links

- **Get Started:** See [QUICK_START.md](QUICK_START.md) (5 minutes)
- **AI Context:** See [AI_CONTEXT.md](AI_CONTEXT.md) (for AI assistants)
- **Agent Prompts:** See [AGENT_PROMPTS.md](AGENT_PROMPTS.md)
- **Test Cases:** See [EXAMPLES.md](EXAMPLES.md)
- **Workflow Files:**
  - **Main:** `workflow-misinformation-detection-fixed.json` ⭐ (RECOMMENDED)
  - **Legacy:** `workflow-twitter-whatsapp-combined.json`
  - **Standalone:** `workflow-viral-tweets-easy-scraper.json`

---

## 📁 File Guide

### 📋 File Guide Summary:

| File | Size | Purpose | When to Use |
|------|------|---------|-------------|
| **workflow-misinformation-detection-fixed.json** ⭐ | 38K | Fixed n8n workflow (RECOMMENDED) | Import into n8n - all fixes included |
| **workflow-twitter-whatsapp-combined.json** | 36K | Legacy workflow (original) | Reference only - has known issues |
| **workflow-viral-tweets-easy-scraper.json** | 3K | Standalone Twitter scraper | Testing Twitter API separately |
| **README.md** | 10K | Project overview (this file) | First time reading about project |
| **QUICK_START.md** | 9K | 5-minute setup guide | Installing and testing |
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

## 🆕 What's New in v3.1 (December 9, 2025)

### ✅ Fixed Issues:
- **Manual Trigger Error** - Fixed "Cannot assign to read only property" error
- **Item Limit Not Working** - Now respects limit setting (2, 5, 10 tweets)
- **Duplicate Items** - Fixed duplicate processing by bypassing merge node
- **Batch Processing** - Added "Split Out Items" node for individual tweet processing
- **Field Mapping** - Flexible mapping for different Twitter API response formats

### 🎯 New Features:
- **Debug Logging** - Console logs for API response structure
- **Error Handling** - Try-catch blocks with fallback values
- **Standalone Scraper** - Separate workflow for testing Twitter API

---

## 🎯 What This Does

A **multi-agent AI system** that detects misinformation in:
- **Dataset messages** (manual input via WhatsApp - currently active)
  - Supports both **true-news** and **false-news** datasets
  - Input format: `T123` (true-news) or `F456` (false-news)
- **Twitter/X tweets** (automated scraping - FIXED ✅)
  - Fetches viral tweets every 4 hours OR manual trigger
  - Processes each tweet individually through the pipeline
  - Configurable limit (2, 5, 10, etc.)

### How It Works:

```
Input (Dataset/Twitter)
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

### Dataset Flow (Active):
```
WhatsApp Message (e.g., "T123" or "F456")
    ↓
Parse: Dataset type (T/F) + Index (123)
    ↓
Fetch from Supabase ("true-news" or "false-news" table)
    ↓
AI Agent formats to unified structure
    ↓
Agents 1, 2, 3 analyze (parallel)
    ↓
[Backup agents if needed]
    ↓
Agent 4 decides (70% fact + 30% source)
    ↓
Return risk assessment
```

### Twitter Flow (FIXED ✅):
```
Manual Trigger OR Every 4 Hours
    ↓
Set Limit (2, 5, 10 tweets)
    ↓
Search Viral News Tweets (RapidAPI)
    ↓
Add Limit to Response (pass limit forward)
    ↓
Get Top N Most Viral (rank by virality score)
    ↓
Split Out Items (process individually) ⭐ NEW
    ↓
Format Input Data
    ↓
Parse Input Data
    ↓
Agents 1, 2, 3 analyze (parallel) - ONE TWEET AT A TIME
    ↓
[Backup agents if needed]
    ↓
Agent 4 decides (50% fact + 30% source + 20% account)
    ↓
Return risk assessment (per tweet)
```

**Key Improvements:**
- ✅ Each tweet processed individually (not in batch)
- ✅ Configurable limit actually works
- ✅ No duplicate processing
- ✅ Proper error handling

---

## 🆕 Recent Updates

### v3.1 (Dec 9, 2025) - Twitter Integration Fixed
- Fixed manual trigger error
- Added "Split Out Items" for individual processing
- Fixed item limit not being respected
- Removed duplicate processing
- Added flexible field mapping for Twitter API
- Added debug logging

### v3.0 (Dec 8, 2025) - Advanced False News Classification

### 🚀 Major Upgrade: Advanced False News Classification

#### **Agent 1 - Completely Redesigned:**
- ✅ **Multi-Dimensional Classification:**
  - MISINFORMATION (unintentional false info)
  - DISINFORMATION (deliberate false info)
  - PROPAGANDA (true facts, misleading framing) ⭐ NEW
  - SATIRICAL (humor/satire)
  - CLICK-BAIT (low quality content)
  - LEGITIMATE (accurate and fair)
  - BIASED_BUT_FACTUAL (true but biased) ⭐ NEW

- ✅ **Two-Dimensional Scoring:**
  - `fact_accuracy_score` (0-100) - How factually correct
  - `deceptiveness_score` (0-100) - How misleading ⭐ NEW
  - **Key Insight:** TRUE FACTS can still be MISLEADING

- ✅ **Advanced Pattern Detection:**
  - FABRICATION - Made-up facts
  - SELECTIVE_OMISSION - Cherry-picking facts
  - FALSE_CAUSATION - Incorrect cause-effect
  - INTENT_FABRICATION - Falsely attributing motives
  - EMOTIONAL_MANIPULATION - Exploiting emotions
  - MISLEADING_FRAMING - Biased presentation

- ✅ **Context Analysis:**
  - Detects omitted context
  - Identifies false connections between facts
  - Flags misleading framing
  - Recognizes false choices/dichotomies

#### **Agent 2 - Enhanced Source Analysis:**
- ✅ **Publisher Extraction:** For dataset articles, extracts actual publisher from text
- ✅ **Three-Scenario Support:** Dataset/Twitter/News articles
- ✅ **Web Search Integration:** Uses web_search for verification

#### **Backup Agents - True Independence:**
- ✅ **Comparison Analysis:** New `comparison_with_primary` field
  - Areas of agreement
  - Areas of disagreement
  - Explanation of differences
- ✅ **Encouraged Disagreement:** "Disagreement is valuable"
- ✅ **Web Search Access:** Independent verification capability

### Updated:
- 🔄 **Max Iterations:** Increased to 5 for Agent 1 (was 1)
- 🔄 **Web Search Tools:** Integrated for fact verification
- 🔄 **Groq Model** - Primary agents use `meta-llama/llama-4-scout-17b-16e-instruct`
- 🔄 **Google Gemini Model** - Backup/decision agents use `models/gemini-2.5-flash`

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
| **Dataset** | ~$0.008 | ~$0.023 |
| **Twitter** | ~$0.015 | ~$0.085 |

**Monthly (1000 messages):**
- Dataset: $8-23
- Twitter: $15-85
- Mixed: $11-54

*Note: Dataset flow uses AI Agent for formatting, slightly higher cost than direct code*  
*Using Groq free tier can reduce costs significantly for primary agents*

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
Send WhatsApp message with dataset + ID (e.g., "T123" or "F456")

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

### Supabase Tables:

**Table 1: False News Dataset**
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

**Table 2: True News Dataset**
```sql
CREATE TABLE "true-news" (
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
  tweetSource: "dataset name or URL",
  sourceType: "dataset" | "twitter",
  tweetMetadata: {},  // Twitter only
  accountData: {},    // Twitter only
  // Dataset-specific fields
  dataset: "true-news" | "false-news",
  datasetType: "T" | "F",
  supabase_id: 123
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
- ✅ Added dual dataset support (true-news + false-news)
- ✅ WhatsApp input format: T123 (true) or F456 (false)
- ✅ Dynamic Supabase routing based on dataset type
- ✅ AI Agent formats data with dataset metadata
- ✅ Changed terminology: WhatsApp → Dataset throughout
- ✅ Unified input format for both Dataset and Twitter
- ✅ Cleaned up documentation (removed 10 duplicate files)

### Why:
- Support testing with both true and false news datasets
- Track which dataset each message comes from
- Enable comparison of detection accuracy across datasets
- More accurate terminology (data comes from datasets, not WhatsApp)

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
