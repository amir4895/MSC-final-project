# Dataset Processor Workflow

**File:** `workflow-dataset-processor.json`  
**Purpose:** Process WhatsApp manual input (dataset queries) and format for main pipeline  
**Status:** Standalone workflow

---

## 🎯 What This Does

This workflow handles manual input from WhatsApp for dataset queries (e.g., "T30", "F600") and formats the data to match the structure expected by the main misinformation detection pipeline.

---

## 📊 Input Structure (WhatsApp)

```json
{
  "body": {
    "dataset": "true-news",  // or "false-news"
    "idx": 30                // row ID
  }
}
```

**Example WhatsApp Messages:**
- `T30` → `{"dataset": "true-news", "idx": 30}`
- `F600` → `{"dataset": "false-news", "idx": 600}`

---

## 🔄 Workflow Flow

```
WhatsApp Webhook
  ↓
Get Dataset Row (Supabase)
  ↓
Format Dataset Data (Code)
  ↓
Respond to Webhook
```

### **Node Details:**

#### **1. WhatsApp Webhook**
- Receives manual input
- Path: `/webhook-dataset`
- Expects: `{"body": {"dataset": "...", "idx": ...}}`

#### **2. Get Dataset Row (Supabase)**
- Fetches row from Supabase
- Table: `true-news` or `false-news`
- Filter: `id = idx`
- Returns: `{id, text, title, subject, date, ...}`

#### **3. Format Dataset Data (Code)**
Transforms Supabase data to match Twitter structure:

```javascript
{
  // Main content
  tweetText: "article text from Supabase",
  
  // Source info
  tweetSource: "true-news",
  sourceType: "dataset",
  
  // Metadata
  tweetMetadata: {
    title: "article title",
    subject: "politicsNews",
    date: "December 24, 2017",
    created_at: "2017-12-24T00:00:00.000Z"
  },
  
  // Account data (empty for dataset)
  accountData: {
    username: "dataset",
    verified: false,
    followers: 0,
    // ... all fields set to 0/false/empty
  },
  
  // Dataset specific
  supabase_id: 30,
  dataset: "true-news",
  datasetType: "TRUE",
  title: "article title",
  subject: "politicsNews",
  date: "December 24, 2017",
  
  // For Google Sheets
  dataset_link: "https://supabase.com/.../true-news?filter=id%3Deq%3D30",
  
  // Search results (populated later)
  search_results: [],
  search_status: "PENDING",
  credible_sources_found: 0,
  total_results: 0
}
```

#### **4. Respond to Webhook**
- Sends success response
- Returns: `{"status": "success", "dataset": "...", "idx": ..., "datasetType": "..."}`

---

## 🔗 Integration with Main Pipeline

### **Option A: Direct Connection**
Connect "Format Dataset Data" output to main pipeline's "Format Input Data" node.

### **Option B: Webhook Chain**
1. This workflow responds to WhatsApp
2. Triggers main pipeline via webhook
3. Passes formatted data

### **Option C: Merge Node**
Keep "Merge Dataset & Twitter Inputs" but:
- Input 0: Twitter data (from "Get Top N Most Viral")
- Input 1: Dataset data (from this workflow's "Format Dataset Data")

---

## 📝 Supabase Data Structure

### **Expected Fields:**
```
id: int2 (primary key)
text: text (article content)
title: text (article title)
subject: text (category, e.g., "politicsNews")
date: text (publication date)
```

### **Example Row:**
```json
{
  "id": 30,
  "text": "Treasury Secretary Mnuchin was sent gift-wrapped box...",
  "title": "(Reuters) - A gift-wrapped package addressed...",
  "subject": "politicsNews",
  "date": "December 24, 2017"
}
```

---

## ⚙️ Setup Instructions

### **1. Import Workflow**
```bash
# In n8n UI:
# Workflows → Import from File → Select workflow-dataset-processor.json
```

### **2. Configure Supabase Credentials**
- Node: "Get Dataset Row"
- Credentials: Select your Supabase account
- Should match: `Cgrz5nOdspcCgDyr` (or update)

### **3. Update Supabase Project Link**
In "Format Dataset Data" node, update line:
```javascript
dataset_link: `https://supabase.com/dashboard/project/YOUR_PROJECT/editor/${dataset}?filter=id%3Deq%3D${idx}`,
```
Replace `YOUR_PROJECT` with your actual Supabase project ID.

### **4. Test Webhook**
```bash
curl -X POST http://localhost:5678/webhook/webhook-dataset \
  -H "Content-Type: application/json" \
  -d '{"body": {"dataset": "true-news", "idx": 30}}'
```

---

## 🧪 Testing

### **Test Case 1: True News**
```json
Input: {"body": {"dataset": "true-news", "idx": 30}}
Expected Output:
- tweetText: (article text)
- dataset: "true-news"
- datasetType: "TRUE"
- supabase_id: 30
```

### **Test Case 2: False News**
```json
Input: {"body": {"dataset": "false-news", "idx": 600}}
Expected Output:
- tweetText: (article text)
- dataset: "false-news"
- datasetType: "FALSE"
- supabase_id: 600
```

---

## 🔧 Troubleshooting

### **Error: "Supabase returned no data"**
- Check if row exists: `SELECT * FROM "true-news" WHERE id = 30;`
- Verify Supabase credentials
- Check table name matches exactly

### **Error: "Missing field 'text'"**
- Supabase row might not have `text` field
- Check column names in your Supabase table
- Update code to match your schema

### **Error: "Invalid dataset"**
- Only accepts: "true-news" or "false-news"
- Check webhook input format
- Verify dataset name spelling

---

## 📊 Output Compatibility

The output structure matches the main pipeline's expected format:

| Field | Twitter | Dataset | Notes |
|-------|---------|---------|-------|
| `tweetText` | ✅ Tweet text | ✅ Article text | Main content |
| `sourceType` | "twitter" | "dataset" | Source identifier |
| `tweetMetadata` | Tweet data | Article data | Metadata object |
| `accountData` | Twitter account | Empty (all 0) | Account info |
| `search_results` | Pre-fetched | Empty array | Populated by search nodes |

---

## 🚀 Next Steps

1. **Import this workflow** into n8n
2. **Configure Supabase** credentials
3. **Test with sample data** (T30, F600)
4. **Connect to main pipeline** (choose Option A, B, or C above)
5. **Remove redundant "Merge Dataset & Twitter Inputs"** if using Option A or B

---

**Version:** 1.0  
**Created:** December 14, 2025  
**Purpose:** Standalone dataset processor for WhatsApp input

