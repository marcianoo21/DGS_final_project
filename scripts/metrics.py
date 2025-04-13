import sqlite3
import pandas as pd

CLINGEN_VCF_PATH = "data/VCF_clingen.vcf"
DELFOS_VCF_PATH = "data/VCF_ulises.vcf"
DB_PATH = "db/variants.db"

conn = sqlite3.connect(DB_PATH)

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
print("Initial Data Size:", df.shape[0])

df.drop_duplicates(subset=['chrom', 'pos', 'ref', 'alt'], inplace=True)
print("Data after deduplication:", df.shape[0])

# finding valid variations
df = df[df['delfos_interpretation'].str.contains("ACCEPTED", na=False)]

print("Data after filtering for 'ACCEPTED WITH STRONG EVIDENCE' in DELFOS:", df.shape)

def categorize(row):
    delfos = row['delfos_interpretation']
    clingen = row['clingen_interpretation']
    
    if delfos and 'ACCEPTED' in delfos:
        if clingen in ['Pathogenic', 'Likely Pathogenic']:
            return 'Concordant'
        elif clingen in ['Benign', 'Likely Benign', 'Uncertain Significance']:
            return 'Discordant'
        elif pd.isna(clingen):
            return 'No ClinGen Match'
        else:
            return 'Unclassified'
    return 'Not Accepted by DELFOS'

df['concordance_status'] = df.apply(categorize, axis=1)

summary = df['concordance_status'].value_counts().rename_axis('Interpretation Match').reset_index(name='Variant Count')
print("Summary of Interpretation Concordance:")
print(summary)

df.to_csv("results/interpretation_concordance_analysis.csv", index=False)
summary.to_csv("results/concordance_summary.csv", index=False)

conn.close()

print("Data saved in results directory.")

# METRICS

total = len(df)
concordant = (df['concordance_status'] == 'Concordant').sum()
discordant = (df['concordance_status'] == 'Discordant').sum()
not_accepted = (df['concordance_status'] == 'Not Accepted by DELFOS').sum()
no_clingen = (df['concordance_status'] == 'No ClinGen Match').sum()

concordance_rate = concordant / total * 100
discordance_rate = discordant / total * 100
clingen_coverage_rate = (total - no_clingen) / total * 100

metrics = pd.DataFrame([
    ['Total variants analyzed', total],
    ['Concordant interpretations', concordant],
    ['Discordant interpretations', discordant],
    ['Not accepted by DELFOS', not_accepted],
    ['No ClinGen match', no_clingen],
    ['Concordance rate (%)', round(concordance_rate, 2)],
    ['Discordance rate (%)', round(discordance_rate, 2)],
    ['ClinGen coverage rate (%)', round(clingen_coverage_rate, 2)],
], columns=['Metric', 'Value'])

print(metrics)

metrics.to_csv("results/statistical_parameters_summary.csv", index=False, encoding="utf-8")

print("Saved!")