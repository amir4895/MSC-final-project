# Changelog - v4.0 Release

**Release Date:** December 11, 2025  
**Previous Version:** v3.3  
**Workflow Size:** 133KB (was 90KB)  
**Node Count:** 57 nodes (was ~40)

---

## 🎯 Overview

Version 4.0 represents a major enhancement to the misinformation detection pipeline, focusing on **verification quality**, **date awareness**, and **architectural robustness**. The workflow now includes comprehensive protocols to prevent common fact-checking pitfalls like anachronistic verification and insufficient source validation.

---

## 🚨 Breaking Changes

### 1. New Classification Type: "UNVERIFIABLE"
- **Agent 1** can now return `"UNVERIFIABLE"` when credible date-appropriate sources cannot be found
- **Impact:** Downstream systems must handle this new classification
- **Rationale:** Honest acknowledgment when verification is impossible is better than guessing

### 2. Mandatory External Verification (Agent 2)
- **Agent 2** will FAIL if `sources_checked` is empty for Twitter accounts
- **Impact:** Agent 2 MUST perform web searches; cannot skip
- **Rationale:** Prevents lazy analysis relying only on account metrics

### 3. Dual-Path Architecture
- **Data flow changed** from linear to dual-path merge
- **Impact:** Debugging requires understanding two parallel paths
- **Benefit:** Original data preserved even if enrichment fails

---

## ✨ Major Features

### 1. Breaking News Verification Protocol (Agent 1)

#### **Date Extraction & Awareness**
```
Tweet Date: {{ $json.tweetMetadata.created_at }}
Current Date: {{ $now.format('YYYY-MM-DD') }}
```

#### **Time-Sensitive Verification**
- Extracts tweet posting date from metadata
- Compares to current date
- Requires sources from ±30 days of tweet date
- Prevents using 2020 sources for 2025 claims

#### **Date-Aware Searches**
```javascript
// For recent tweets (< 30 days old):
web_search("[claim] December 2025")
web_search("[claim] latest")

// For older tweets:
web_search("[claim] [tweet's month] [tweet's year]")
```

#### **UNVERIFIABLE Classification**
When no credible date-appropriate sources found:
```json
{
  "classification": "UNVERIFIABLE",
  "confidence": "low",
  "recommendation": "REQUIRES_MORE_INVESTIGATION",
  "overall_assessment": "No credible sources from [time period] found"
}
```

---

### 2. Source Quality Guidelines (Agent 1)

#### **High Credibility Sources:**
✅ Official sources (.gov, .edu, official org websites)  
✅ Major news agencies (Reuters, AP, BBC, CNN, NBC, Al Jazeera)  
✅ Academic/research institutions  
✅ Verified official accounts announcing their own actions  
✅ Fact-checking organizations (Snopes, FactCheck.org, PolitiFact)

#### **Lower Credibility Sources:**
⚠️ Blogs, opinion pieces  
⚠️ Unverified social media claims  
⚠️ Sites without clear sourcing  
⚠️ Partisan sources without corroboration

#### **Verification Approach:**
- Cross-reference 3+ credible sources (ideal)
- Check publication dates match claim timeframe
- Look for original sources, not aggregators
- If unclear/contradictory → Mark as UNVERIFIABLE

---

### 3. Mandatory External Verification (Agent 2)

#### **Required Web Searches:**
```javascript
// MANDATORY - Cannot skip these:
web_search("[username] Twitter credibility")
web_search("[username] bias fact check")
web_search("[username] misinformation") // if needed
```

#### **Enforcement:**
- `sources_checked` field CANNOT be empty for Twitter
- Agent will be REJECTED if empty
- Must record ALL searches, even if no results

#### **Political Bias Detection:**

**Indicators:**
- "BRICS News" → Pro-Russia/China bias
- "Geopolitics" → Political commentary, not neutral
- Partisan language → Note in red_flags
- "Breaking News" + political focus → Possible agenda

**Score Adjustments:**
- Known misinformation source: **-30 points**
- Partisan/biased source: **-10 to -20 points**
- Generally reliable: **+10 points**
- Established credible: **+15 points**
- Political bias indicators: **-5 to -15 points**

#### **Red Flags:**
- `tweets_per_day > 50` → "Very high activity"
- Political bias language in bio
- Known for spreading misinformation (from searches)
- New account (<90 days) with high activity
- Following >> followers (spam pattern)
- Profile incomplete (<3/7)

---

### 4. Dual-Path Merge Architecture

#### **Flow Diagram:**
```
Get Top N Most Viral
  ├─→ Enrich Twitter Account Data (HTTP)
  │     ↓ outputPropertyName: "enrichmentData"
  │   Merge Enriched Data (Code)
  │     ↓ Processes enrichmentData
  │   Merge2 (input 1)
  │     ↓
  └─→ (direct) ────────────────────────────────────────→ Merge2 (input 0)
                                                            ↓
                                               Build Final Enriched Data (Code)
                                                            ↓
                                                  Format Input Data
```

#### **Benefits:**
1. **Data Preservation**: Original tweet data flows directly to Merge2
2. **Parallel Processing**: Enrichment doesn't block main flow
3. **Fallback Logic**: If enrichment fails, original data still available
4. **Separation of Concerns**: Data vs. enrichment are separate paths

#### **HTTP Node Fix:**
```json
{
  "options": {
    "response": {
      "response": {
        "outputPropertyName": "enrichmentData"  // ✅ CRITICAL FIX
      }
    }
  }
}
```

**Before:** HTTP request overwrote entire input item  
**After:** HTTP response added as `enrichmentData` property, original data preserved

---

## 📊 Prompt Enhancements

### Agent 1 (Fact Check)
- **Lines Added:** ~150 lines of new protocols
- **Key Sections:**
  - 🚨 CRITICAL: CURRENT DATE & CONTEXT AWARENESS
  - SOURCE QUALITY GUIDELINES
  - 🚨 STEP 0: BREAKING NEWS VERIFICATION PROTOCOL
  - SELF-CHECK BEFORE FINALIZING

### Agent 2 (Credibility)
- **Lines Added:** ~120 lines of new protocols
- **Key Sections:**
  - 🚨 CRITICAL: MANDATORY EXTERNAL VERIFICATION
  - Political Bias Detection
  - Dynamic Score Adjustment
  - SELF-CHECK BEFORE SUBMITTING

---

## 📈 Workflow Statistics

| Metric | v3.3 | v4.0 | Change |
|--------|------|------|--------|
| **File Size** | 90KB | 133KB | +48% |
| **Node Count** | ~40 | 57 | +42% |
| **Agent 1 Prompt** | ~500 lines | ~650 lines | +30% |
| **Agent 2 Prompt** | ~400 lines | ~520 lines | +30% |
| **Classifications** | 7 types | 8 types | +1 (UNVERIFIABLE) |
| **Required Searches** | Optional | Mandatory | ✅ |

---

## 🔧 Technical Changes

### New Nodes:
1. **"Merge2"** - Combines dual paths
2. **"Build Final Enriched Data"** - Merges both inputs
3. **"Merge Enriched Data"** - Processes enrichmentData

### Modified Nodes:
1. **"Enrich Twitter Account Data"** - Added `outputPropertyName`
2. **"Agent 1 - Fact Check"** - Enhanced prompt
3. **"Agent 2 - Credibility"** - Enhanced prompt

### Configuration Changes:
```json
// HTTP Request node
{
  "outputPropertyName": "enrichmentData"  // NEW
}
```

---

## 📝 Documentation Updates

### Files Updated:
1. ✅ **README.md** - v4.0 features section
2. ✅ **QUICK_START.md** - Version update
3. ✅ **AI_CONTEXT.md** - v4.0 changes + TL;DR
4. ✅ **PENDING_IMPROVEMENTS.md** - Marked completed items
5. ✅ **COMPARISON_v3_vs_v4.md** - Created (architectural comparison)
6. ✅ **CHANGELOG_v4.0.md** - Created (this file)

---

## 🎯 Impact on Analysis Quality

### Fact-Checking Improvements:
- ✅ No more anachronistic verification
- ✅ Honest "UNVERIFIABLE" when sources lacking
- ✅ Date-appropriate source requirements
- ✅ 3+ source cross-referencing

### Credibility Analysis Improvements:
- ✅ Mandatory external verification (can't skip)
- ✅ Political bias detection
- ✅ Dynamic score adjustment based on reputation
- ✅ Red flag detection (high activity, bias indicators)

### Data Flow Improvements:
- ✅ No data loss during enrichment
- ✅ Fallback logic if enrichment fails
- ✅ Parallel processing (faster)
- ✅ Separation of concerns (cleaner)

---

## 🧪 Testing Recommendations

### Test Cases to Validate:

1. **Breaking News Tweet (Recent)**
   - Input: Tweet from today with "BREAKING" claim
   - Expected: Agent 1 searches with current month/year
   - Expected: Sources from ±30 days of today

2. **Old Tweet (Anachronistic)**
   - Input: Tweet from 2020 with old claim
   - Expected: Agent 1 searches with "2020"
   - Expected: Sources from 2020, not 2025

3. **Unverifiable Claim**
   - Input: Tweet with claim that has no credible sources
   - Expected: Classification = "UNVERIFIABLE"
   - Expected: Confidence = "low"

4. **Political Bias Account**
   - Input: Tweet from "BRICS News" or partisan account
   - Expected: Agent 2 flags bias in red_flags
   - Expected: Score penalty applied
   - Expected: sources_checked NOT empty

5. **High Activity Account**
   - Input: Tweet from account with 56+ tweets/day
   - Expected: Red flag: "Very high activity (56.98/day)"
   - Expected: Bot likelihood assessment

6. **Enrichment Failure**
   - Input: Tweet with invalid username for enrichment
   - Expected: Original tweet data still flows through
   - Expected: Fallback to basic accountData

---

## 🚀 Migration Guide

### From v3.3 to v4.0:

1. **Export your current workflow** (backup)
2. **Import v4.0 workflow** (`workflow-misinformation-detection-fixed.json`)
3. **Update credentials** (same as before)
4. **Test with manual trigger**
5. **Verify Google Sheets output** includes new fields
6. **Check for "UNVERIFIABLE" classification** handling in downstream systems

### Configuration Required:
- No new API keys needed
- Same credentials as v3.3
- Google Sheets columns auto-map

### Backward Compatibility:
- ✅ WhatsApp input: Compatible
- ✅ Twitter input: Compatible
- ✅ Google Sheets output: Compatible (new columns added)
- ⚠️ Classification types: New "UNVERIFIABLE" type added

---

## 🐛 Known Issues

### None Currently
All major issues from v3.3 have been resolved:
- ✅ Agent 3 enrichment working
- ✅ Data loss fixed
- ✅ HTTP node configured correctly
- ✅ Dual-path merge implemented

---

## 🔮 Future Roadmap

See [PENDING_IMPROVEMENTS.md](PENDING_IMPROVEMENTS.md) for:
- Batch processing option (multiple tweets per execution)
- Commenting/response functionality
- Pure manual testing mode
- Performance optimization

---

## 📞 Support

For issues or questions:
1. Check [README.md](README.md) for overview
2. Check [QUICK_START.md](QUICK_START.md) for setup
3. Check [AI_CONTEXT.md](AI_CONTEXT.md) for technical details
4. Check [COMPARISON_v3_vs_v4.md](COMPARISON_v3_vs_v4.md) for architecture

---

**Version:** 4.0  
**Released:** December 11, 2025  
**Maintained by:** MSC Student (Final Project)

