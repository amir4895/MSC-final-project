# Example Payloads and Test Cases

This document contains example inputs and expected outputs for testing the misinformation detection pipeline.

---

## Twitter Webhook Examples

### Example 1: True Claim from Credible Source

**Input:**
```json
{
  "tweets": [
    {
      "tweetText": "NASA announces successful Artemis I mission launch. The uncrewed spacecraft is on its way to the Moon. https://nasa.gov/artemis",
      "tweetSource": "https://nasa.gov/artemis",
      "tweetMetadata": {
        "account_handle": "@NASA",
        "account_created_date": "2008-12-19",
        "follower_count": 50000000,
        "following_count": 300,
        "tweet_count": 85000,
        "bio": "Exploring the universe and our home planet.",
        "profile_image_url": "https://pbs.twimg.com/profile_images/nasa.jpg",
        "location": "Washington, DC",
        "verified": true,
        "header_image_url": "https://pbs.twimg.com/profile_banners/nasa.jpg"
      }
    }
  ]
}
```

**Expected Output:**
```json
{
  "final_assessment": {
    "risk_level": "LOW",
    "composite_score": 95,
    "confidence": "HIGH"
  },
  "contributing_factors": {
    "fact_check_verdict": "TRUE",
    "fact_check_score": 95,
    "source_credibility": "HIGH",
    "source_score": 100,
    "account_authenticity": "MINIMAL",
    "account_score": 95
  },
  "key_concerns": [],
  "mitigating_factors": [
    "Verified official NASA account",
    "Claims verified by multiple credible sources",
    "Source is official government website"
  ],
  "recommended_action": {
    "primary_action": "No intervention needed",
    "rationale": "Verified information from official source",
    "urgency": "none"
  },
  "human_review_needed": false,
  "summary": "Verified information from official NASA account with credible sources."
}
```

---

### Example 2: False Claim from Unreliable Source

**Input:**
```json
{
  "tweets": [
    {
      "tweetText": "BREAKING: 5G towers confirmed to cause COVID-19! Government trying to hide the truth! SHARE NOW before they delete this!",
      "tweetSource": "https://conspiracynews247.com/5g-covid",
      "tweetMetadata": {
        "account_handle": "@truthseeker8472",
        "account_created_date": "2023-11-15",
        "follower_count": 250,
        "following_count": 5000,
        "tweet_count": 8500,
        "bio": "Wake up sheeple! Follow for REAL news",
        "profile_image_url": null,
        "location": null,
        "verified": false,
        "header_image_url": null
      }
    }
  ]
}
```

**Expected Output:**
```json
{
  "final_assessment": {
    "risk_level": "HIGH",
    "composite_score": 15,
    "confidence": "HIGH"
  },
  "contributing_factors": {
    "fact_check_verdict": "FALSE",
    "fact_check_score": 0,
    "source_credibility": "LOW",
    "source_score": 10,
    "account_authenticity": "HIGH",
    "account_score": 25
  },
  "key_concerns": [
    "Claims definitively debunked by multiple fact-checkers",
    "Source flagged as conspiracy/misinformation site",
    "New account with suspicious activity patterns",
    "Uses emotional manipulation and urgency tactics"
  ],
  "mitigating_factors": [],
  "recommended_action": {
    "primary_action": "Flag for immediate removal and add warning label",
    "rationale": "Dangerous health misinformation from unreliable source",
    "urgency": "immediate"
  },
  "human_review_needed": true,
  "human_review_reason": "High-risk health misinformation with potential for harm",
  "summary": "Debunked conspiracy theory from unreliable source. Immediate action recommended."
}
```

---

### Example 3: Unverifiable Claim (Triggers Backup Agents)

**Input:**
```json
{
  "tweets": [
    {
      "tweetText": "Sources close to the White House say major policy announcement coming next week. Details unclear.",
      "tweetSource": "https://twitter.com/politicalinsider/status/123456",
      "tweetMetadata": {
        "account_handle": "@politicalinsider",
        "account_created_date": "2019-03-10",
        "follower_count": 15000,
        "following_count": 2000,
        "tweet_count": 25000,
        "bio": "Political commentary and analysis",
        "profile_image_url": "https://example.com/profile.jpg",
        "location": "Washington, DC",
        "verified": false,
        "header_image_url": "https://example.com/header.jpg"
      }
    }
  ]
}
```

**Expected Output:**
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
    "source_credibility": "MEDIUM",
    "source_score": 60,
    "account_authenticity": "LOW",
    "account_score": 70
  },
  "key_concerns": [
    "Vague attribution ('sources close to')",
    "No specific details to verify",
    "Unverified account"
  ],
  "mitigating_factors": [
    "No false claims detected",
    "Account has established presence",
    "Claim is framed as speculation, not fact"
  ],
  "recommended_action": {
    "primary_action": "Add context label suggesting verification",
    "rationale": "Unverified claim with vague sourcing",
    "urgency": "monitor"
  },
  "human_review_needed": false,
  "summary": "Unverifiable political claim with vague sourcing. Suggest caution and verification."
}
```

**Note:** This example would trigger Agent 1B and 2B due to low confidence/unverifiable verdict.

---

### Example 4: Bot Account with True Information

**Input:**
```json
{
  "tweets": [
    {
      "tweetText": "Weather Alert: National Weather Service issues tornado warning for Dallas County until 8:00 PM CDT. Seek shelter immediately.",
      "tweetSource": "https://weather.gov/alerts/tx",
      "tweetMetadata": {
        "account_handle": "@weatherbot_tx",
        "account_created_date": "2023-10-01",
        "follower_count": 500,
        "following_count": 0,
        "tweet_count": 45000,
        "bio": "Automated weather alerts for Texas",
        "profile_image_url": "https://example.com/bot.jpg",
        "location": "Texas",
        "verified": false,
        "header_image_url": null
      }
    }
  ]
}
```

**Expected Output:**
```json
{
  "final_assessment": {
    "risk_level": "MEDIUM",
    "composite_score": 65,
    "confidence": "HIGH"
  },
  "contributing_factors": {
    "fact_check_verdict": "TRUE",
    "fact_check_score": 90,
    "source_credibility": "HIGH",
    "source_score": 95,
    "account_authenticity": "VERY_HIGH",
    "account_score": 10
  },
  "key_concerns": [
    "Account exhibits bot-like behavior (high tweet frequency)",
    "New account with automated posting patterns"
  ],
  "mitigating_factors": [
    "Information is factually accurate",
    "Source is official government weather service",
    "Bot appears to be legitimate automated alert system"
  ],
  "recommended_action": {
    "primary_action": "Allow but label as automated account",
    "rationale": "Accurate information but inauthentic amplification",
    "urgency": "none"
  },
  "human_review_needed": false,
  "summary": "Automated bot sharing accurate weather alerts from official source. Legitimate use case."
}
```

---

### Example 5: Satire/Opinion Piece

**Input:**
```json
{
  "tweets": [
    {
      "tweetText": "OPINION: Why pineapple absolutely belongs on pizza, and anyone who disagrees is wrong. Fight me. 🍕🍍",
      "tweetSource": "https://twitter.com/foodcritic/status/789012",
      "tweetMetadata": {
        "account_handle": "@foodcritic",
        "account_created_date": "2015-06-20",
        "follower_count": 25000,
        "following_count": 1500,
        "tweet_count": 15000,
        "bio": "Food critic and writer. Opinions are my own and probably controversial.",
        "profile_image_url": "https://example.com/profile.jpg",
        "location": "New York, NY",
        "verified": false,
        "header_image_url": "https://example.com/header.jpg"
      }
    }
  ]
}
```

**Expected Output:**
```json
{
  "final_assessment": {
    "risk_level": "LOW",
    "composite_score": 90,
    "confidence": "HIGH"
  },
  "contributing_factors": {
    "fact_check_verdict": "TRUE",
    "fact_check_score": 95,
    "source_credibility": "MEDIUM",
    "source_score": 80,
    "account_authenticity": "MINIMAL",
    "account_score": 85
  },
  "key_concerns": [],
  "mitigating_factors": [
    "Clearly labeled as opinion",
    "No factual claims to verify",
    "Established account with authentic behavior",
    "Lighthearted/satirical tone"
  ],
  "recommended_action": {
    "primary_action": "No intervention needed",
    "rationale": "Opinion piece with no misinformation risk",
    "urgency": "none"
  },
  "human_review_needed": false,
  "summary": "Opinion piece clearly labeled as such. No misinformation concerns."
}
```

---

## WhatsApp Manual Examples

### Example 1: Health Misinformation

**Input (WhatsApp Message):**
```
Drinking bleach cures coronavirus! My aunt tried it and she's fine. Big pharma doesn't want you to know this!
```

**Expected Output (WhatsApp Reply):**
```
🚨 *Misinformation Check Result*

*Risk Level:* HIGH

*Summary:* This claim has been definitively debunked by health authorities. Drinking bleach is extremely dangerous and can cause serious harm or death. This is not a cure for COVID-19 or any illness.

*Recommendation:* DO NOT follow this advice. It is dangerous and potentially life-threatening. Please consult official health sources like WHO or CDC for accurate COVID-19 information.

*Verification Links:*
- https://www.who.int/emergencies/diseases/novel-coronavirus-2019
- https://www.cdc.gov/coronavirus/2019-ncov/
- https://www.snopes.com/fact-check/bleach-cure-covid/
```

---

### Example 2: True News Story

**Input (WhatsApp Message):**
```
Breaking: SpaceX successfully launches Starship rocket to orbit. Historic achievement for commercial spaceflight.
```

**Expected Output (WhatsApp Reply):**
```
✅ *Misinformation Check Result*

*Risk Level:* LOW

*Summary:* This information appears to be accurate and has been verified by multiple credible sources including SpaceX official channels and reputable news outlets.

*Recommendation:* This appears to be reliable information. Feel free to share.
```

---

### Example 3: Ambiguous Claim (Triggers Backup)

**Input (WhatsApp Message):**
```
They're planning to introduce a new tax next month. Everyone will have to pay more.
```

**Expected Output (WhatsApp Reply):**
```
⚠️ *Misinformation Check Result*

*Risk Level:* MEDIUM

*Summary:* This claim is too vague to verify. Without specific details about who "they" are, what type of tax, and which jurisdiction, it's impossible to confirm or deny.

*Recommendation:* Please verify this information with official government sources or reputable news outlets before sharing. Look for specific details like:
- Which government/authority?
- What type of tax?
- Which country/region?
- Official announcement source?

*Verification Links:*
- Check your local government's official website
- Look for announcements from tax authorities
- Verify with reputable local news sources
```

---

### Example 4: Opinion Statement

**Input (WhatsApp Message):**
```
I think electric cars are the future and everyone should switch to them.
```

**Expected Output (WhatsApp Reply):**
```
✅ *Misinformation Check Result*

*Risk Level:* LOW

*Summary:* This is an opinion statement about electric vehicles. While it contains a viewpoint, it doesn't make specific factual claims that can be verified as true or false.

*Recommendation:* This is a personal opinion. No misinformation concerns detected.
```

---

### Example 5: Outdated Information

**Input (WhatsApp Message):**
```
Breaking news: Donald Trump wins 2020 presidential election!
```

**Expected Output (WhatsApp Reply):**
```
🚨 *Misinformation Check Result*

*Risk Level:* HIGH

*Summary:* This claim is false. Joe Biden won the 2020 U.S. presidential election, as confirmed by official election results, the Electoral College, and certified by Congress. This has been verified by multiple credible sources.

*Recommendation:* This is misinformation. The 2020 election results have been officially certified and confirmed. Please verify information with official sources before sharing.

*Verification Links:*
- https://www.archives.gov/electoral-college/2020
- https://www.politifact.com/
- https://www.factcheck.org/
```

---

## Testing Checklist

Use these test cases to verify your pipeline is working correctly:

### Twitter Webhook Tests

- [ ] Test 1: True claim from verified account → LOW risk
- [ ] Test 2: False claim from new account → HIGH risk
- [ ] Test 3: Unverifiable claim → MEDIUM risk, triggers backup agents
- [ ] Test 4: Bot account with true info → MEDIUM risk
- [ ] Test 5: Opinion/satire → LOW risk
- [ ] Test 6: Missing metadata → Handles gracefully
- [ ] Test 7: Multiple tweets in one request → Processes all
- [ ] Test 8: Malformed JSON → Returns error

### WhatsApp Manual Tests

- [ ] Test 1: Dangerous health misinfo → HIGH risk, strong warning
- [ ] Test 2: True news story → LOW risk, confirmation
- [ ] Test 3: Vague claim → MEDIUM risk, triggers backup, asks for details
- [ ] Test 4: Opinion statement → LOW risk, acknowledges opinion
- [ ] Test 5: Outdated info → HIGH risk, corrects with current info
- [ ] Test 6: Empty message → Handles gracefully
- [ ] Test 7: Very long message → Processes correctly
- [ ] Test 8: Non-English text → Handles appropriately

---

## Curl Commands for Testing

### Test Twitter Webhook (True Claim)

```bash
curl -X POST http://localhost:5678/webhook/misinformation-check \
  -H "Content-Type: application/json" \
  -d '{
    "tweets": [{
      "tweetText": "NASA announces successful Artemis I mission launch.",
      "tweetSource": "https://nasa.gov/artemis",
      "tweetMetadata": {
        "account_handle": "@NASA",
        "account_created_date": "2008-12-19",
        "follower_count": 50000000,
        "following_count": 300,
        "tweet_count": 85000,
        "bio": "Exploring the universe",
        "verified": true
      }
    }]
  }'
```

### Test Twitter Webhook (False Claim)

```bash
curl -X POST http://localhost:5678/webhook/misinformation-check \
  -H "Content-Type: application/json" \
  -d '{
    "tweets": [{
      "tweetText": "5G towers cause COVID-19! Share before deleted!",
      "tweetSource": "https://conspiracynews247.com/5g",
      "tweetMetadata": {
        "account_handle": "@truthseeker123",
        "account_created_date": "2023-11-15",
        "follower_count": 250,
        "following_count": 5000,
        "tweet_count": 8500,
        "bio": "Wake up!",
        "verified": false
      }
    }]
  }'
```

---

## Performance Benchmarks

Expected response times:

- **Without Backup Agents:** 5-10 seconds
- **With Backup Agents:** 15-25 seconds
- **Multiple Tweets (5):** 10-15 seconds (parallel processing)

Expected costs per analysis:

- **Twitter (no backup):** ~$0.015
- **Twitter (with backup):** ~$0.085
- **WhatsApp (no backup):** ~$0.012
- **WhatsApp (with backup):** ~$0.070

---

## Monitoring Metrics

Track these metrics for your deployment:

1. **Accuracy Metrics:**
   - False positive rate (flagged as misinfo but actually true)
   - False negative rate (missed actual misinfo)
   - Backup agent trigger rate (should be 20-30%)

2. **Performance Metrics:**
   - Average response time
   - 95th percentile response time
   - API failure rate

3. **Cost Metrics:**
   - Cost per analysis
   - Monthly API costs
   - Cost per risk level (HIGH/MEDIUM/LOW)

4. **Usage Metrics:**
   - Total analyses per day
   - Risk level distribution
   - Human review rate

---

## Troubleshooting Common Issues

### Issue: All results return MEDIUM risk

**Cause:** Agents are being too cautious

**Fix:** Adjust confidence thresholds in prompts

### Issue: Backup agents trigger too often

**Cause:** Primary agents returning low confidence frequently

**Fix:** 
1. Improve primary agent prompts
2. Increase backup trigger threshold
3. Use more capable primary LLM

### Issue: High false positive rate

**Cause:** Risk thresholds too aggressive

**Fix:** Adjust risk score thresholds in Agent 4 (e.g., HIGH: 0-35 instead of 0-40)

### Issue: Response times too slow

**Cause:** Sequential processing or slow LLM

**Fix:**
1. Ensure agents run in parallel
2. Use faster LLM models
3. Implement caching for common queries

---

Happy testing! 🚀

