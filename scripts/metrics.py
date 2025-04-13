import sqlite3
import pandas as pd

# Connect to the existing SQLite DB
conn = sqlite3.connect("db/variants.db")
cur = conn.cursor()

#creating tables
cur.executescript("""
DROP TABLE IF EXISTS ClinGen_Variants;
DROP TABLE IF EXISTS DELFOS_Variants;
                  
CREATE TABLE IF NOT EXISTS ClinGen_Variants (
    chrom TEXT,
    pos INTEGER,
    id TEXT,
    ref TEXT,
    alt TEXT,
    interpretation TEXT,
    criteria_met TEXT,
    criteria_not_met TEXT,
    expert_panel TEXT
);

CREATE TABLE IF NOT EXISTS DELFOS_Variants (
    chrom TEXT,
    pos INTEGER,
    id TEXT,
    ref TEXT,
    alt TEXT,
    phenotype TEXT,
    interpretation TEXT,
    interpretation_reason TEXT,
    clinical_actionability TEXT
);
""")

query = """
SELECT 
    d.chrom, d.pos, d.ref, d.alt,
    d.interpretation AS delfos_interpretation,
    c.interpretation AS clingen_interpretation
FROM DELFOS_Variants d
LEFT JOIN ClinGen_Variants c
ON d.chrom = c.chrom AND d.pos = c.pos AND d.ref = c.ref AND d.alt = c.alt
WHERE d.phenotype LIKE '%MONOGENIC DIABETES%'
"""

df = pd.read_sql_query(query, conn)

# Normalize for comparison
df['delfos_interpretation'] = df['delfos_interpretation'].str.upper().str.strip()
df['clingen_interpretation'] = df['clingen_interpretation'].str.title().str.strip()

# Step 2: Categorize interpretation concordance
def categorize(row):
    delfos = row['delfos_interpretation']
    clingen = row['clingen_interpretation']
    
    if delfos and 'ACCEPTED' in delfos:
        if clingen in ['Pathogenic', 'Likely Pathogenic']:
            return 'Concordant'
        elif clingen in ['Benign', 'Likely Benign', 'Uncertain Significance']:
            return 'Discordant'
        elif clingen is None:
            return 'No ClinGen Match'
        else:
            return 'Unclassified'
    return 'Not Accepted by DELFOS'

df['concordance_status'] = df.apply(categorize, axis=1)

# Step 3: Statistics summary
summary = df['concordance_status'].value_counts().rename_axis('Interpretation Match').reset_index(name='Variant Count')
print(summary)

# Optional: save to CSV
df.to_csv("interpretation_concordance_analysis.csv", index=False)