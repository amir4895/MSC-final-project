#!/usr/bin/env python3
"""
Confusion Matrix Generator for n8n Misinformation Detection System
Analyzes Google Sheets export to calculate accuracy metrics

FIXED: Handles both string and boolean ground_truth values
"""

import pandas as pd
import sys
from datetime import datetime


def calculate_metrics(csv_file):
    """
    Calculate confusion matrix and performance metrics from Google Sheets CSV export
    """

    print("=" * 80)
    print("MISINFORMATION DETECTION SYSTEM - ACCURACY ANALYSIS")
    print("=" * 80)
    print(f"\nAnalyzing: {csv_file}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Load data
    try:
        df = pd.read_csv(csv_file)
        print(f"✅ Loaded {len(df)} total rows\n")
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {csv_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR: Failed to load CSV: {e}")
        sys.exit(1)

    # Check required columns
    required_columns = ['ground_truth', 'match_type']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"❌ ERROR: Missing required columns: {missing_columns}")
        sys.exit(1)

    # FIXED: Convert ground_truth to string and handle both boolean and string values
    df['ground_truth'] = df['ground_truth'].astype(str).str.upper()

    # Filter to only rows with ground truth (exclude UNKNOWN/NAN)
    df_with_truth = df[df['ground_truth'].isin(['TRUE', 'FALSE'])]
    total_with_truth = len(df_with_truth)
    total_without_truth = len(df) - total_with_truth

    print(f"Dataset Tests (with ground truth): {total_with_truth}")
    print(f"Real-time Tweets (no ground truth): {total_without_truth}")
    print(f"Total Rows: {len(df)}\n")

    if total_with_truth == 0:
        print("⚠️  WARNING: No dataset tests found!")
        print("   Ground truth values found:", df['ground_truth'].unique())
        return

    # Count confusion matrix categories
    tp = len(df_with_truth[df_with_truth['match_type'] == 'TP'])
    tn = len(df_with_truth[df_with_truth['match_type'] == 'TN'])
    fp = len(df_with_truth[df_with_truth['match_type'] == 'FP'])
    fn = len(df_with_truth[df_with_truth['match_type'] == 'FN'])

    total = tp + tn + fp + fn

    # Print Confusion Matrix
    print("=" * 80)
    print("CONFUSION MATRIX")
    print("=" * 80)
    print()
    print("                    Predicted")
    print("                Fake (FALSE)    Real (TRUE)")
    print("              ┌─────────────┬─────────────┐")
    print(f"Actual  Fake  │     {tp:3d}     │     {fn:3d}     │")
    print("        (FALSE)│     TP      │     FN      │")
    print("              ├─────────────┼─────────────┤")
    print(f"        Real  │     {fp:3d}     │     {tn:3d}     │")
    print("        (TRUE)│     FP      │     TN      │")
    print("              └─────────────┴─────────────┘")
    print()

    # Calculate metrics
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # Print Performance Metrics
    print("=" * 80)
    print("PERFORMANCE METRICS")
    print("=" * 80)
    print()
    print(f"Accuracy:  {accuracy:.1%}  ({tp + tn}/{total})")
    print(f"           How often the system is correct overall")
    print()
    print(f"Precision: {precision:.1%}  ({tp}/{tp + fp})")
    print(f"           When system flags as fake, how often is it correct?")
    print()
    print(f"Recall:    {recall:.1%}  ({tp}/{tp + fn})")
    print(f"           Of all actual fake news, how much did we catch?")
    print()
    print(f"F1-Score:  {f1_score:.1%}")
    print(f"           Harmonic mean of precision and recall")
    print()

    # Print Detailed Breakdown
    print("=" * 80)
    print("DETAILED BREAKDOWN")
    print("=" * 80)
    print()
    print(f"True Positives (TP):   {tp:3d}  - Correctly identified fake news")
    print(f"True Negatives (TN):   {tn:3d}  - Correctly identified real news")
    print(f"False Positives (FP):  {fp:3d}  - Real news incorrectly flagged as fake")
    print(f"False Negatives (FN):  {fn:3d}  - Fake news missed (not detected)")
    print(f"{'─' * 40}")
    print(f"Total Dataset Tests:   {total:3d}")
    print()

    # Error Analysis
    if fp > 0 or fn > 0:
        print("=" * 80)
        print("ERROR ANALYSIS")
        print("=" * 80)
        print()

        if fp > 0:
            print(f"⚠️  FALSE POSITIVES (False Alarms): {fp}")
            print("   Real news incorrectly flagged as fake:")
            fp_rows = df_with_truth[df_with_truth['match_type'] == 'FP']
            for idx, row in fp_rows.iterrows():
                classification = row.get('fact_check_classification', 'UNKNOWN')
                preview = str(row.get('content_preview', 'No preview'))[:60]
                print(f"   - {classification}: {preview}...")
            print()

        if fn > 0:
            print(f"❌ FALSE NEGATIVES (Missed Detections): {fn}")
            print("   Fake news that was not caught:")
            fn_rows = df_with_truth[df_with_truth['match_type'] == 'FN']
            for idx, row in fn_rows.iterrows():
                classification = row.get('fact_check_classification', 'UNKNOWN')
                preview = str(row.get('content_preview', 'No preview'))[:60]
                print(f"   - {classification}: {preview}...")
            print()

    # Classification Distribution
    if 'fact_check_classification' in df_with_truth.columns:
        print("=" * 80)
        print("CLASSIFICATION DISTRIBUTION (Dataset Tests Only)")
        print("=" * 80)
        print()
        class_counts = df_with_truth['fact_check_classification'].value_counts()
        for classification, count in class_counts.items():
            percentage = (count / total_with_truth) * 100
            print(f"{classification:20s}: {count:3d} ({percentage:5.1f}%)")
        print()

    # Ground Truth Distribution
    print("=" * 80)
    print("GROUND TRUTH DISTRIBUTION")
    print("=" * 80)
    print()
    true_count = len(df_with_truth[df_with_truth['ground_truth'] == 'TRUE'])
    false_count = len(df_with_truth[df_with_truth['ground_truth'] == 'FALSE'])
    print(f"Real News (TRUE):  {true_count:3d} ({true_count / total_with_truth * 100:5.1f}%)")
    print(f"Fake News (FALSE): {false_count:3d} ({false_count / total_with_truth * 100:5.1f}%)")
    print()

    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print()

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'tp': tp,
        'tn': tn,
        'fp': fp,
        'fn': fn,
        'total': total
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python confusion_matrix.py <csv_file>")
        print()
        print("Example:")
        print("  python confusion_matrix.py results.csv")
        sys.exit(1)

    csv_file = sys.argv[1]
    calculate_metrics(csv_file)

