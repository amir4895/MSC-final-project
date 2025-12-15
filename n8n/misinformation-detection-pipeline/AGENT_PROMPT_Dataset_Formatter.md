# Agent Prompt: Dataset Formatter

**Purpose:** Extract data from Supabase and format for misinformation detection pipeline

---

## Refined Prompt (Copy this to Agent node)

```
Use the supabase tool to get the row from the dataset table.

INPUT PARAMETERS:
- Table: {{ $json.dataset }}
- Row ID: {{ $json.idx }}

INSTRUCTIONS:
1. Use the Supabase tool to fetch the row where id = {{ $json.idx }}
2. Extract ALL fields from the returned row
3. Format the output EXACTLY as specified below

OUTPUT FORMAT (return ONLY this JSON structure):

{
  "tweetText": "<copy the 'text' field from Supabase row>",
  "tweetSource": "{{ $json.dataset }}",
  "sourceType": "dataset",
  "tweetMetadata": {
    "title": "<copy the 'title' field from Supabase row, or empty string if missing>",
    "subject": "<copy the 'subject' field from Supabase row, or empty string if missing>",
    "date": "<copy the 'date' field from Supabase row, or empty string if missing>",
    "created_at": "<copy the 'date' field from Supabase row, or current date if missing>"
  },
  "accountData": {
    "username": "dataset",
    "verified": false,
    "followers": 0,
    "following": 0,
    "follower_ratio": "0",
    "total_tweets": 0,
    "account_age_days": 0,
    "tweets_per_day": "0",
    "profile_completeness_score": "0/7",
    "has_profile_image": false,
    "has_bio": false,
    "has_location": false,
    "has_banner": false,
    "has_website": false,
    "created_at": "",
    "description": "",
    "location": "",
    "website": ""
  },
  "supabase_id": {{ $json.idx }},
  "dataset": "{{ $json.dataset }}",
  "datasetType": "{{ $json.dataset == 'true-news' ? 'TRUE' : 'FALSE' }}",
  "title": "<copy the 'title' field from Supabase row>",
  "subject": "<copy the 'subject' field from Supabase row>",
  "date": "<copy the 'date' field from Supabase row>",
  "search_results": [],
  "search_status": "PENDING",
  "credible_sources_found": 0,
  "total_results": 0
}

CRITICAL RULES:
1. Replace ALL <copy...> placeholders with actual values from Supabase
2. If a field is missing from Supabase, use empty string "" (not null, not "missing")
3. The "text" field from Supabase goes into "tweetText"
4. Keep accountData exactly as shown (all zeros/false/empty)
5. Return ONLY the JSON object (no markdown, no explanation, no code blocks)
6. Ensure all strings are properly escaped
7. Do NOT fabricate data - only use what Supabase returns

EXAMPLE:
If Supabase returns:
{
  "id": 30,
  "text": "Treasury Secretary Mnuchin was sent gift-wrapped box...",
  "title": "(Reuters) - A gift-wrapped package addressed...",
  "subject": "politicsNews",
  "date": "December 24, 2017"
}

You should return:
{
  "tweetText": "Treasury Secretary Mnuchin was sent gift-wrapped box...",
  "tweetSource": "true-news",
  "sourceType": "dataset",
  "tweetMetadata": {
    "title": "(Reuters) - A gift-wrapped package addressed...",
    "subject": "politicsNews",
    "date": "December 24, 2017",
    "created_at": "December 24, 2017"
  },
  "accountData": {
    "username": "dataset",
    "verified": false,
    "followers": 0,
    "following": 0,
    "follower_ratio": "0",
    "total_tweets": 0,
    "account_age_days": 0,
    "tweets_per_day": "0",
    "profile_completeness_score": "0/7",
    "has_profile_image": false,
    "has_bio": false,
    "has_location": false,
    "has_banner": false,
    "has_website": false,
    "created_at": "",
    "description": "",
    "location": "",
    "website": ""
  },
  "supabase_id": 30,
  "dataset": "true-news",
  "datasetType": "TRUE",
  "title": "(Reuters) - A gift-wrapped package addressed...",
  "subject": "politicsNews",
  "date": "December 24, 2017",
  "search_results": [],
  "search_status": "PENDING",
  "credible_sources_found": 0,
  "total_results": 0
}

Return ONLY the JSON object.
```

---

## System Message (for Agent node)

```
You are a data formatter. Your job is to:
1. Fetch data from Supabase using the provided tool
2. Extract ALL fields from the returned row
3. Format the data EXACTLY as specified in the prompt
4. Return ONLY valid JSON (no markdown, no code blocks, no explanation)

If a field is missing from Supabase, use empty string "".
Do NOT fabricate or guess data.
Copy values exactly as they appear in Supabase.
```

---

## Alternative: Simplified Prompt (More Explicit)

```
TASK: Fetch row {{ $json.idx }} from table {{ $json.dataset }} and format it.

STEP 1: Use Supabase tool
- Table: {{ $json.dataset }}
- Filter: id = {{ $json.idx }}

STEP 2: Extract these fields from Supabase response:
- text (required) → use for "tweetText"
- title (optional) → use for "title" and "tweetMetadata.title"
- subject (optional) → use for "subject" and "tweetMetadata.subject"  
- date (optional) → use for "date" and "tweetMetadata.date"

STEP 3: Build JSON with this structure:

Main content:
- tweetText = <text field from Supabase>
- tweetSource = {{ $json.dataset }}
- sourceType = "dataset"

Metadata:
- tweetMetadata.title = <title field or "">
- tweetMetadata.subject = <subject field or "">
- tweetMetadata.date = <date field or "">
- tweetMetadata.created_at = <date field or "">

Account (all static):
- accountData.username = "dataset"
- accountData.verified = false
- accountData.followers = 0
- accountData.following = 0
- accountData.follower_ratio = "0"
- accountData.total_tweets = 0
- accountData.account_age_days = 0
- accountData.tweets_per_day = "0"
- accountData.profile_completeness_score = "0/7"
- accountData.has_profile_image = false
- accountData.has_bio = false
- accountData.has_location = false
- accountData.has_banner = false
- accountData.has_website = false
- accountData.created_at = ""
- accountData.description = ""
- accountData.location = ""
- accountData.website = ""

Dataset info:
- supabase_id = {{ $json.idx }}
- dataset = {{ $json.dataset }}
- datasetType = "TRUE" if {{ $json.dataset }} is "true-news", else "FALSE"
- title = <title field or "">
- subject = <subject field or "">
- date = <date field or "">

Search (all empty - will be filled later):
- search_results = []
- search_status = "PENDING"
- credible_sources_found = 0
- total_results = 0

STEP 4: Return ONLY the complete JSON object (no markdown, no explanation)
```

---

## Usage Instructions

1. **Copy the "Refined Prompt"** section above
2. **Paste into Agent node** "text" parameter
3. **Set System Message** to the provided system message
4. **Set maxIterations** to 3
5. **Connect Supabase tool** to the agent
6. **Test** with sample input: `{"dataset": "true-news", "idx": 30}`

---

## Expected Input Format

```json
{
  "dataset": "true-news",
  "idx": 30
}
```

or

```json
{
  "dataset": "false-news",
  "idx": 600
}
```

---

## Expected Output Format

```json
{
  "tweetText": "full article text...",
  "tweetSource": "true-news",
  "sourceType": "dataset",
  "tweetMetadata": {
    "title": "article title",
    "subject": "politicsNews",
    "date": "December 24, 2017",
    "created_at": "December 24, 2017"
  },
  "accountData": { /* all fields as specified */ },
  "supabase_id": 30,
  "dataset": "true-news",
  "datasetType": "TRUE",
  "title": "article title",
  "subject": "politicsNews",
  "date": "December 24, 2017",
  "search_results": [],
  "search_status": "PENDING",
  "credible_sources_found": 0,
  "total_results": 0
}
```

---

## Troubleshooting

### Issue: Agent returns incomplete JSON
**Solution:** Increase `maxOutputTokens` to 2000+ in the LLM node

### Issue: Agent fabricates data
**Solution:** Add to system message: "Do NOT fabricate data. Only use what Supabase returns."

### Issue: Missing fields
**Solution:** Check Supabase table has all expected columns (text, title, subject, date)

### Issue: Wrong datasetType
**Solution:** Ensure logic: `true-news` → `"TRUE"`, `false-news` → `"FALSE"`

---

**Version:** 1.0  
**Created:** December 14, 2025  
**Purpose:** Agent prompt for dataset formatting

