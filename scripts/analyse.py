import sqlite3

# Connect to the DB
conn = sqlite3.connect("db/variants.db")
cursor = conn.cursor()

# ----------- True Positives (TP) ----------------
tp_query = """
SELECT COUNT(*) FROM Variant v
JOIN ClinGen_Data c ON v.idVariant = c.variant_id
JOIN Delfos_Data d ON v.idVariant = d.variant_id
WHERE c.clinical_significance IN ('pathogenic', 'likely pathogenic')
  AND d.classification = 'accepted';
"""
tp = cursor.execute(tp_query).fetchone()[0]

# ----------- False Positives (FP) ----------------
fp_query = """
SELECT COUNT(*) FROM Variant v
JOIN ClinGen_Data c ON v.idVariant = c.variant_id
JOIN Delfos_Data d ON v.idVariant = d.variant_id
WHERE c.clinical_significance NOT IN ('pathogenic', 'likely pathogenic')
  AND d.classification = 'accepted';
"""
fp = cursor.execute(fp_query).fetchone()[0]

# ----------- False Negatives (FN) ----------------
fn_query = """
SELECT COUNT(*) FROM Variant v
JOIN ClinGen_Data c ON v.idVariant = c.variant_id
JOIN Delfos_Data d ON v.idVariant = d.variant_id
WHERE c.clinical_significance IN ('pathogenic', 'likely pathogenic')
  AND d.classification != 'accepted';
"""
fn = cursor.execute(fn_query).fetchone()[0]

# ----------- Calculate Metrics ----------------
precision = tp / (tp + fp) if (tp + fp) > 0 else 0
recall = tp / (tp + fn) if (tp + fn) > 0 else 0

# ----------- Display Results ----------------
print(f"✅ RESULTS:")
print(f"True Positives (TP): {tp}")
print(f"False Positives (FP): {fp}")
print(f"False Negatives (FN): {fn}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")

conn.close()
