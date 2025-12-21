# Analysis Tools

This directory contains tools for analyzing the performance of the misinformation detection system.

---

## 📁 Files

### **confusion_matrix.py**
Python script that calculates confusion matrix and performance metrics from Google Sheets export.

**Features:**
- Calculates accuracy, precision, recall, and F1-score
- Generates confusion matrix visualization
- Provides detailed error analysis
- Shows classification distribution
- Handles both dataset tests and real-time tweets

### **results.csv**
Sample Google Sheets export containing test results with ground truth labels.

**Required Columns:**
- `ground_truth` - TRUE/FALSE (actual label)
- `match_type` - TP/TN/FP/FN (confusion matrix category)
- `fact_check_classification` - System's classification
- `content_preview` - Preview of the content

---

## 🚀 Usage

### **Run Analysis:**

```bash
# From the analysis directory
python confusion_matrix.py results.csv

# Or from project root
python analysis/confusion_matrix.py analysis/results.csv
```

### **With Your Own Data:**

1. Export your Google Sheets results as CSV
2. Ensure it has the required columns (see above)
3. Run the script:

```bash
python confusion_matrix.py your_results.csv
```

---

## 📊 Output

The script generates a comprehensive report including:

### **1. Confusion Matrix**
```
                    Predicted
                Fake (FALSE)    Real (TRUE)
              ┌─────────────┬─────────────┐
Actual  Fake  │     TP      │     FN      │
        (FALSE)│             │             │
              ├─────────────┼─────────────┤
        Real  │     FP      │     TN      │
        (TRUE)│             │             │
              └─────────────┴─────────────┘
```

### **2. Performance Metrics**
- **Accuracy:** Overall correctness
- **Precision:** When flagged as fake, how often correct?
- **Recall:** Of all fake news, how much caught?
- **F1-Score:** Harmonic mean of precision and recall

### **3. Detailed Breakdown**
- True Positives (TP): Correctly identified fake news
- True Negatives (TN): Correctly identified real news
- False Positives (FP): Real news incorrectly flagged
- False Negatives (FN): Fake news missed

### **4. Error Analysis**
- Lists all false positives with previews
- Lists all false negatives with previews
- Helps identify patterns in errors

### **5. Classification Distribution**
- Shows how many items in each classification category
- Percentages for each category

### **6. Ground Truth Distribution**
- Real vs. Fake news breakdown
- Helps verify dataset balance

---

## 📋 Requirements

```bash
pip install pandas
```

---

## 🧪 Example Output

```
================================================================================
MISINFORMATION DETECTION SYSTEM - ACCURACY ANALYSIS
================================================================================

Analyzing: results.csv
Generated: 2025-12-21 14:30:00

✅ Loaded 150 total rows

Dataset Tests (with ground truth): 100
Real-time Tweets (no ground truth): 50
Total Rows: 150

================================================================================
CONFUSION MATRIX
================================================================================

                    Predicted
                Fake (FALSE)    Real (TRUE)
              ┌─────────────┬─────────────┐
Actual  Fake  │      45     │       5     │
        (FALSE)│     TP      │     FN      │
              ├─────────────┼─────────────┤
        Real  │       8     │      42     │
        (TRUE)│     FP      │     TN      │
              └─────────────┴─────────────┘

================================================================================
PERFORMANCE METRICS
================================================================================

Accuracy:  87.0%  (87/100)
           How often the system is correct overall

Precision: 84.9%  (45/53)
           When system flags as fake, how often is it correct?

Recall:    90.0%  (45/50)
           Of all actual fake news, how much did we catch?

F1-Score:  87.4%
           Harmonic mean of precision and recall
```

---

## 📝 Notes

### **Ground Truth Values:**
- The script handles both string (`"TRUE"`, `"FALSE"`) and boolean (`True`, `False`) values
- Values are automatically converted to uppercase for consistency
- Rows without ground truth (real-time tweets) are excluded from metrics

### **Match Type Categories:**
- **TP (True Positive):** Fake news correctly identified as fake
- **TN (True Negative):** Real news correctly identified as real
- **FP (False Positive):** Real news incorrectly flagged as fake
- **FN (False Negative):** Fake news incorrectly classified as real

### **Dataset vs. Real-time:**
- **Dataset tests:** Have ground truth, used for metrics calculation
- **Real-time tweets:** No ground truth, excluded from confusion matrix

---

## 🔗 Related Files

- Main workflow: `../n8n/misinformation-detection-pipeline/workflow-misinformation-detection-fixed.json`
- Documentation: `../n8n/misinformation-detection-pipeline/README.md`
- Quick start: `../n8n/misinformation-detection-pipeline/QUICK_START.md`

---

## 📊 Understanding the Metrics

### **Accuracy**
- **Definition:** (TP + TN) / Total
- **Meaning:** Overall correctness rate
- **Good when:** Dataset is balanced

### **Precision**
- **Definition:** TP / (TP + FP)
- **Meaning:** Of items flagged as fake, how many are actually fake?
- **Important when:** False alarms are costly

### **Recall (Sensitivity)**
- **Definition:** TP / (TP + FN)
- **Meaning:** Of all actual fake news, how much did we catch?
- **Important when:** Missing fake news is costly

### **F1-Score**
- **Definition:** 2 × (Precision × Recall) / (Precision + Recall)
- **Meaning:** Balance between precision and recall
- **Good for:** Comparing different models

---

## 🎯 Interpreting Results

### **High Accuracy, High Precision, High Recall:**
✅ **Excellent!** System is working well.

### **High Accuracy, Low Recall:**
⚠️ **Conservative:** System is accurate but misses some fake news.

### **High Accuracy, Low Precision:**
⚠️ **Aggressive:** System catches fake news but has many false alarms.

### **Low Accuracy:**
❌ **Needs Improvement:** System needs tuning or more training data.

---

**Version:** 1.0  
**Last Updated:** December 21, 2025  
**Part of:** MSC Final Project - Misinformation Detection System

