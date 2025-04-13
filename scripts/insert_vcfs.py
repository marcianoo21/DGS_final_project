import sqlite3
import pandas as pd
from io import StringIO

# Utility: parse INFO field for relevant keys
def parse_info(info, keys):
    parts = dict(kv.split('=') for kv in info.split(';') if '=' in kv)
    return [parts.get(k) for k in keys]


conn = sqlite3.connect("db/variants.db")
cur = conn.cursor()

# 3. Load and insert ClinGen data
with open("data/VCF_clingen.vcf", "r") as f:
    lines = [l for l in f if not l.startswith("##")]
clingen_df = pd.read_csv(StringIO("".join(lines)), sep="\t")
clingen_df[['interpretation', 'criteria_met', 'criteria_not_met', 'expert_panel']] = clingen_df['INFO'].apply(
    lambda info: pd.Series(parse_info(info, ['INTERPRETATION', 'MET_CRITERIA', 'NOT_MET_CRITERIA', 'EXPERT_PANEL']))
)
clingen_df[['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'interpretation', 'criteria_met', 'criteria_not_met', 'expert_panel']]\
    .rename(columns={'#CHROM': 'chrom', 'POS': 'pos', 'ID': 'id', 'REF': 'ref', 'ALT': 'alt'})\
    .to_sql("ClinGen_Variants", conn, if_exists="append", index=False)

# 4. Load and insert DELFOS data
with open("data/VCF_ulises.vcf", "r") as f:
    lines = [l for l in f if not l.startswith("##")]
delfos_df = pd.read_csv(StringIO("".join(lines)), sep="\t")
delfos_df[['phenotype', 'interpretation', 'interpretation_reason', 'clinical_actionability']] = \
    delfos_df['INFO'].apply(lambda info: pd.Series(parse_info(info, ['PHENOTYPE', 'INTERPRETATION', 'INTERPRETATION_REASON', 'CLINICAL_ACTIONABILITY'])))
delfos_df[['#CHROM', 'POS', 'ID', 'REF', 'ALT', 'phenotype', 'interpretation', 'interpretation_reason', 'clinical_actionability']]\
    .rename(columns={'#CHROM': 'chrom', 'POS': 'pos', 'ID': 'id', 'REF': 'ref', 'ALT': 'alt'})\
    .to_sql("DELFOS_Variants", conn, if_exists="append", index=False)


print("DONE!")