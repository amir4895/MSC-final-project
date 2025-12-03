# Project Summary - N8N Misinformation Detection Pipeline

## Overview

This project implements a sophisticated multi-agent AI system for detecting misinformation in tweets and text messages using N8N workflow automation.

---

## What We Built

### 🎯 Core System

**6 AI Agents working together:**

1. **Agent 1: Fact-Check Agent** (Google Gemini)
   - Verifies factual claims using professional fact-checkers
   - Returns: TRUE/MOSTLY_TRUE/MIXED/MOSTLY_FALSE/FALSE/UNVERIFIABLE
   - Score: 0-100

2. **Agent 2: Credibility Agent** (Google Gemini)
   - Evaluates source trustworthiness (MBFC, NewsGuard)
   - Detects bot behavior patterns
   - Score: 0-100

3. **Agent 3: Twitter Check Agent** (Google Gemini)
   - Analyzes Twitter account behavior
   - Tweet frequency, profile completeness, account age
   - Score: 0-100
   - **Note:** Only runs for Twitter/webhook flow, NOT for WhatsApp

4. **Agent 4: Decision Agent** (Google Gemini)
   - Synthesizes all agent outputs
   - Calculates composite risk score
   - Returns: HIGH/MEDIUM/LOW risk classification

5. **Agent 1B: Backup Fact-Check** (OpenAI GPT-4 or Claude)
   - Second opinion when Agent 1 is uncertain
   - Uses different LLM for independent reasoning
   - Triggered on low confidence or UNVERIFIABLE verdict

6. **Agent 2B: Backup Credibility** (OpenAI GPT-4 or Claude)
   - Second opinion when Agent 2 is uncertain
   - Uses different LLM for independent reasoning
   - Triggered on low confidence

### 🔄 Two Workflows

**1. Twitter Webhook (Automated)**
- Receives tweets via HTTP webhook
- Analyzes all 3 dimensions: Facts + Source + Account
- Returns JSON risk assessment
- Use case: Automated Twitter monitoring

**2. WhatsApp Manual (User-Initiated)**
- Receives text via WhatsApp message
- Analyzes 2 dimensions: Facts + Source (no account data)
- Returns user-friendly WhatsApp reply
- Use case: On-demand fact-checking for users

---

## Key Features

✅ **Multi-Agent Architecture** - 6 specialized AI agents  
✅ **Backup System** - Second opinions when uncertain  
✅ **Dual Input Methods** - Webhook or WhatsApp  
✅ **Conflict Resolution** - Averages scores when agents disagree  
✅ **Risk Scoring** - Quantitative 0-100 score + HIGH/MEDIUM/LOW classification  
✅ **Source Verification** - Checks MBFC, NewsGuard, fact-checking sites  
✅ **Bot Detection** - Identifies automated/suspicious accounts  
✅ **Contextual Adjustments** - Considers topic sensitivity (health, elections)  
✅ **Human Review Flagging** - Escalates uncertain cases  

---

## Technical Architecture

### Workflow Flow (Twitter)

```
Webhook Input
    ↓
Parse Tweet Data
    ↓
┌─────────────┬──────────────┬───────────────┐
│  Agent 1    │   Agent 2    │   Agent 3     │
│ (Fact)      │ (Credibility)│ (Twitter)     │
│ [Parallel]  │  [Parallel]  │  [Parallel]   │
└──────┬──────┴──────┬───────┴───────┬───────┘
       │             │               │
       └─────────────┴───────────────┘
                     ↓
           Combine Agent Outputs
                     ↓
         Check if Backup Needed?
                     ↓
         ┌───────────┴───────────┐
         │ YES                   │ NO
         ↓                       ↓
    ┌────────┬────────┐     Skip to Agent 4
    │Agent 1B│Agent 2B│
    └────┬───┴───┬────┘
         │       │
         └───┬───┘
             ↓
    Merge Backup Results
    (Average scores)
             ↓
        Agent 4 (Decision)
             ↓
      Webhook Response
```

### Workflow Flow (WhatsApp)

```
WhatsApp Message
    ↓
Parse Message
    ↓
┌─────────────┬──────────────┐
│  Agent 1    │   Agent 2    │
│ (Fact)      │ (Credibility)│
│ [Parallel]  │  [Parallel]  │
└──────┬──────┴──────┬───────┘
       │             │
       └──────┬──────┘
              ↓
    Combine Agent Outputs
              ↓
    Check if Backup Needed?
              ↓
         [Same as above]
              ↓
       Agent 4 (Decision)
              ↓
    Format WhatsApp Response
              ↓
    Send WhatsApp Reply
```

---

## Decision Logic

### Risk Score Calculation

**Twitter Flow (with Agent 3):**
```
Risk Score = (Fact Check × 0.50) + (Source × 0.30) + (Account × 0.20)
```

**WhatsApp Flow (without Agent 3):**
```
Risk Score = (Fact Check × 0.65) + (Source × 0.35)
```

### Risk Classification

| Score | Risk Level | Action |
|-------|-----------|--------|
| 0-40 | HIGH | Flag/Remove, Warning Label |
| 41-70 | MEDIUM | Add Context, Monitor |
| 71-100 | LOW | No Action Needed |

### Backup Agent Triggers

```javascript
if (agent1.confidence === "low" || 
    agent1.verdict === "UNVERIFIABLE") {
  trigger_agent_1B();
}

if (agent2.confidence === "low") {
  trigger_agent_2B();
}

// If both agents run, average their scores
final_score = (primary_score + backup_score) / 2;
```

---

## Files Created

### Documentation
- **README.md** - Project overview and architecture
- **QUICK_START.md** - 5-minute setup guide
- **SETUP_GUIDE.md** - Detailed installation and configuration
- **AGENT_PROMPTS.md** - Complete prompts for all 6 agents
- **EXAMPLES.md** - Test cases and example payloads
- **PROJECT_SUMMARY.md** - This file

### N8N Workflows
- **workflow-twitter-webhook.json** - Twitter/webhook workflow
- **workflow-whatsapp-manual.json** - WhatsApp/manual workflow

---

## Requirements

### APIs Required

1. **Google Gemini API** (Primary LLM)
   - Cost: Free tier available (60 req/min)
   - Used for: Agent 1, 2, 3, 4

2. **OpenAI API** (Backup LLM)
   - Cost: Pay-as-you-go (~$0.03/call with GPT-4)
   - Used for: Agent 1B, 2B
   - Alternative: Anthropic Claude

3. **Twitter API v2** (Optional - for webhook flow)
   - Cost: Free tier available (500k tweets/month)
   - Access level: Elevated (for account metadata)

4. **WhatsApp Business API** (Optional - for manual flow)
   - Cost: Varies by provider (~$0.005/message)
   - Options: Official API, Twilio, MessageBird

### Optional APIs (Enhance Accuracy)

5. **Media Bias/Fact Check (MBFC)** - May require subscription
6. **NewsGuard API** - Commercial service
7. **WHOIS API** - For domain age checks

---

## Cost Estimates

### Per Analysis

**Without Backup Agents:**
- Agent 1 (Gemini): $0.004
- Agent 2 (Gemini): $0.004
- Agent 3 (Gemini): $0.004
- Agent 4 (Gemini): $0.003
- **Total: ~$0.015**

**With Backup Agents (30% trigger rate):**
- Above + Agent 1B (GPT-4): $0.030
- Above + Agent 2B (GPT-4): $0.030
- **Total: ~$0.085** (when triggered)

### Monthly Estimates

| Volume | Cost (No Backup) | Cost (With Backup) |
|--------|-----------------|-------------------|
| 1,000 | $15 | $60-85 |
| 10,000 | $150 | $600-850 |
| 100,000 | $1,500 | $6,000-8,500 |

**Cost Optimization:**
- Use GPT-3.5-turbo instead of GPT-4 (10x cheaper)
- Increase confidence thresholds to reduce backup triggers
- Cache results for identical content
- Use Gemini for all agents (cheaper)

---

## Performance

### Response Times

- **Without Backup:** 5-10 seconds
- **With Backup:** 15-25 seconds
- **Multiple Tweets (5):** 10-15 seconds (parallel processing)

### Accuracy Targets

- **False Positive Rate:** <10% (flagged as misinfo but actually true)
- **False Negative Rate:** <5% (missed actual misinfo)
- **Backup Trigger Rate:** 20-30% (optimal)

---

## Use Cases

### 1. Social Media Platform Moderation
- Automated content moderation
- Flag high-risk posts for human review
- Add context labels to uncertain claims

### 2. News Organization Fact-Checking
- Rapid verification of breaking news
- Source credibility assessment
- Bot detection for coordinated campaigns

### 3. Personal Fact-Checking Assistant
- WhatsApp bot for on-demand verification
- Help users verify claims before sharing
- Educational tool for media literacy

### 4. Research & Analysis
- Track misinformation trends
- Analyze coordinated disinformation campaigns
- Study bot behavior patterns

---

## Customization Options

### 1. Adjust Risk Weights
Edit Agent 4 prompt to change scoring priorities:
```javascript
// More emphasis on source credibility
Risk = (Fact × 0.40) + (Source × 0.40) + (Account × 0.20)
```

### 2. Change Risk Thresholds
Modify risk level boundaries:
```javascript
// More strict
HIGH: 0-35 (instead of 0-40)
MEDIUM: 36-75 (instead of 41-70)
LOW: 76-100 (instead of 71-100)
```

### 3. Add New Fact-Check Sources
Edit Agent 1 prompt to include additional sources:
```
4. Your Custom Source:
   - https://yourcustomfactchecker.com/
```

### 4. Change Backup LLM
Replace OpenAI with Claude:
- Delete Agent 1B/2B nodes
- Add Claude nodes
- Configure Anthropic credentials

### 5. Add Notifications
Add email/Slack alerts for high-risk detections:
- Add IF node after Agent 4
- Condition: `risk_level === "HIGH"`
- Add notification node

---

## Security Considerations

### Production Deployment

1. **Webhook Authentication**
   - Add API key authentication
   - Use JWT tokens
   - Rate limiting

2. **Data Privacy**
   - GDPR compliance
   - Don't log sensitive user data
   - Anonymize analytics

3. **API Key Security**
   - Use environment variables
   - Rotate keys regularly
   - Monitor usage for anomalies

4. **Input Validation**
   - Sanitize webhook inputs
   - Validate JSON structure
   - Prevent injection attacks

---

## Monitoring & Maintenance

### Weekly Tasks
- [ ] Review execution logs
- [ ] Check API usage and costs
- [ ] Review false positive/negative cases
- [ ] Monitor backup agent trigger rate

### Monthly Tasks
- [ ] Update fact-checking source list
- [ ] Tune risk thresholds based on feedback
- [ ] Review and update agent prompts
- [ ] Check for N8N updates
- [ ] Analyze accuracy metrics

### Quarterly Tasks
- [ ] Audit overall system performance
- [ ] Review and optimize costs
- [ ] Update documentation
- [ ] Train team members
- [ ] A/B test different configurations

---

## Limitations & Considerations

### Current Limitations

1. **Language Support**
   - Primarily designed for English
   - May need adjustments for other languages

2. **Real-Time Verification**
   - Fact-checking takes 5-25 seconds
   - Not suitable for real-time filtering

3. **Context Understanding**
   - May struggle with heavy sarcasm/satire
   - Cultural context may be missed

4. **Source Coverage**
   - Limited to known fact-checking sources
   - New/niche sources may not be rated

5. **Cost at Scale**
   - Can be expensive for high volumes
   - Requires cost optimization strategies

### Future Improvements

- [ ] Multi-language support
- [ ] Image/video analysis
- [ ] Historical trend analysis
- [ ] Coordinated campaign detection
- [ ] Fine-tuned models for specific domains
- [ ] Real-time caching layer
- [ ] A/B testing framework
- [ ] Feedback loop from human moderators

---

## Success Metrics

### Accuracy Metrics
- False positive rate: <10%
- False negative rate: <5%
- Human review agreement rate: >85%

### Performance Metrics
- Average response time: <10s (no backup)
- 95th percentile: <30s (with backup)
- API failure rate: <1%

### Cost Metrics
- Cost per analysis: <$0.10
- Monthly cost predictability: ±15%

### Usage Metrics
- Daily analyses: Track growth
- Risk distribution: HIGH/MEDIUM/LOW ratio
- Backup trigger rate: 20-30%

---

## Getting Started

### For Quick Testing (5 minutes)
→ See [QUICK_START.md](QUICK_START.md)

### For Production Setup (30 minutes)
→ See [SETUP_GUIDE.md](SETUP_GUIDE.md)

### For Understanding Agents (15 minutes)
→ See [AGENT_PROMPTS.md](AGENT_PROMPTS.md)

### For Test Cases (10 minutes)
→ See [EXAMPLES.md](EXAMPLES.md)

---

## Support & Resources

### Documentation
- N8N Docs: https://docs.n8n.io/
- Google Gemini: https://ai.google.dev/docs
- OpenAI: https://platform.openai.com/docs

### Community
- N8N Community: https://community.n8n.io/
- N8N Discord: https://discord.gg/n8n

### Fact-Checking Resources
- Snopes: https://www.snopes.com/
- PolitiFact: https://www.politifact.com/
- FactCheck.org: https://www.factcheck.org/
- MBFC: https://mediabiasfactcheck.com/

---

## Credits & Acknowledgments

**Built with:**
- N8N (Workflow Automation)
- Google Gemini (Primary LLM)
- OpenAI GPT-4 (Backup LLM)
- Professional fact-checking databases

**Inspired by:**
- Academic research on misinformation detection
- Industry best practices in content moderation
- Multi-agent AI systems

---

## License

MIT License - Feel free to modify and adapt for your use case.

---

## Contact & Feedback

For questions, improvements, or feedback, please:
- Open an issue in your repository
- Share improvements with the N8N community
- Contribute to documentation

---

**Built with ❤️ for fighting misinformation**

This system is a tool to assist human moderators, not replace them. Always combine AI insights with human judgment for best results.

