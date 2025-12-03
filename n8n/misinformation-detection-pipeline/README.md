# N8N Misinformation Detection Pipeline

**Last Updated:** December 3, 2025  
**Version:** 2.0 - Combined Twitter & WhatsApp Support

## Overview

This N8N workflow provides automated fact-checking and misinformation detection for tweets and text messages using a multi-agent AI system with graceful handling of missing data across multiple input sources.

## Architecture

### Three Input Methods

1. **Twitter Webhook (Automated)** - Receives tweets with full metadata from Twitter API
2. **WhatsApp (Manual)** - Receives text messages via WhatsApp Business API with Supabase integration
3. **Combined Flow** - Unified workflow that handles both Twitter and WhatsApp inputs seamlessly

### Recent Updates (Dec 3, 2025)

- ✅ **Unified Workflow:** Single workflow handles both Twitter and WhatsApp inputs
- ✅ **Graceful Data Handling:** Agents intelligently handle missing Twitter metadata when processing WhatsApp messages
- ✅ **Adaptive Risk Scoring:** Agent 4 adjusts weighting based on available data
- ✅ **Groq LLM Integration:** Added Groq as primary LLM provider for faster processing
- ✅ **Format Input Data Node:** Automatic detection and formatting of input source type

### AI Agents

#### Primary Agents

1. **Agent 1: Fact-Check Agent** (LLM: Groq)
   - Verifies factual accuracy of claims
   - Uses professional fact-checking sites
   - Returns verdict: TRUE/MOSTLY_TRUE/MIXED/MOSTLY_FALSE/FALSE/UNVERIFIABLE
   - Confidence: high/medium/low
   - **Works with all input types**

2. **Agent 2: Credibility Agent** (LLM: Groq)
   - Evaluates source trustworthiness (MBFC, NewsGuard)
   - Bot behavior detection heuristics
   - Returns credibility score (0-100)
   - **Handles missing Twitter data:** Returns neutral score (50) with 'NOT_APPLICABLE' when source data unavailable

3. **Agent 3: Twitter Check Agent** (LLM: Groq)
   - Analyzes account behavior patterns
   - Tweet frequency, profile completeness, account age
   - Returns authenticity score (0-100)
   - **Handles missing Twitter data:** Returns neutral score (50) with 'NOT_APPLICABLE' when account data unavailable

4. **Agent 4: Decision Agent** (LLM: Google Gemini)
   - Synthesizes all agent outputs
   - Calculates composite risk score with adaptive weighting
   - Returns: HIGH/MEDIUM/LOW risk classification
   - **Adaptive Scoring:**
     - Full data: Fact (50%) + Source (30%) + Account (20%)
     - Partial data: Fact (70%) + Available (30%)
     - Fact-check only: Fact (100%)

#### Backup Agents (Second Opinion)

5. **Agent 1B: Fact-Check Backup** (LLM: Different from Agent 1, e.g., Claude/GPT-4)
   - Triggered when Agent 1 has low confidence or returns UNVERIFIABLE
   - Uses same sources, different reasoning approach

6. **Agent 2B: Source Trust Backup** (LLM: Different from Agent 2, e.g., Claude/GPT-4)
   - Triggered when Agent 2 has low confidence
   - Independent second opinion on source credibility

**Conflict Resolution:** If primary and backup agents disagree, their scores are averaged.

## Workflow Logic

### Combined Unified Flow (v2.0)
```
┌─────────────────────┐         ┌──────────────────────┐
│  Twitter Webhook    │         │  WhatsApp Trigger    │
│  (Full Metadata)    │         │  → Code → AI Agent   │
└──────────┬──────────┘         │  → Supabase Lookup   │
           │                    └──────────┬───────────┘
           │                               │
           └───────────┬───────────────────┘
                       ↓
              Combine All Agent Results2
                       ↓
              Format Input Data (NEW!)
              (Auto-detects source type)
                       ↓
              Parse Input Data
              (Handles missing fields)
                       ↓
        ┌──────────────┼──────────────┐
        ↓              ↓              ↓
    Agent 1        Agent 2        Agent 3
  (Fact-Check)  (Credibility)  (Twitter Check)
   [Groq LLM]    [Groq LLM]     [Groq LLM]
        │              │              │
        │    [if low confidence]      │
        ↓              ↓              │
    Agent 1B       Agent 2B           │
    [Gemini]       [Gemini]           │
        │              │              │
        └──────┬───────┴──────────────┘
               ↓
        Combine All Agent Results
               ↓
        Combine All Agent Results1
               ↓
        Agent 4 (Decision)
        [Gemini - Adaptive Scoring]
               ↓
        Final Risk Assessment
               ↓
        Respond to Webhook
```

### Key Features:
- **Automatic Source Detection:** Format Input Data node identifies Twitter vs WhatsApp
- **Graceful Degradation:** Agents handle missing data without errors
- **Adaptive Weighting:** Agent 4 adjusts scoring based on available data
- **Unified Output:** Same JSON structure regardless of input source

## Prerequisites

### N8N Setup
- N8N instance (self-hosted or cloud)
- N8N version 1.0+ recommended

### API Keys Required

1. **Groq API Key** (Primary LLM - Fast & Free Tier Available)
   - Get from: https://console.groq.com/
   - Used for: Agent 1, 2, 3 (Primary agents)
   - Models: llama-3.1-70b-versatile, mixtral-8x7b

2. **Google Gemini API Key** (Backup & Decision Agent)
   - Get from: https://makersuite.google.com/app/apikey
   - Used for: Agent 1B, 2B (Backup agents), Agent 4 (Decision)
   - Model: gemini-1.5-pro

3. **Supabase Account** (For WhatsApp data storage)
   - Get from: https://supabase.com/
   - Used for: Storing and retrieving fact-check data
   - Table required: `false-news` with `id` and `text` columns

3. **Twitter API v2** (For webhook flow)
   - Elevated access required
   - Get from: https://developer.twitter.com/
   - Needed fields: account metadata, recent tweets

4. **WhatsApp Business API** (For manual flow)
   - Get from: https://business.whatsapp.com/
   - Or use N8N's WhatsApp Trigger node

### Optional APIs (Enhance accuracy)

5. **Media Bias/Fact Check (MBFC)** - May require subscription
6. **NewsGuard API** - Commercial service
7. **WHOIS API** - For domain age checks

## Installation

### Available Workflow Files

1. **`workflow-twitter-whatsapp-combined.json`** ⭐ **RECOMMENDED**
   - Unified workflow supporting both Twitter and WhatsApp
   - Handles missing data gracefully
   - Latest version with all improvements

2. **`workflow-twitter-automated.json`**
   - Twitter-only automated webhook flow
   - Legacy version

3. **`workflow-twitter-webhook.json`**
   - Original Twitter webhook implementation

4. **`workflow-whatsapp-manual.json`**
   - WhatsApp-only manual flow

### Setup Steps

1. **Import Workflow**
   ```bash
   # Import via N8N UI: Workflows → Import from File
   # Choose: workflow-twitter-whatsapp-combined.json
   ```

2. **Configure Credentials**
   - Go to N8N → Credentials
   - Add **Groq API** credentials (primary agents)
   - Add **Google Gemini API** credentials (backup + decision agent)
   - Add **Supabase** credentials (for WhatsApp data storage)
   - Add **Twitter API** credentials (if using Twitter webhook)
   - Add **WhatsApp Business API** credentials (if using WhatsApp)

3. **Setup Supabase Table** (for WhatsApp flow)
   ```sql
   CREATE TABLE "false-news" (
     id INTEGER PRIMARY KEY,
     text TEXT NOT NULL,
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

4. **Activate Webhook**
   - Activate the workflow
   - Copy webhook URL from "Webhook - Twitter Input" node
   - Configure your Twitter integration to POST to this URL

5. **Test Both Flows**
   - **Twitter:** Send POST request to webhook with tweet data
   - **WhatsApp:** Send message with ID number to retrieve from Supabase
   - Verify all agents execute and handle data correctly

## Configuration

### Agent LLM Assignment (v2.0)

**Primary Agents:** Groq (Fast, Cost-Effective)
- Agent 1: Fact-Check → Groq (llama-3.1-70b)
- Agent 2: Credibility → Groq (llama-3.1-70b)
- Agent 3: Twitter Check → Groq (llama-3.1-70b)

**Backup Agents:** Google Gemini (Second Opinion)
- Agent 1B: Fact-Check Backup → Gemini 1.5 Pro
- Agent 2B: Source Trust Backup → Gemini 1.5 Pro

**Decision Agent:** Google Gemini (Synthesis)
- Agent 4: Decision → Gemini 1.5 Pro

### Adaptive Scoring Weights (Agent 4 - v2.0)

**Full Data Available (Twitter Flow):**
```
Composite Risk Score = 
  (Fact Check Score × 0.50) + 
  (Source Credibility × 0.30) + 
  (Account Authenticity × 0.20)
```

**Partial Data (WhatsApp Flow - No Twitter Metadata):**
```
Composite Risk Score = 
  (Fact Check Score × 0.70) + 
  (Source Credibility × 0.30)
  
  Account Authenticity = 50 (neutral, NOT_APPLICABLE)
```

**Fact-Check Only (Minimal Data):**
```
Composite Risk Score = Fact Check Score × 1.00
```

The system automatically detects available data and adjusts weights accordingly.

### Risk Thresholds

- **HIGH RISK:** 0-40 (Flag/Remove)
- **MEDIUM RISK:** 41-70 (Add context label)
- **LOW RISK:** 71-100 (No action)

## Usage

### Webhook (Automated)

Send POST request to webhook URL:

```json
{
  "tweets": [
    {
      "tweetText": "Breaking: Scientists discover...",
      "tweetSource": "https://example.com/article",
      "tweetMetadata": {
        "account_handle": "@username",
        "account_created_date": "2020-01-15",
        "follower_count": 5000,
        "following_count": 500,
        "tweet_count": 12000,
        "bio": "Science journalist",
        "profile_image_url": "https://...",
        "verified": false
      }
    }
  ]
}
```

### Manual (WhatsApp)

Simply send a text message to your WhatsApp Business number:

```
"Breaking: Scientists discover cure for common cold"
```

## Output Format

### v2.0 Enhanced Output

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
    "Source flagged as low credibility by MBFC"
  ],
  "recommended_action": {
    "primary_action": "Flag for review and add warning label",
    "rationale": "False claims from unreliable source",
    "urgency": "within_24h"
  },
  "human_review_needed": true,
  "summary": "Tweet contains false health claims from unreliable source. Recommend immediate review."
}
```

## Troubleshooting

### Common Issues

1. **"Agent returned low confidence"**
   - Expected behavior - backup agents will be triggered
   - Check if backup agents executed successfully

2. **"Twitter API rate limit exceeded"**
   - Implement rate limiting in webhook
   - Consider caching account data

3. **"Fact-checking sites unreachable"**
   - Implement fallback to alternative sources
   - Add retry logic with exponential backoff

4. **"MBFC/NewsGuard not accessible"**
   - These may require paid subscriptions
   - Consider using free alternatives or web scraping

## Cost Estimation (v2.0 - Groq + Gemini)

### Per Analysis Cost

**Primary Agents (Groq - Free Tier Available):**
- Agent 1 (Groq): ~$0.001 (or FREE on free tier)
- Agent 2 (Groq): ~$0.001 (or FREE on free tier)
- Agent 3 (Groq): ~$0.001 (or FREE on free tier)

**Backup Agents (Google Gemini):**
- Agent 1B (if triggered): ~$0.005
- Agent 2B (if triggered): ~$0.005

**Decision Agent (Google Gemini):**
- Agent 4: ~$0.005

**Average cost per analysis:** 
- Without backups: ~$0.008 (or FREE with Groq free tier)
- With backups: ~$0.018

### Monthly Estimates

**Using Groq Free Tier:**
- 100 messages/day: ~$15/month (Gemini only)
- 1,000 messages/day: ~$150/month

**Using Groq Paid Tier:**
- 100 messages/day: ~$24/month
- 1,000 messages/day: ~$240/month

**Cost Savings:** ~90% reduction compared to v1.0 (all Gemini/GPT-4)

## Customization

### Adjusting Risk Weights

Edit Agent 4 prompt to change weight distribution:

```javascript
// Current: Fact (50%), Source (30%), Account (20%)
// Adjust based on your priorities
Risk Score = (Fact × 0.50) + (Source × 0.30) + (Account × 0.20)
```

### Adding New Fact-Check Sources

Edit Agent 1 prompt, add to source list:

```
4. Your New Source:
   - https://newfactchecker.com/
```

### Changing LLM Providers

- Replace Google Gemini nodes with OpenAI/Claude/etc.
- Update credentials
- Adjust prompt formatting if needed

## Support & Maintenance

### Monitoring

- Track false positive/negative rates
- Monitor API costs
- Review human moderator feedback

### Optimization

- A/B test different weight configurations
- Fine-tune confidence thresholds
- Update fact-checking source priorities

## Version History

### v2.0 (December 3, 2025)
- ✅ Unified Twitter + WhatsApp workflow
- ✅ Graceful handling of missing data
- ✅ Adaptive risk scoring based on available data
- ✅ Groq LLM integration for cost reduction
- ✅ Format Input Data node for automatic source detection
- ✅ 90% cost reduction vs v1.0

### v1.0 (Initial Release)
- Basic Twitter webhook flow
- Separate WhatsApp manual flow
- Google Gemini + GPT-4 agents

## License

MIT License - Feel free to modify and adapt for your use case.

## Contributing

Feedback and improvements welcome! This is a living system that should evolve with new misinformation tactics.

## Author

MSC Final Project - Misinformation Detection System  
Last Updated: December 3, 2025
