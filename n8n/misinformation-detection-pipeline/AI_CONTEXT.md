# AI Context File - Misinformation Detection Pipeline

**Purpose:** This file provides complete context for AI assistants to understand this project quickly.  
**Last Updated:** December 14, 2025  
**Version:** 5.2 - Prompt Optimization & Refinement  
**Project Status:** Active Development - WhatsApp ✅ | Twitter ✅ | Google Sheets Logging ✅ | Optimized Prompts ✅

---

## 📑 Table of Contents

1. [Project Overview](#-project-overview)
2. [Project Structure & File Guide](#-project-structure--file-guide)
3. [Current Workflow Flow](#-current-workflow-flow)
4. [Data Structures](#-data-structures)
5. [Key Design Decisions](#-key-design-decisions)
6. [Cost Structure](#-cost-structure)
7. [Recent Changes](#-recent-changes-dec-5-2025)
8. [Current Status & Limitations](#-current-status--limitations)
9. [Academic Context](#-academic-context)
10. [API Keys & Credentials Required](#-api-keys--credentials-required)
11. [Common Issues & Solutions](#-common-issues--solutions)
12. [Testing & Validation](#-testing--validation)
13. [Future Roadmap](#-future-roadmap)
14. [Tips for AI Assistants](#-tips-for-ai-assistants)
15. [Quick Context Summary (TL;DR)](#-quick-context-summary-tldr)

---

## 🎯 Project Overview

### What This Is:
A **multi-agent AI system** built in n8n that detects misinformation in text messages (WhatsApp) and tweets (Twitter) using specialized AI agents.

### Original Research Proposal:
The student proposed a 5-agent system:
1. ~~Scout Agent~~ - Real-time Twitter monitoring (not implemented yet)
2. **Fact-Check Agent** - Verify claims using LLMs and fact-checking sites
3. **Credibility Agent** - Source trustworthiness + bot detection
4. **Decision Agent** - Risk assessment combining all factors
5. ~~Responder Agent~~ - Automated counter-messaging (not implemented yet)

### Current Implementation:
**6 AI Agents** in n8n:
- **Agent 1** - Fact Check (Groq LLM)
- **Agent 2** - Credibility/Source Trust (Groq LLM)
- **Agent 3** - Twitter Account Behavior (Groq LLM)
- **Agent 4** - Final Decision (Google Gemini)
- **Agent 1B** - Fact Check Backup (Google Gemini) - triggered on low confidence
- **Agent 2B** - Credibility Backup (Google Gemini) - triggered on low confidence

---

## 📁 Project Structure & File Guide

### Current Files (Cleaned Up - Dec 5, 2025):

```
n8n/misinformation-detection-pipeline/
├── workflow-twitter-whatsapp-combined.json  ⭐ MAIN WORKFLOW
├── README.md                                📖 PROJECT OVERVIEW
├── QUICK_START.md                           🚀 SETUP GUIDE
├── AI_CONTEXT.md                            🤖 THIS FILE
├── AGENT_PROMPTS.md                         💬 AGENT DETAILS
└── EXAMPLES.md                              📝 TEST CASES
```

### 📋 File Guide Summary:

| File | Size | Purpose | When to Use |
|------|------|---------|-------------|
| **workflow-twitter-whatsapp-combined.json** | 36K | n8n workflow definition | Import into n8n to set up the pipeline |
| **README.md** | 9.0K | Project overview & documentation | First time reading about the project |
| **QUICK_START.md** | 8.9K | Step-by-step setup guide | Installing, configuring, and testing |
| **AI_CONTEXT.md** | 19K | Complete context for AI assistants | Starting new AI chat sessions |
| **AGENT_PROMPTS.md** | 19K | All 6 agent prompts & customization | Customizing agent behavior |
| **EXAMPLES.md** | 16K | Test cases & validation scenarios | Testing and validating accuracy |

### 🎯 Quick Navigation:

**For Users:**
1. **First time?** → Start with `README.md`
2. **Want to set up?** → Follow `QUICK_START.md`
3. **Need test data?** → Check `EXAMPLES.md`
4. **Want to customize?** → See `AGENT_PROMPTS.md`

**For AI Assistants:**
1. **Need context?** → Read `AI_CONTEXT.md` (this file)
2. **Understanding workflow?** → Check workflow structure below
3. **Helping with setup?** → Reference `QUICK_START.md`
4. **Debugging agents?** → See `AGENT_PROMPTS.md`

**For Developers:**
1. **Import workflow:** `workflow-twitter-whatsapp-combined.json`
2. **Understand architecture:** `README.md` + `AI_CONTEXT.md`
3. **Test:** `QUICK_START.md` + `EXAMPLES.md`
4. **Customize:** `AGENT_PROMPTS.md`

### 🗑️ Deleted Files (Dec 5, 2025 Cleanup):

**Removed for consolidation:**
- ❌ `START_HERE.txt` → Merged into `README.md`
- ❌ `PROJECT_SUMMARY.md` → Merged into `README.md` + `AI_CONTEXT.md`
- ❌ `SETUP_GUIDE.md` → Merged into `QUICK_START.md`
- ❌ `UPDATED_FLOW_DIAGRAM.md` → Merged into `AI_CONTEXT.md`
- ❌ `WORKFLOW_UPDATE_SUMMARY.md` → Merged into `README.md`
- ❌ `IMPORT_AND_TEST_GUIDE.md` → Merged into `QUICK_START.md`

**Removed legacy workflows:**
- ❌ `workflow-twitter-automated-reorganized.json`
- ❌ `workflow-twitter-automated.json`
- ❌ `workflow-twitter-webhook.json`
- ❌ `workflow-whatsapp-manual.json`

**Result:** Reduced from 16 files to 6 files (-62%) with no loss of information

---

## 🔄 Current Workflow Flow

### WhatsApp Flow (Currently Active):
```
WhatsApp Trigger
  ↓
Code in JavaScript (extract ID from message)
  ↓
Get a row in Supabase (fetch by ID from "false-news" table)
  ↓
Format WhatsApp Data (JavaScript - formats to unified structure)
  ↓
Combine All Agent Results2 (merge with Twitter input)
  ↓
Format Input Data (auto-detect source type)
  ↓
Parse Input Data (normalize fields)
  ↓
┌─────────────┬──────────────┬───────────────┐
│  Agent 1    │   Agent 2    │   Agent 3     │
│ (Fact)      │ (Credibility)│ (Twitter)     │
│ [Groq]      │  [Groq]      │  [Groq]       │
└──────┬──────┴──────┬───────┴───────┬───────┘
       │             │               │
       ↓             ↓               ↓
Check Confidence  Check Confidence   (no check)
       │             │               │
  [If Low]      [If Low]             │
       ↓             ↓               │
   Agent 1B      Agent 2B            │
   [Gemini]      [Gemini]            │
       │             │               │
       ↓             ↓               │
Merge Results  Merge Results         │
       │             │               │
       └─────────────┴───────────────┘
                     ↓
          Combine All Agent Results
                     ↓
          Combine All Agent Results1
                     ↓
              Agent 4 (Decision)
              [Gemini - Adaptive]
                     ↓
            Respond to Webhook
```

### Twitter Flow (Ready, Not Yet Active):
```
Webhook - Twitter Input
  ↓
Combine All Agent Results2
  ↓
[Same as above from "Format Input Data" onwards]
```

---

## 🗄️ Data Structures

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

### Unified Input Format (After "Format WhatsApp Data"):
```javascript
{
  text: "content here",
  tweetText: "content here",              // Main content for analysis
  tweetSource: "source or title",         // Source reference
  sourceType: "whatsapp" | "twitter",     // Input type
  tweetMetadata: {},                      // Twitter metadata (empty for WhatsApp)
  accountData: {},                        // Twitter account data (empty for WhatsApp)
  // WhatsApp-specific fields (preserved for reference)
  supabase_id: 123,
  subject: "...",
  date: "..."
}
```

### Agent Output Format:

**Agent 1 (Fact Check):**
```json
{
  "verdict": "TRUE/MOSTLY_TRUE/MIXED/MOSTLY_FALSE/FALSE/UNVERIFIABLE",
  "confidence": "high/medium/low",
  "verified_claims": [...],
  "overall_assessment": "...",
  "fact_check_score": 0-100
}
```

**Agent 2 (Credibility):**
```json
{
  "source_credibility": {
    "rating": "HIGH/MEDIUM/LOW/UNKNOWN/NOT_APPLICABLE",
    "score": 0-100,
    "explanation": "...",
    "sources_checked": ["MBFC", "NewsGuard"],
    "red_flags": [...]
  },
  "bot_likelihood": {
    "assessment": "HIGH_RISK/MODERATE_RISK/LOW_RISK/HUMAN_LIKELY/NOT_APPLICABLE",
    "confidence": "high/medium/low/not_applicable"
  },
  "overall_trustworthiness_score": 0-100,
  "data_available": true/false
}
```

**Agent 3 (Twitter Check):**
```json
{
  "account_analysis": {
    "handle": "@username" | "N/A",
    "account_age_risk": "VERY_HIGH/HIGH/MODERATE/LOW/MINIMAL/NOT_APPLICABLE",
    "frequency_risk": "...",
    "profile_completeness": {...}
  },
  "bot_probability": "VERY_HIGH/HIGH/MODERATE/LOW/MINIMAL/NOT_APPLICABLE",
  "authenticity_score": 0-100,
  "data_available": true/false
}
```

**Agent 4 (Decision):**
```json
{
  "final_assessment": {
    "risk_level": "HIGH/MEDIUM/LOW",
    "composite_score": 0-100,
    "confidence": "HIGH/MEDIUM/LOW",
    "data_completeness": "FULL/PARTIAL/FACT_CHECK_ONLY"
  },
  "contributing_factors": {...},
  "key_concerns": [...],
  "recommended_action": {...},
  "human_review_needed": true/false,
  "summary": "..."
}
```

---

## 🎯 Key Design Decisions

### 1. Adaptive Weighting (Agent 4)
Agent 4 automatically adjusts scoring weights based on available data:

| Data Available | Weighting |
|----------------|-----------|
| **Full (Twitter)** | Fact (50%) + Source (30%) + Account (20%) |
| **Partial (WhatsApp)** | Fact (70%) + Source (30%) |
| **Fact-check only** | Fact (100%) |

**Why:** WhatsApp messages don't have Twitter account data, so Agent 3 returns neutral score (50) with "NOT_APPLICABLE". Agent 4 detects this and adjusts weights to focus on fact-checking and source credibility.

### 2. Backup Agents (1B, 2B)
**Triggered when:**
- Agent 1: `confidence === "low"` OR `verdict === "UNVERIFIABLE"`
- Agent 2: `confidence === "low"` OR `overall_trustworthiness_score < 50`

**Why:** Provides second opinion using different LLM (Gemini vs Groq) for independent reasoning.

**Conflict Resolution:** If primary and backup disagree, their scores are averaged.

### 3. LLM Selection
- **Primary agents (1, 2, 3):** Groq (fast, cost-effective, free tier available)
- **Backup agents (1B, 2B):** Google Gemini (different reasoning approach)
- **Decision agent (4):** Google Gemini (synthesis and nuanced judgment)

### 4. Graceful Missing Data Handling
All agents check for missing data and return:
- Neutral scores (50) instead of failing
- "NOT_APPLICABLE" flags
- `data_available: false` indicators

This allows the workflow to work with both full Twitter data and minimal WhatsApp data.

---

## 💰 Cost Structure

### Per Analysis:
- **WhatsApp (no backups):** ~$0.003
- **WhatsApp (with backups):** ~$0.018
- **Twitter (no backups):** ~$0.015
- **Twitter (with backups):** ~$0.085

### Monthly (1000 messages):
- **WhatsApp only:** $3-18
- **Twitter only:** $15-85
- **Mixed (50/50):** $9-50

### Cost Optimization:
- Using Groq free tier can reduce costs to near-zero for primary agents
- Backup trigger rate typically 20-30%
- Caching identical content can reduce duplicate analyses

---

## 🔧 Recent Changes (Dec 5, 2025)

### What Changed:
1. **Removed AI Agent1** (Google Gemini) that was extracting text from Supabase
2. **Added "Format WhatsApp Data"** - Simple JavaScript code node
3. **Changed "Get a row in Supabase"** from `supabaseTool` to regular `supabase` node
4. **Removed Google Gemini Chat Model3** (no longer needed)

### Why:
- AI Agent1 was using expensive LLM call for simple data extraction
- JavaScript code is faster, cheaper, and more reliable
- 60% cost reduction for WhatsApp flow

### Result:
- Unified input format for both WhatsApp and Twitter
- Simpler workflow with fewer dependencies
- Same functionality, better performance

---

## 🚧 Current Status & Limitations

### ✅ Working:
- WhatsApp manual input flow
- Supabase data retrieval
- All 6 agents with backup logic
- Adaptive weighting
- Graceful missing data handling
- JSON output for webhook responses

### ⏳ Ready but Not Active:
- Twitter webhook input
- Full Twitter account analysis
- Real-time tweet monitoring

### ❌ Not Implemented:
- Scout Agent (automated Twitter scraping)
- Responder Agent (automated replies)
- Caching layer
- Analytics dashboard
- Human feedback loop
- Batch processing

### Known Limitations:
1. **Language:** Primarily designed for English
2. **Response time:** 5-30 seconds (not real-time)
3. **Context:** May struggle with heavy sarcasm/satire
4. **Source coverage:** Limited to known fact-checking sites
5. **WhatsApp:** No account analysis (by design)

---

## 🎓 Academic Context

### Research Focus:
- Multi-agent AI systems for misinformation detection
- Combining fact-checking, source credibility, and behavioral analysis
- Graceful degradation with partial data
- Cost-effective LLM usage strategies

### Key Innovations:
1. **Adaptive weighting** based on available data
2. **Backup agent system** for second opinions
3. **Unified input format** supporting multiple sources
4. **Cost optimization** using Groq for primary agents

### Potential Publications:
- Multi-agent architecture for misinformation detection
- Adaptive scoring with partial data availability
- Cost-effective LLM orchestration strategies
- Comparison of LLM performance on fact-checking tasks

---

## 🔑 API Keys & Credentials Required

### Active:
1. **Groq API** - Primary agents (1, 2, 3)
   - Get from: https://console.groq.com/
   - Free tier available
   
2. **Google Gemini API** - Backup agents (1B, 2B) + Decision (4)
   - Get from: https://makersuite.google.com/app/apikey
   - Free tier: 60 req/min
   
3. **Supabase** - WhatsApp data storage
   - Get from: https://supabase.com/
   - Table: "false-news"
   
4. **WhatsApp Business API** - WhatsApp trigger
   - Get from: https://business.whatsapp.com/

### Future (for Twitter):
5. **Twitter API v2** - Elevated access
   - Get from: https://developer.twitter.com/

### Optional (enhance accuracy):
6. **Media Bias/Fact Check (MBFC)** - May require subscription
7. **NewsGuard API** - Commercial service
8. **WHOIS API** - Domain age checks

---

## 🐛 Common Issues & Solutions

### Issue: "Supabase node failed"
**Solution:** Check credentials, verify table exists, ensure ID exists in database

### Issue: "Agent returns NOT_APPLICABLE for everything"
**Solution:** Check input data format, verify sourceType is set correctly

### Issue: "Backup agents trigger too often (>50%)"
**Solution:** Agents may be underconfident, review and tune prompts

### Issue: "Agent 4 uses wrong weighting"
**Solution:** Verify sourceType field, check Agent 4 prompt includes adaptive logic

### Issue: "Execution timeout"
**Solution:** LLM API may be slow, consider increasing n8n timeout settings

---

## 📊 Testing & Validation

### Test Cases:
See `EXAMPLES.md` for full test cases including:
1. True claims from reliable sources
2. False claims from unreliable sources
3. Mixed/unverifiable claims
4. Bot-like account patterns
5. Authentic journalist accounts

### Validation Metrics:
- **False Positive Rate:** Target <10%
- **False Negative Rate:** Target <5%
- **Backup Trigger Rate:** Target 20-30%
- **Response Time:** <10s without backups, <30s with backups

### Manual Testing:
1. Send WhatsApp message with ID number
2. Check execution in n8n
3. Verify all agents executed
4. Review final risk assessment
5. Validate against known ground truth

---

## 🆕 Recent Updates (v3.0 - Dec 8, 2025)

### 🚀 MAJOR UPGRADE: Advanced False News Classification System

This is a complete paradigm shift from simple fact-checking to sophisticated false news classification.

#### **Core Philosophy Change:**
- ❌ **Old Approach:** Binary TRUE/FALSE fact-checking
- ✅ **New Approach:** Nuanced classification that recognizes **TRUE FACTS can be MISLEADING**

#### **Agent 1 - Now "False News Classification Agent":**

**New Classifications (7 types):**
1. **LEGITIMATE** - Accurate and fair reporting
2. **BIASED_BUT_FACTUAL** - True facts with bias
3. **PROPAGANDA** - True facts with misleading framing ⭐ KEY INNOVATION
4. **MISINFORMATION** - Inaccurate, unintentional
5. **DISINFORMATION** - False, deliberate
6. **SATIRICAL** - Humor/satire
7. **CLICK-BAIT** - Low quality for traffic

**Two-Dimensional Scoring:**
- `fact_accuracy_score` (0-100) - Factual correctness
- `deceptiveness_score` (0-100) - How misleading

**Classification Logic:**
- If Accuracy < 40: DISINFORMATION/MISINFORMATION
- If Accuracy > 60 BUT Deceptiveness > 60: **PROPAGANDA** ⭐
- If Accuracy > 80 AND Deceptiveness < 30: LEGITIMATE

**New Detection Patterns:**
- FABRICATION - Made-up information
- SELECTIVE_OMISSION - Cherry-picking facts
- FALSE_CAUSATION - Incorrect cause-effect relationships
- INTENT_FABRICATION - Falsely attributing motives
- EMOTIONAL_MANIPULATION - Exploiting emotions
- MISLEADING_FRAMING - Biased presentation

**Context Analysis:**
- Detects omitted context
- Identifies false connections
- Flags intent fabrication
- Recognizes misleading framing
- Spots false choices/dichotomies

**Technical Changes:**
- Max iterations: 5 (was 1)
- Web search integration
- More sophisticated output structure

#### **Agent 2 - Enhanced Source Analysis:**
- **Publisher Extraction:** For dataset articles, extracts actual publisher from article text (not image sources)
- **Three-Scenario Support:**
  1. Dataset articles → Extract publisher from text
  2. Twitter data → Full analysis
  3. News articles → Domain credibility
- **Web Search Integration:** Uses web_search for verification
- **More Detailed Output:** Includes `source_identified`, `source_type`, `extraction_method`

#### **Backup Agents - True Second Opinions:**
- **New Field:** `comparison_with_primary`
  - `areas_of_agreement`
  - `areas_of_disagreement`
  - `why_different`
- **Philosophy:** "Disagreement is valuable"
- **Independence:** Encouraged to disagree with primary agent
- **Web Search Access:** Can verify independently

### Previous Updates (v2.2 - Dec 7, 2025)

### Major Fixes:
1. **Output Parsing Errors Fixed**
   - Removed `agent: "conversationalAgent"` parameter from all 6 AI agents
   - Added `maxIterations: 1` to force direct output without action wrappers
   - Updated system messages to explicitly forbid markdown formatting
   - Result: Agents now return clean JSON without parsing failures

2. **Backup Agent Logic Fixed**
   - Agent 1B & 2B now receive full prompts (not placeholders)
   - Backup agents get both original content AND primary agent's analysis
   - Confidence check now only triggers on `confidence == "low"` (not verdict-dependent)
   - Result: True second opinions with proper context

3. **Merge Nodes Fixed**
   - Changed from `combine/mergeByPosition` to `append` mode
   - Merge Agent Results now use `$('Agent 1 - Fact Check').item.json.output` to reference primary agents
   - Fixed "Expected 2 inputs, got 1" errors
   - Result: Proper averaging of primary and backup scores

4. **Confidence Check IF Nodes Fixed**
   - Updated to parse JSON output: `JSON.parse($json.output).confidence`
   - Fixed Agent 1 check to only evaluate confidence (removed verdict condition)
   - Result: Backup agents trigger correctly when confidence is low

### Model Updates:
- **Groq (Primary Agents 1, 2, 3):** `meta-llama/llama-4-scout-17b-16e-instruct`
- **Google Gemini (Backup/Decision):** `models/gemini-2.5-flash-lite`
- Parameter name corrected: `modelName` (not `model`) for Gemini

### Component Renaming:
- `Combine All Agent Results` → `Merge Agents 1 & 2`
- `Combine All Agent Results1` → `Merge with Agent 3`
- `Combine All Agent Results2` → `Merge Dataset & Twitter Inputs`

---

## 🚀 Future Roadmap

### Short-term (Next 2-4 weeks):
- [ ] Test Twitter webhook flow
- [ ] Add more test cases
- [ ] Tune agent prompts based on results
- [ ] Add execution monitoring

### Medium-term (1-3 months):
- [ ] Implement Scout Agent (automated Twitter monitoring)
- [ ] Add caching layer for duplicate content
- [ ] Build analytics dashboard (Streamlit)
- [ ] Add human feedback loop
- [ ] Multi-language support

### Long-term (3-6 months):
- [ ] Implement Responder Agent (automated replies)
- [ ] Fine-tune custom models for specific domains
- [ ] Add image/video analysis
- [ ] Coordinated campaign detection
- [ ] A/B testing framework

---

## 💡 Tips for AI Assistants

### When helping with this project:

1. **Always check the workflow file first** - `workflow-twitter-whatsapp-combined.json` is the source of truth

2. **Understand the data flow:**
   - WhatsApp → Supabase → Format → Agents → Decision
   - Twitter → Format → Agents → Decision

3. **Remember the adaptive weighting** - Agent 4 changes weights based on available data

4. **Agent 3 is intentional** - It returns neutral scores for WhatsApp, this is by design

5. **Backup agents are optional** - They only trigger on low confidence

6. **Cost matters** - Always consider LLM API costs when suggesting changes

7. **Check recent updates** - Read `WORKFLOW_UPDATE_SUMMARY.md` for latest changes

8. **Test before suggesting** - Validate JSON syntax if modifying workflow

### Common User Questions:

**"Why is Agent 3 running for WhatsApp?"**
→ It's designed to handle missing data gracefully, returns neutral score

**"Can I remove the backup agents?"**
→ Yes, but you'll lose second opinion capability

**"How do I add Twitter support?"**
→ Just add Twitter API credentials, webhook is already configured

**"Can I change the risk thresholds?"**
→ Yes, edit Agent 4 prompt to modify HIGH/MEDIUM/LOW boundaries

**"Why use both Groq and Gemini?"**
→ Cost optimization (Groq) + independent reasoning (Gemini for backups)

---

## 📞 Contact & Support

### Documentation Files:
- **Quick help:** `START_HERE.txt`
- **Setup:** `QUICK_START.md` or `SETUP_GUIDE.md`
- **Testing:** `IMPORT_AND_TEST_GUIDE.md`
- **Technical:** `PROJECT_SUMMARY.md`
- **Prompts:** `AGENT_PROMPTS.md`

### External Resources:
- n8n Docs: https://docs.n8n.io/
- Groq Docs: https://console.groq.com/docs
- Google Gemini: https://ai.google.dev/docs
- Supabase Docs: https://supabase.com/docs

---

## 🎯 Quick Context Summary (TL;DR)

**What:** Multi-agent misinformation detection system in n8n  
**Input:** WhatsApp messages (manual) or Twitter viral tweets (automated, 1 per execution)  
**Agents:** 6 AI agents (3 primary Groq + 2 backup Gemini + 1 decision Gemini)  
**Output:** Risk level (HIGH/MEDIUM/LOW) + detailed analysis + Google Sheets logging  
**Status:** WhatsApp ✅ | Twitter ✅ | Google Sheets ✅ | Optimized Prompts ✅  
**Cost:** ~$0.003-0.018 per item analyzed  
**Latest:** Prompt optimization with partial verification logic, source credibility override, 10% size reduction (Dec 14, 2025)  
**Key Features:** Condensed prompts, weighted scoring, source override, safety-first architecture, 172KB workflow  

---

**Last Updated:** December 14, 2025  
**Version:** 5.2 (Prompt Optimization & Refinement)  
**Maintained by:** MSC Student (Final Project)

---

## 🆕 v5.2 Major Changes (December 14, 2025)

### **Prompt Optimization:**
- **File Size:** 172KB (was 191KB) - **10% reduction**
- **Agent 1A/4 Prompts:** Condensed by 100-300 lines each
- **Structure:** Better organized, clearer instructions, less redundancy
- **Readability:** Bullet points, concise format, easier to scan

### **New Features:**
- **Partial Verification Logic:** Weighted scoring for TRUE core + UNVERIFIED details
- **Source Credibility Override:** Context labels even when facts TRUE but source LOW

### **Maintained:**
- All v5.1 functionality (safety checks, bug fixes)
- Classification-specific handling
- Safety-first architecture

---

## 📜 v5.1 Major Changes (December 14, 2025)

### **Critical Bug Fix: UNVERIFIED ≠ LEGITIMATE**
- **Before:** Can't verify claims → LEGITIMATE (score 100) ❌
- **After:** Can't verify claims → UNVERIFIABLE (score 50) ✅

### **Agent 1A Enhancements:**
- **STEP 0: Safety & Parody Check** (runs FIRST)
  - Hate content detection
  - Incitement/coordination detection
  - Parody disclosure check
- **New Classifications:** HATE_CONTENT, SATIRE
- **Enhanced Verification:** Added "Did I confuse UNVERIFIED with LEGITIMATE?" check

### **Agent 4 Enhancements:**
- **STEP 0: Safety Classification Override** (runs FIRST)
  - HATE_CONTENT → Force HIGH risk, immediate action
  - SATIRE → Force MEDIUM risk, add label
- **Classification-Specific Actions:**
  - Different handling per type (not one-size-fits-all)
- **Government Source Weighting:** 45% (was 30%)
- **Very Low Source Penalty:** Additional 15% penalty for score < 40

### **Statistics:**
- 191KB (was 202KB) - optimized
- Safety-first architecture
- Bug fixes for UNVERIFIED classification

---

## 📜 v5.0 Major Changes (December 13, 2025)

### **Pre-Fetch Search System:**

**Innovation:** Pre-fetch credible sources BEFORE Agent 1 runs

**Flow:**
```
Tweet → Extract Search Terms → Google API → Filter Sources → Agent 1
```

**New Nodes:**
- "1. Extract Search Terms" - Smart query building
- "2. Search Google" - Google Custom Search API
- "3. Filter Credible Sources" - 3-tier ranking system

**Benefits:**
- No URL fabrication (Agent 1 gets real URLs)
- Better search quality (dedicated code nodes)
- Source filtering (Tier 1/2/3 system)
- Semantic guidance ("interest" vs. "confirmation")

### **Agent 1 Complete Rewrite:**

**New Sections:**
- **Semantic Analysis** - Teaches COMPLETED vs. INTEREST/SPECULATION
- **Reality Check Exercise** - Forces analysis of each result
- **Absolute Rules** - No URL fabrication, interest ≠ confirmation
- **Mandatory Pre-Output Verification** - 4-question checklist

**Source Tiers:**
- **Tier 1**: Reuters, AP, NYT, BBC (top-tier)
- **Tier 2**: Regional, specialized, official bodies (MLB.com, NFL.com)
- **Tier 3**: ESPN, TMZ, UK tabloids
- **Excluded**: Twitter, Reddit, YouTube

**Statistics:**
- 202KB (was 133KB)
- 83 nodes (was 57)
- 900+ line Agent 1 prompt

---

## 📜 v4.0 Major Changes (December 11, 2025)

### **Enhanced Agent Prompts:**

#### **Agent 1 (Fact Check) - New Features:**
- **Breaking News Verification Protocol**
  - Extracts tweet date from metadata: `{{ $json.tweetMetadata.created_at }}`
  - Compares to current date: `{{ $now.format('YYYY-MM-DD') }}`
  - Requires date-appropriate sources (±30 days of tweet)
  - New classification: **"UNVERIFIABLE"** when credible sources unavailable
- **Source Quality Guidelines**
  - Prioritizes: Reuters, AP, BBC, official .gov/.edu, fact-checkers
  - Flags: blogs, unverified social media, partisan sources
  - Requires 3+ credible sources for high confidence
- **Date-Aware Searches**
  - Includes month/year in web_search queries
  - Prevents anachronistic verification (e.g., using 2020 sources for 2025 claims)

#### **Agent 2 (Credibility) - New Features:**
- **Mandatory External Verification**
  - `sources_checked` field CANNOT be empty for Twitter
  - Minimum 2 web_search queries required
  - Searches: "[username] Twitter credibility", "[username] bias fact check"
- **Political Bias Detection**
  - Flags: "BRICS News", partisan language, geopolitical commentary
  - Score penalties: -5 to -15 points for bias
  - Red flag for tweets_per_day > 50
- **Dynamic Score Adjustment**
  - Base score from account metrics
  - Adjusted by external reputation findings
  - Known misinformation sources: -30 points

### **Dual-Path Architecture:**
```
Get Top N Most Viral
  ├─→ Enrich Twitter Account Data → Merge Enriched Data → Merge2
  └─→ (direct) ────────────────────────────────────────→ Merge2
                                                            ↓
                                               Build Final Enriched Data
```
- **Benefits**: Original data preserved, fallback logic, separation of concerns
- **Fixed**: HTTP node now uses `outputPropertyName: "enrichmentData"`

### **Workflow Size:**
- **v3.3**: 90KB, ~40 nodes
- **v4.0**: 133KB, 57 nodes
- **Reason**: Massively enhanced prompts with detailed protocols

---

## 🔄 How to Use This File

### For Future AI Assistants:
1. Read this entire file first
2. Check `COMPARISON_v3_vs_v4.md` for architectural changes
3. Review `workflow-misinformation-detection-fixed.json` for current state (v4.0)
4. Ask clarifying questions before making changes

### For the Student:
1. Share this file at the start of new AI chat sessions
2. Update this file when making significant changes
3. Reference specific sections when asking questions
4. Keep this file in sync with actual workflow

---

**End of AI Context File**

