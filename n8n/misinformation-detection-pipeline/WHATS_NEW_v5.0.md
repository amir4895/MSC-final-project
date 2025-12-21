# What's New in v5.0 (December 13, 2025)

**Previous Version:** v4.0 (133KB, 57 nodes)  
**Current Version:** v5.0 (202KB, 83 nodes)  
**Size Increase:** +52% (+69KB)  
**Node Increase:** +45% (+26 nodes)

---

## 🎯 Major Innovation: Pre-Fetch Search System

### **The Problem v5.0 Solves:**

In v4.0, Agent 1 had to:
1. Read the tweet
2. Decide what to search
3. Call web_search tool
4. Parse results
5. Analyze credibility

**Issues:**
- LLM might search poorly (wrong keywords)
- LLM might fabricate URLs
- LLM might misinterpret "interest" as "confirmation"
- No control over source quality
- Expensive (multiple LLM calls for searches)

### **The v5.0 Solution:**

**Pre-fetch credible sources BEFORE Agent 1 runs:**

```
Tweet → Extract Search Terms → Google Custom Search API → Filter Credible Sources → Agent 1
```

**Benefits:**
1. ✅ **No URL fabrication** - Agent 1 gets real URLs upfront
2. ✅ **Better search quality** - Dedicated code nodes build smart queries
3. ✅ **Source filtering** - Only credible sources reach Agent 1
4. ✅ **Semantic guidance** - Agent 1 prompt teaches "interest" vs "confirmation"
5. ✅ **Cost reduction** - Fewer LLM web_search calls

---

## 🔧 New Nodes (26 Added)

### **Pre-Fetch Search Pipeline:**

1. **"1. Extract Search Terms"** (Code)
   - Cleans tweet text
   - Removes URLs, noise words
   - Extracts 3-6 key words
   - Adds date context (year/month for recent tweets)

2. **"2. Search Google"** (HTTP Request)
   - Calls Google Custom Search API
   - Returns top 10 results
   - Uses API key: `---GOOGLE-API-KEY-PLACEHOLDER---`
   - Custom Search Engine ID: `a16574f588c3a47df`

3. **"3. Filter Credible Sources"** (Code)
   - **3-Tier Source Ranking System:**
     - **Tier 1**: Reuters, AP, NYT, BBC, WSJ, WashPost (top-tier)
     - **Tier 2**: Regional papers, specialized outlets, official .gov/.edu
     - **Tier 3**: ESPN, TMZ, UK tabloids (legitimate but lower standards)
   - Excludes: Twitter, Reddit, YouTube, Facebook
   - Returns top 5 credible sources
   - Counts credible vs. total sources

4. **"1. Build Smart Search Query"** (Code) - IMPROVED VERSION
   - Extracts entities (names, places, organizations)
   - Extracts action verbs (signed, approved, rejected)
   - Removes opinion words (astonishing, corrupt, shocking)
   - Separates quoted facts from commentary
   - Adds wider date ranges (3-7 days for recent tweets)
   - Universal exclusions: `-site:reddit.com -site:twitter.com`

5. **"2. Search Google1"** & **"2. Search Google2"** (HTTP Requests)
   - Additional search attempts with different queries
   - Fallback if first search fails

6. **"3. Verify & Score Sources"** (Code)
   - Same filtering logic as "3. Filter Credible Sources"
   - Ranks and scores results

7. **"merge Tweet with web Search"** (Merge node)
   - Combines original tweet data with search results
   - Passes to Agent 1 with pre-fetched sources

---

## 🧠 Agent 1 Complete Rewrite

### **New Structure:**

```
═══════════════════════════════════════════════════════════════
AGENT 1A: PRIMARY FACT-CHECKING AGENT
═══════════════════════════════════════════════════════════════

Your Core Principle:
When in doubt → classify as UNVERIFIABLE (not LEGITIMATE)
Better to be cautious than to approve false information.

═══════════════════════════════════════════════════════════════
📊 YOUR INPUT DATA
═══════════════════════════════════════════════════════════════

## PRE-FETCHED SEARCH RESULTS
Search Status: {{ $json.search_status }}
Credible Sources Found: {{ $json.credible_sources_found }}
Total Results: {{ $json.total_results }}

Search Results:
{{ JSON.stringify($json.search_results, null, 2) }}
```

### **Key Sections:**

#### **1. STEP 1: EXTRACT CLAIMS & IDENTIFY TOPIC**
- Extract WHO, WHAT, WHEN, HOW MUCH
- Identify topic (Sports, Politics, Health, etc.)
- Determines which sources are credible for this topic

#### **2. STEP 2: SEMANTIC ANALYSIS - READ VERY CAREFULLY** ⭐ NEW
```
**CRITICAL: You must distinguish between COMPLETED ACTIONS vs INTEREST/SPECULATION**

✅ CONFIRMS A COMPLETED ACTION:
- "Player SIGNS contract"
- "Team ANNOUNCES signing"
- "Player AGREES TO deal"
- "Official: Player joins Team"

❌ Shows INTEREST/PURSUIT (NOT confirmation):
- "Teams INTERESTED in Player"
- "Team PURSUING Player"
- "Team TARGETS Player"
- "Team IN TALKS with Player"

❌ Shows SPECULATION (NOT confirmation):
- "Free agent PREDICTIONS"
- "POSSIBLE destinations"
- "COULD sign with"
- "RUMORS of deal"
```

**Reality Check Exercise:**
```
Example 1:
Tweet claims: "Player X signed with Team Y"
Search result title: "Teams interested in Player X"

Question: Does "interested" mean "signed"?
Answer: NO - interest ≠ completed signing
Conclusion: Claim is NOT confirmed
```

#### **3. STEP 3: DECIDE IF YOU NEED MORE SOURCES**
- If pre-fetched results CONFIRM → Proceed
- If results show only interest/speculation → Try additional web_search
- If still no confirmation → Classification = UNVERIFIABLE

#### **4. 🚨 ABSOLUTE RULES - READ BEFORE CONTINUING** ⭐ CRITICAL

**RULE 1: URL Citation**
```
YOU CAN ONLY CITE URLs THAT APPEAR IN:
- The search_results array above, OR
- Results from web_search tool you called

❌ NEVER ALLOWED:
- Fabricating URLs
- Creating plausible-looking URLs
- Using "XXXXXX" placeholders
- Inventing URLs like "https://espn.com/story/made-up-article"

✅ ALLOWED:
- Citing exact URLs from search_results
- Leaving sources empty [] if nothing confirms

If you cite even ONE fabricated URL, you have failed your task completely.
```

**RULE 2: Interest ≠ Confirmation**
```
These are NOT the same thing:
- "Teams interested" ≠ "Team signed"
- "Pursuing" ≠ "Completed"
- "Predictions" ≠ "Confirmed"
- "Rumors" ≠ "Facts"
```

**RULE 3: Verified Account ≠ Automatic Truth**
```
Even if:
- Account is verified ✓
- Account is ESPN/Reuters/BBC
- Account has millions of followers

You still must verify with actual news sources.
```

**RULE 4: Default to UNVERIFIABLE When Uncertain**
```
When in doubt:
- NOT sure if sources confirm? → UNVERIFIABLE
- Sources show interest only? → UNVERIFIABLE
- Can't find confirming sources? → UNVERIFIABLE

Do NOT default to LEGITIMATE. That's dangerous.
```

#### **5. 🛑 MANDATORY PRE-OUTPUT VERIFICATION** ⭐ NEW

**Question 1: Did sources CONFIRM or just DISCUSS?**
```
Review your semantic analysis from Step 2:
- How many sources CONFIRMED the completed action? _____
- How many sources showed only interest/speculation? _____

If confirmed count = 0:
→ You CANNOT classify as LEGITIMATE
→ Must be UNVERIFIABLE
```

**Question 2: Are you citing only REAL URLs?**
```
List every URL you plan to cite:
1. ____________________
2. ____________________

Now go back to "PRE-FETCHED SEARCH RESULTS" section.
Does each URL appear in that list? Check each one:
1. YES/NO
2. YES/NO

If ANY answer is NO → REMOVE THAT URL
```

**Question 3: Is your classification justified?**
```
If you're classifying as LEGITIMATE:
- [ ] Do sources confirm the COMPLETED action (not just interest)?
- [ ] Are you citing ONLY real URLs from search_results?
- [ ] Do sources confirm SPECIFIC details (amounts, dates)?

If ANY checkbox is unchecked → Change to UNVERIFIABLE
```

---

## 📊 Source Credibility Tiers

### **Tier 1: Top-Tier News (Highest Trust)**
- International: Reuters, AP, AFP
- US Papers: NYT, WashPost, WSJ, USA Today, LA Times
- UK News: BBC, Guardian, Telegraph
- Broadcast: CNN, NBC, ABC, CBS, CNBC
- Business: Bloomberg, FT, Forbes
- Public: NPR, PBS

### **Tier 2: Established Regional/Specialized**
- Regional US: Miami Herald, Denver Post, Seattle Times, Boston Globe
- International: Times of India, Al Jazeera, DW, France24
- Korean: Korea Times, Korea Herald, Yonhap
- Entertainment: Variety, Hollywood Reporter, Billboard, Rolling Stone
- Health/Science: Scientific American, Nature, WebMD, Mayo Clinic, NIH, CDC
- Tech: TechCrunch, The Verge, Wired, Ars Technica
- **Official Bodies**: MLB.com, NFL.com, NBA.com, NHL.com, FIFA.com, WHO.int, FDA.gov ⭐ NEW

### **Tier 3: Legitimate but Lower Standards**
- Sports: ESPN, SI, CBS Sports, Sky Sports, Bleacher Report
- Entertainment: EW, People, US Magazine, TMZ
- UK Tabloids: The Sun, Daily Mail, Mirror, Express
- Political: Politico, The Hill, Axios, Vox, Salon, HuffPost

### **Excluded: Social Media**
- Facebook, Twitter/X, Instagram, Threads
- Reddit, TikTok, YouTube
- Pinterest, Tumblr, Quora, Medium

---

## 🎯 Impact on Analysis Quality

### **Before v5.0 (Agent 1 searches on its own):**
- ❌ LLM might search poorly
- ❌ LLM might fabricate URLs
- ❌ LLM might confuse "interest" with "confirmation"
- ❌ No source quality control
- ❌ Expensive (multiple LLM calls)

### **After v5.0 (Pre-fetch + Semantic Guidance):**
- ✅ Smart search queries (dedicated code)
- ✅ Real URLs only (from Google API)
- ✅ Semantic training (interest vs. confirmation)
- ✅ Source filtering (3-tier system)
- ✅ Cost-effective (fewer LLM calls)

---

## 🔄 Workflow Changes

### **Old Flow (v4.0):**
```
Tweet → Format → Parse → Agent 1 (searches internally) → Agent 2 → Agent 3 → Agent 4
```

### **New Flow (v5.0):**
```
Tweet → Extract Search Terms → Google API → Filter Sources → Format → Parse → Agent 1 (uses pre-fetched) → Agent 2 → Agent 3 → Agent 4
```

---

## 📈 Statistics

| Metric | v4.0 | v5.0 | Change |
|--------|------|------|--------|
| **File Size** | 133KB | 202KB | +52% |
| **Node Count** | 57 | 83 | +45% |
| **Agent 1 Prompt** | ~650 lines | ~900 lines | +38% |
| **Search Nodes** | 0 | 7 | NEW |
| **Source Tiers** | 0 | 3 | NEW |
| **Credible Sources** | ~30 | ~70+ | +133% |

---

## 🧪 Key Improvements

### **1. No More URL Fabrication**
- Agent 1 gets real URLs from Google API
- Can only cite URLs from `search_results` array
- Empty sources `[]` if nothing confirms

### **2. Semantic Understanding**
- Teaches Agent 1 to distinguish:
  - "signed" vs. "interested"
  - "confirmed" vs. "rumored"
  - "completed" vs. "pursuing"

### **3. Source Quality Control**
- 3-tier ranking system
- Official bodies added (MLB.com, NFL.com, FIFA.com, etc.)
- Social media excluded

### **4. Smart Search Queries**
- Extracts entities (names, places)
- Extracts actions (signed, approved)
- Removes opinions (shocking, corrupt)
- Adds date context (wider ranges for recent tweets)

### **5. Mandatory Verification Checklist**
- Agent 1 must answer 4 questions before output
- Forces review of semantic analysis
- Prevents premature LEGITIMATE classification

---

## 🚀 Testing Recommendations

### **Test Case 1: Sports Rumor vs. Confirmation**
- Input: Tweet claiming "Player X signed with Team Y"
- Pre-fetch finds: "Teams interested in Player X"
- Expected: Agent 1 marks UNVERIFIABLE (interest ≠ signing)

### **Test Case 2: URL Fabrication Prevention**
- Input: Tweet with claim not in search results
- Expected: Agent 1 returns empty sources `[]` or uses web_search
- Expected: NO fabricated URLs

### **Test Case 3: Source Tier Filtering**
- Input: Tweet with claim
- Pre-fetch finds: Reddit, Twitter, ESPN, Reuters
- Expected: Only ESPN, Reuters in `search_results` (Reddit/Twitter excluded)

### **Test Case 4: Semantic Analysis**
- Input: Tweet: "Player signs 3-year deal"
- Search result: "Player signs 3-year deal with Team"
- Expected: LEGITIMATE (confirms completed action)

### **Test Case 5: Opinion Removal**
- Input: Tweet: "Shocking! Player X's corrupt deal with Team Y"
- Search query: Should extract "Player X deal Team Y" (no "shocking", "corrupt")
- Expected: Clean, factual search query

---

## 📝 Documentation Status

- [ ] README.md - Update to v5.0
- [ ] QUICK_START.md - Update version
- [ ] AI_CONTEXT.md - Add v5.0 changes
- [ ] PENDING_IMPROVEMENTS.md - Mark completed
- [ ] CHANGELOG_v5.0.md - Create comprehensive changelog

---

**Version:** 5.0  
**Released:** December 13, 2025  
**Maintained by:** MSC Student (Final Project)

