# Setup Guide - N8N Misinformation Detection Pipeline

## Quick Start

This guide will walk you through setting up the misinformation detection pipeline in N8N.

---

## Step 1: Prerequisites

### 1.1 N8N Installation

If you don't have N8N installed:

```bash
# Using npm (recommended)
npm install n8n -g

# Or using Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### 1.2 Start N8N

```bash
n8n start
```

Access N8N at: http://localhost:5678

---

## Step 2: API Keys Setup

You'll need the following API keys:

### 2.1 Google Gemini API (Primary LLM)

**Required for:** Agent 1, 2, 3, 4

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Get API Key"
3. Create or select a project
4. Copy your API key

**Cost:** Free tier available (60 requests/minute)

### 2.2 OpenAI API (Backup LLM)

**Required for:** Agent 1B, 2B

1. Go to: https://platform.openai.com/
2. Create account or sign in
3. Navigate to API Keys
4. Create new secret key
5. Copy your API key

**Cost:** Pay-as-you-go (~$0.03 per backup agent call with GPT-4)

**Alternative:** You can use Claude instead:
- Go to: https://console.anthropic.com/
- Get API key
- Modify workflow to use Claude nodes instead of OpenAI

### 2.3 Twitter API v2 (For Webhook Flow)

**Required for:** Twitter/Webhook workflow only

1. Go to: https://developer.twitter.com/
2. Apply for developer account
3. Create a new app
4. Request "Elevated" access (required for account metadata)
5. Copy your Bearer Token

**Cost:** Free tier available (500k tweets/month)

**Required Access Level:** Elevated (for account metadata like follower count, creation date)

### 2.4 WhatsApp Business API (For Manual Flow)

**Required for:** WhatsApp/Manual workflow only

**Option A - Official API:**
1. Go to: https://business.whatsapp.com/
2. Sign up for WhatsApp Business API
3. Get your access token

**Option B - Third-party (easier):**
- Twilio WhatsApp: https://www.twilio.com/whatsapp
- MessageBird: https://www.messagebird.com/
- N8N Cloud has built-in WhatsApp integration

**Cost:** Varies by provider (Twilio: $0.005 per message)

---

## Step 3: Configure N8N Credentials

### 3.1 Add Google Gemini Credentials

1. In N8N, go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Search for "Google Gemini"
4. Enter your API key
5. Name it: "Google Gemini API"
6. Click **Save**

### 3.2 Add OpenAI Credentials

1. Go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Search for "OpenAI"
4. Enter your API key
5. Name it: "OpenAI API"
6. Click **Save**

### 3.3 Add Twitter Credentials (Optional)

1. Go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Search for "Twitter"
4. Enter your Bearer Token
5. Name it: "Twitter API"
6. Click **Save**

### 3.4 Add WhatsApp Credentials (Optional)

1. Go to **Settings** → **Credentials**
2. Click **Add Credential**
3. Search for "WhatsApp"
4. Follow provider-specific setup
5. Name it: "WhatsApp Business API"
6. Click **Save**

---

## Step 4: Import Workflows

### 4.1 Import Twitter Webhook Workflow

1. In N8N, click **Workflows** → **Import from File**
2. Select: `workflow-twitter-webhook.json`
3. Click **Import**
4. The workflow will appear in your workflows list

### 4.2 Import WhatsApp Manual Workflow

1. Click **Workflows** → **Import from File**
2. Select: `workflow-whatsapp-manual.json`
3. Click **Import**

---

## Step 5: Configure Workflows

### 5.1 Configure Twitter Webhook Workflow

1. Open the "Misinformation Detection - Twitter Webhook" workflow
2. Click on each agent node (Agent 1, 2, 3, 4, 1B, 2B)
3. Verify credentials are correctly assigned:
   - Agent 1, 2, 3, 4 → "Google Gemini API"
   - Agent 1B, 2B → "OpenAI API"
4. Click **Save**

### 5.2 Configure WhatsApp Manual Workflow

1. Open the "Misinformation Detection - WhatsApp Manual" workflow
2. Click on each agent node
3. Verify credentials:
   - Agent 1, 2, 4 → "Google Gemini API"
   - Agent 1B, 2B → "OpenAI API"
4. Click on "WhatsApp Trigger" node
5. Assign "WhatsApp Business API" credentials
6. Click **Save**

---

## Step 6: Activate Workflows

### 6.1 Activate Twitter Webhook

1. Open the Twitter webhook workflow
2. Toggle the **Active** switch at the top right
3. Click on the "Webhook Trigger" node
4. Copy the **Webhook URL** (you'll need this)
5. The URL will look like: `https://your-n8n-instance.com/webhook/misinformation-check`

### 6.2 Activate WhatsApp Manual

1. Open the WhatsApp manual workflow
2. Toggle the **Active** switch at the top right
3. The workflow will now listen for WhatsApp messages

---

## Step 7: Test the Workflows

### 7.1 Test Twitter Webhook

Use curl or Postman to send a test request:

```bash
curl -X POST https://your-n8n-instance.com/webhook/misinformation-check \
  -H "Content-Type: application/json" \
  -d '{
    "tweets": [
      {
        "tweetText": "Breaking: Scientists discover cure for common cold",
        "tweetSource": "https://example.com/article",
        "tweetMetadata": {
          "account_handle": "@testuser",
          "account_created_date": "2020-01-15",
          "follower_count": 5000,
          "following_count": 500,
          "tweet_count": 12000,
          "bio": "Science journalist",
          "profile_image_url": "https://example.com/image.jpg",
          "verified": false
        }
      }
    ]
  }'
```

**Expected Response:**
```json
{
  "final_assessment": {
    "risk_level": "MEDIUM",
    "composite_score": 55,
    "confidence": "MEDIUM"
  },
  "contributing_factors": {
    "fact_check_verdict": "UNVERIFIABLE",
    "fact_check_score": 50,
    "source_credibility": "UNKNOWN",
    "source_score": 45,
    "account_authenticity": "LOW_RISK",
    "account_score": 75
  },
  "recommended_action": {
    "primary_action": "Add context label",
    "rationale": "Claim cannot be verified",
    "urgency": "monitor"
  },
  "summary": "Extraordinary health claim from unknown source requires verification."
}
```

### 7.2 Test WhatsApp Manual

1. Send a WhatsApp message to your configured number:
   ```
   Breaking: Scientists discover cure for common cold
   ```

2. You should receive a reply like:
   ```
   ⚠️ *Misinformation Check Result*

   *Risk Level:* MEDIUM

   *Summary:* Extraordinary health claim requires verification from credible sources.

   *Recommendation:* Please verify with reputable health organizations before sharing.
   ```

---

## Step 8: Monitoring and Debugging

### 8.1 View Execution History

1. In N8N, go to **Executions**
2. Click on any execution to see detailed logs
3. Check each node's input/output

### 8.2 Common Issues

**Issue: "Agent returned empty response"**
- **Cause:** LLM didn't return valid JSON
- **Fix:** Check agent prompts, ensure "Respond ONLY with valid JSON" is present

**Issue: "Backup agents not triggering"**
- **Cause:** Confidence check not working
- **Fix:** Verify the "Check if Backup Needed" node conditions

**Issue: "Twitter API rate limit exceeded"**
- **Cause:** Too many requests
- **Fix:** Implement rate limiting or upgrade Twitter API tier

**Issue: "Webhook not receiving data"**
- **Cause:** Webhook URL not accessible
- **Fix:** Ensure N8N is publicly accessible (use ngrok for local testing)

### 8.3 Enable Debug Mode

1. Open workflow
2. Click **Settings** (gear icon)
3. Enable "Save Execution Progress"
4. Enable "Save Manual Executions"
5. This will log all intermediate steps

---

## Step 9: Production Deployment

### 9.1 Security Considerations

1. **Webhook Authentication:**
   - Add authentication to webhook endpoint
   - Use API keys or JWT tokens

2. **Rate Limiting:**
   - Implement rate limiting to prevent abuse
   - Use N8N's built-in rate limiting or external service

3. **Data Privacy:**
   - Ensure compliance with GDPR/privacy laws
   - Don't log sensitive user data

### 9.2 Scaling

**For High Volume:**

1. **Use N8N Cloud** (managed service)
   - Auto-scaling
   - Built-in monitoring
   - High availability

2. **Self-Hosted with Queue:**
   - Use Redis queue for async processing
   - Deploy multiple N8N instances
   - Load balancer in front

3. **Optimize LLM Calls:**
   - Cache common results
   - Batch similar requests
   - Use cheaper models for simple cases

### 9.3 Cost Optimization

**Estimated Costs (per 1000 tweets):**

- Google Gemini (4 calls): ~$0.40
- OpenAI GPT-4 (2 backup calls, 30% trigger rate): ~$18
- Twitter API: Free (under 500k/month)
- Total: ~$18-20 per 1000 tweets

**Optimization Tips:**

1. Use GPT-3.5-turbo instead of GPT-4 for backups (10x cheaper)
2. Increase confidence thresholds to reduce backup triggers
3. Cache results for identical tweets
4. Use Gemini for all agents (cheaper than GPT-4)

---

## Step 10: Customization

### 10.1 Adjust Risk Weights

Edit Agent 4 prompt to change scoring:

```javascript
// Current weights
Risk Score = (Fact × 0.50) + (Source × 0.30) + (Account × 0.20)

// Example: Prioritize source credibility more
Risk Score = (Fact × 0.40) + (Source × 0.40) + (Account × 0.20)
```

### 10.2 Add New Fact-Check Sources

Edit Agent 1 prompt to include additional sources:

```
4. Your Custom Source:
   - https://yourcustomfactchecker.com/
```

### 10.3 Change Backup LLM

Replace OpenAI nodes with Claude:

1. Delete Agent 1B and 2B nodes
2. Add "Claude" nodes
3. Configure with Anthropic API credentials
4. Copy prompts from deleted nodes

### 10.4 Add Email Notifications

For high-risk detections:

1. Add "IF" node after Agent 4
2. Condition: `risk_level === "HIGH"`
3. Add "Send Email" node
4. Configure with SMTP credentials

---

## Step 11: Integration Examples

### 11.1 Integrate with Twitter Bot

```python
import tweepy
import requests

# Twitter API setup
api = tweepy.API(auth)

# Monitor mentions
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # Send to N8N webhook
        payload = {
            "tweets": [{
                "tweetText": status.text,
                "tweetSource": f"https://twitter.com/{status.user.screen_name}/status/{status.id}",
                "tweetMetadata": {
                    "account_handle": f"@{status.user.screen_name}",
                    "account_created_date": status.user.created_at.isoformat(),
                    "follower_count": status.user.followers_count,
                    "following_count": status.user.friends_count,
                    "tweet_count": status.user.statuses_count,
                    "bio": status.user.description,
                    "verified": status.user.verified
                }
            }]
        }
        
        response = requests.post(
            "https://your-n8n-instance.com/webhook/misinformation-check",
            json=payload
        )
        
        result = response.json()
        
        # Take action based on risk level
        if result["final_assessment"]["risk_level"] == "HIGH":
            # Reply with warning
            api.update_status(
                f"⚠️ This tweet may contain misinformation. {result['summary']}",
                in_reply_to_status_id=status.id
            )
```

### 11.2 Integrate with Slack

Add Slack notification node after Agent 4:

1. Add "Slack" node
2. Configure webhook URL
3. Message template:
   ```
   🚨 High Risk Tweet Detected!
   
   Risk Level: {{ $json.final_assessment.risk_level }}
   Summary: {{ $json.summary }}
   
   Action Required: {{ $json.recommended_action.primary_action }}
   ```

---

## Support & Resources

### Documentation
- N8N Docs: https://docs.n8n.io/
- Google Gemini Docs: https://ai.google.dev/docs
- OpenAI Docs: https://platform.openai.com/docs

### Community
- N8N Community: https://community.n8n.io/
- N8N Discord: https://discord.gg/n8n

### Troubleshooting
- Check execution logs in N8N
- Review agent prompts for JSON formatting
- Verify API credentials are active
- Test with simple examples first

---

## Next Steps

1. ✅ Complete setup following this guide
2. ✅ Test with sample data
3. ✅ Monitor first 100 executions
4. ✅ Adjust thresholds based on results
5. ✅ Implement production security
6. ✅ Set up monitoring and alerts
7. ✅ Train team on interpreting results

---

## Maintenance Checklist

**Weekly:**
- [ ] Review execution logs
- [ ] Check API usage and costs
- [ ] Review false positive/negative cases

**Monthly:**
- [ ] Update fact-checking source list
- [ ] Tune risk thresholds based on feedback
- [ ] Review and update agent prompts
- [ ] Check for N8N updates

**Quarterly:**
- [ ] Audit overall system performance
- [ ] Review and optimize costs
- [ ] Update documentation
- [ ] Train new team members

---

Good luck with your misinformation detection pipeline! 🚀

