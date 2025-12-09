# Workflow Flowchart - v3.3
## Simplified Single-Item Processing with Google Sheets

**Last Updated:** December 9, 2025  
**Version:** 3.3  
**Architecture:** Simple Linear Flow (No Loops)

---

## 📊 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         INPUT SOURCES                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼────────┐  ┌──────▼──────────┐
            │ Manual Trigger │  │ Every 4 Hours   │
            │  (On-demand)   │  │  (Scheduled)    │
            └───────┬────────┘  └──────┬──────────┘
                    │                   │
                    └─────────┬─────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                     TWITTER DATA FETCHING                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────▼──────────┐
                    │ Search Viral News  │
                    │     Tweets         │
                    │  (RapidAPI)        │
                    │  count=1 ⭐        │
                    └─────────┬──────────┘
                              │
                    ┌─────────▼──────────┐
                    │ Get Top 1 Most     │
                    │    Viral Tweet     │
                    │ (Rank by virality) │
                    │  ITEM_LIMIT = 1    │
                    └─────────┬──────────┘
                              │
┌─────────────────────────────────────────────────────────────────┐
│                    WHATSAPP DATA FLOW                            │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
    ┌───────▼────────┐       │       ┌─────────▼────────┐
    │ WhatsApp       │       │       │ AI Agent -       │
    │   Trigger      │       │       │ Supabase         │
    │                │       │       │ Formatter        │
    └───────┬────────┘       │       └─────────┬────────┘
            │                │                 │
            │                │                 │
            └────────────────┼─────────────────┘
                             │
                    ┌────────▼─────────┐
                    │ Merge Dataset &  │
                    │ Twitter Inputs   │
                    └────────┬─────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                    DATA FORMATTING                               │
└─────────────────────────────────────────────────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │ Format Input     │
                    │     Data         │
                    │ (Preserve all    │
                    │   metadata)      │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Parse Input Data │
                    │  (Pass-through)  │
                    └────────┬─────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                    AI AGENT ANALYSIS                             │
│                  (1 TWEET PROCESSED)                             │
└─────────────────────────────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐         ┌────▼────┐        ┌────▼────┐
    │ Agent 1 │         │ Agent 2 │        │ Agent 3 │
    │  Fact   │         │ Source  │        │ Twitter │
    │  Check  │         │Credibil │        │ Account │
    │ (Groq)  │         │  ity    │        │ Check   │
    └────┬────┘         │ (Groq)  │        │ (Groq)  │
         │              └────┬────┘        └────┬────┘
         │                   │                   │
    ┌────▼──────┐            │                   │
    │ Check     │            │                   │
    │Confidence │            │                   │
    └────┬──────┘            │                   │
         │                   │                   │
    ┌────▼──────┐       ┌────▼──────┐           │
    │If Low:    │       │If Low:    │           │
    │Agent 1B   │       │Agent 2B   │           │
    │(Gemini)   │       │(Gemini)   │           │
    └────┬──────┘       └────┬──────┘           │
         │                   │                   │
    ┌────▼──────┐       ┌────▼──────┐           │
    │Merge      │       │Merge      │           │
    │Results    │       │Results    │           │
    └────┬──────┘       └────┬──────┘           │
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                    ┌────────▼─────────┐
                    │ Merge Agents     │
                    │    1 & 2         │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Merge with       │
                    │   Agent 3        │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Combine for      │
                    │   Agent 4        │
                    │ (Parse outputs)  │
                    └────────┬─────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                    FINAL DECISION                                │
└─────────────────────────────────────────────────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │   Agent 4 -      │
                    │    Decision      │
                    │   (Gemini)       │
                    │                  │
                    │ Composite Score: │
                    │ Fact 50% +       │
                    │ Source 30% +     │
                    │ Account 20%      │
                    └────────┬─────────┘
                             │
┌─────────────────────────────────────────────────────────────────┐
│                    GOOGLE SHEETS LOGGING                         │
└─────────────────────────────────────────────────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │ Format for       │
                    │ Google Sheets    │
                    │                  │
                    │ Extract 25+      │
                    │ columns          │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │ Append row in    │
                    │     sheet        │
                    │                  │
                    │ Write 1 row ✅   │
                    └────────┬─────────┘
                             │
                        ┌────▼────┐
                        │  DONE   │
                        │    ✅   │
                        └─────────┘
```

---

## 🔑 Key Features

### ✅ Simple Linear Flow
- **No loops** - straightforward execution
- **No batching** - one item per execution
- **Predictable** - same path every time

### ✅ Single Item Processing
- **1 tweet per execution** (Manual or Scheduled)
- **API requests only 1 tweet** (count=1)
- **Clean data flow** - no multiplication issues

### ✅ Parallel Agent Analysis
- Agents 1, 2, 3 run simultaneously
- Backup agents (1B, 2B) triggered on low confidence
- Results merged before final decision

### ✅ Google Sheets Integration
- Automatic logging after each analysis
- 25+ detailed metric columns
- One row per tweet/article

---

## 📋 Data Flow Details

### Input Data Structure

**Twitter Input:**
```json
{
  "tweetText": "BREAKING: Two NJ brothers have been arrested...",
  "tweetSource": "twitter_viral",
  "sourceType": "twitter",
  "virality_score": 3771,
  "engagement": "1558 RT | 0 ♥ | 195 💬",
  "author": "@bennyjohnson",
  "tweet_id": "1234567890",
  "tweet_url": "https://twitter.com/i/web/status/1234567890",
  "accountData": {
    "username": "bennyjohnson",
    "verified": false,
    "followers": 1250000
  }
}
```

**Dataset Input (WhatsApp):**
```json
{
  "tweetText": "Article text from Supabase...",
  "tweetSource": "false-news",
  "sourceType": "dataset",
  "dataset": "false-news",
  "supabase_id": 600,
  "datasetType": "F",
  "title": "Article title",
  "subject": "Politics",
  "date": "2024-01-15"
}
```

**Direct Access:**
- **Twitter**: Click `tweet_url` to view original tweet
- **Dataset**: Use `dataset` + `supabase_id` to identify article (e.g., F600, T123)

### Agent Outputs
- **Agent 1**: Fact accuracy, deceptiveness, classification
- **Agent 2**: Source credibility, trustworthiness score
- **Agent 3**: Bot probability, authenticity score
- **Agent 4**: Final risk level, composite score, recommendations

### Google Sheets Output
```
| Timestamp | Source | Risk Level | Composite Score | Confidence |
| Fact Check Classification | Fact Check Score |
| Source Credibility Rating | Source Credibility Score |
| Account Authenticity | Account Score |
| Key Concerns | Recommended Action | Urgency | Rationale |
| Summary | Tweet URL | Author | Dataset | Supabase ID | Raw Assessment |
```

### Direct Links in Output
- **Twitter**: `tweet_url` = `https://twitter.com/i/web/status/{tweet_id}`
- **Dataset**: Shows `dataset` (true-news/false-news) + `supabase_id` (index number)
  - Example: "false-news" + ID "600" = Article F600 from Supabase
  - Example: "true-news" + ID "123" = Article T123 from Supabase

---

## 🎯 Execution Modes

### Manual Trigger
1. Click "Execute Workflow"
2. Fetches 1 most viral tweet
3. Processes through all agents
4. Logs to Google Sheets
5. Done

### Scheduled (Every 4 Hours)
1. Triggers automatically
2. Fetches 1 most viral tweet
3. Processes through all agents
4. Logs to Google Sheets
5. Done
6. Waits 4 hours, repeats

### WhatsApp Input
1. Send message (e.g., "F600" or "T123")
2. Fetches from Supabase dataset
3. Processes through all agents
4. Logs to Google Sheets
5. Done

---

## 🔄 Pending Improvements

1. **Agent 3 Optimization** - Improve Twitter account behavior analysis
2. **Fix Proposal** - Implementation pending
3. **Batch Processing Option** - Allow processing multiple tweets per execution
4. **Commenting/Response** - Add automated response functionality
5. **Pure Manual Testing** - Add manual input mode for ad-hoc testing

---

## 📊 Performance Metrics

- **Execution Time**: ~30-60 seconds per tweet
- **API Calls**: 
  - 1 Twitter API call (RapidAPI)
  - 3-5 LLM calls (Groq + Gemini)
  - 1 Google Sheets write
- **Cost per Execution**: ~$0.003-0.018
- **Throughput**: 
  - Manual: On-demand
  - Scheduled: 6 tweets per day (every 4 hours)

---

**End of Flowchart Document**

