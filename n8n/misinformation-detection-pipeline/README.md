# N8N Misinformation Detection Pipeline

## Overview

This N8N workflow provides automated fact-checking and misinformation detection for tweets and text messages using a multi-agent AI system.

## Architecture

### Two Input Methods

1. **Automated (Webhook)** - Receives list of tweets from Twitter API
2. **Manual (WhatsApp)** - Receives single sentence/text input from WhatsApp

### AI Agents

#### Primary Agents

1. **Agent 1: Fact-Check Agent** (LLM: Google Gemini)
   - Verifies factual accuracy of claims
   - Uses professional fact-checking sites
   - Returns verdict: TRUE/MOSTLY_TRUE/MIXED/MOSTLY_FALSE/FALSE/UNVERIFIABLE
   - Confidence: high/medium/low

2. **Agent 2: Credibility Agent** (LLM: Google Gemini)
   - Evaluates source trustworthiness (MBFC, NewsGuard)
   - Bot behavior detection heuristics
   - Returns credibility score (0-100)

3. **Agent 3: Twitter Check Agent** (LLM: Google Gemini)
   - **Only for Webhook/Twitter flow**
   - Analyzes account behavior patterns
   - Tweet frequency, profile completeness, account age
   - Returns authenticity score (0-100)

4. **Agent 4: Decision Agent** (LLM: Google Gemini)
   - Synthesizes all agent outputs
   - Calculates composite risk score
   - Returns: HIGH/MEDIUM/LOW risk classification

#### Backup Agents (Second Opinion)

5. **Agent 1B: Fact-Check Backup** (LLM: Different from Agent 1, e.g., Claude/GPT-4)
   - Triggered when Agent 1 has low confidence or returns UNVERIFIABLE
   - Uses same sources, different reasoning approach

6. **Agent 2B: Source Trust Backup** (LLM: Different from Agent 2, e.g., Claude/GPT-4)
   - Triggered when Agent 2 has low confidence
   - Independent second opinion on source credibility

**Conflict Resolution:** If primary and backup agents disagree, their scores are averaged.

## Workflow Logic

### Twitter/Webhook Flow
```
Webhook Input (tweets)
    ↓
Parse Tweet Data
    ↓
┌───────────────┬─────────────────┬──────────────────┐
│   Agent 1     │    Agent 2      │     Agent 3      │
│ (Fact-Check)  │ (Credibility)   │ (Twitter Check)  │
└───────┬───────┴────────┬────────┴────────┬─────────┘
        ↓                ↓                 ↓
    [if low confidence]
        ↓                ↓
    Agent 1B         Agent 2B
        ↓                ↓
        └────────┬───────┘
                 ↓
            Agent 4 (Decision)
                 ↓
        Final Risk Assessment
```

### WhatsApp/Manual Flow
```
WhatsApp Input (text)
    ↓
Parse Message
    ↓
┌───────────────┬─────────────────┐
│   Agent 1     │    Agent 2      │
│ (Fact-Check)  │ (Credibility)   │
└───────┬───────┴────────┬────────┘
        ↓                ↓
    [if low confidence]
        ↓                ↓
    Agent 1B         Agent 2B
        ↓                ↓
        └────────┬───────┘
                 ↓
            Agent 4 (Decision)
                 ↓
        Final Risk Assessment
```

## Prerequisites

### N8N Setup
- N8N instance (self-hosted or cloud)
- N8N version 1.0+ recommended

### API Keys Required

1. **Google Gemini API Key** (Primary LLM)
   - Get from: https://makersuite.google.com/app/apikey
   - Used for: Agent 1, 2, 3, 4

2. **Alternative LLM API Key** (Backup Agents)
   - Options: OpenAI (GPT-4), Anthropic (Claude), etc.
   - Get from: https://platform.openai.com/ or https://console.anthropic.com/
   - Used for: Agent 1B, 2B

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

1. **Import Workflows**
   ```bash
   # Copy workflow JSON files to your N8N instance
   # Import via N8N UI: Workflows → Import from File
   ```

2. **Configure Credentials**
   - Go to N8N → Credentials
   - Add Google Gemini API credentials
   - Add backup LLM API credentials (OpenAI/Claude)
   - Add Twitter API credentials (if using webhook)
   - Add WhatsApp credentials (if using manual)

3. **Set Webhook URL**
   - Activate webhook workflow
   - Copy webhook URL
   - Configure your Twitter integration to send data to this URL

4. **Test Workflows**
   - Start with manual workflow (simpler)
   - Send test message via WhatsApp
   - Verify all agents execute correctly

## Configuration

### Agent LLM Assignment

**Primary Agents:** Google Gemini
- Agent 1: Fact-Check
- Agent 2: Credibility
- Agent 3: Twitter Check
- Agent 4: Decision

**Backup Agents:** Alternative LLM (Claude/GPT-4)
- Agent 1B: Fact-Check Backup
- Agent 2B: Source Trust Backup

### Scoring Weights (Agent 4)

```
Composite Risk Score = 
  (Fact Check Score × 0.50) + 
  (Source Credibility × 0.30) + 
  (Account Authenticity × 0.20)
```

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

```json
{
  "final_assessment": {
    "risk_level": "HIGH/MEDIUM/LOW",
    "composite_score": 45,
    "confidence": "HIGH/MEDIUM/LOW"
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

## Cost Estimation

### Per Tweet Analysis (Webhook Flow)

- Agent 1 (Gemini): ~$0.01
- Agent 2 (Gemini): ~$0.01
- Agent 3 (Gemini): ~$0.01
- Agent 4 (Gemini): ~$0.005
- Agent 1B (if triggered, GPT-4): ~$0.03
- Agent 2B (if triggered, GPT-4): ~$0.03

**Average cost per tweet:** $0.03-$0.10 (depending on backup agent triggers)

### Monthly Estimates

- 100 tweets/day: ~$90-300/month
- 1,000 tweets/day: ~$900-3,000/month

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

## License

MIT License - Feel free to modify and adapt for your use case.

## Contributing

Feedback and improvements welcome! This is a living system that should evolve with new misinformation tactics.
