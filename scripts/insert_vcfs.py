import sqlite3
import pandas as pd
from io import StringIO


CLINGEN_VCF_PATH = "data/VCF_clingen.vcf"
DELFOS_VCF_PATH = "data/VCF_ulises.vcf"
DB_PATH = "db/variants.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

def parse_info(info, keys):
    parsed = dict(kv.split("=", 1) for kv in info.split(";") if "=" in kv)
    return [parsed.get(k) for k in keys]

# ClinGen 
with open(CLINGEN_VCF_PATH, "r") as f:
    lines = [l for l in f if not l.startswith("##")]
clingen_df = pd.read_csv(StringIO("".join(lines)), sep="\t")
clingen_df[['interpretation', 'criteria_met', 'criteria_not_met', 'expert_panel']] = \
    clingen_df['INFO'].apply(lambda i: pd.Series(parse_info(i, ['INTERPRETATION', 'MET_CRITERIA', 'NOT_MET_CRITERIA', 'EXPERT_PANEL'])))
clingen_df = clingen_df.rename(columns={'#CHROM': 'chrom', 'POS': 'pos', 'ID': 'id', 'REF': 'ref', 'ALT': 'alt'})
clingen_df[['chrom', 'pos', 'id', 'ref', 'alt', 'interpretation', 'criteria_met', 'criteria_not_met', 'expert_panel']]\
    .to_sql("ClinGen_Variants", conn, if_exists="append", index=False)

# DELFOS 
with open(DELFOS_VCF_PATH, "r") as f:
    lines = [l for l in f if not l.startswith("##")]
delfos_df = pd.read_csv(StringIO("".join(lines)), sep="\t")
delfos_df[['phenotype', 'interpretation', 'interpretation_reason', 'clinical_actionability', 'gene']] = \
    delfos_df['INFO'].apply(lambda i: pd.Series(parse_info(i, ['PHENOTYPE', 'INTERPRETATION', 'INTERPRETATION_REASON', 'CLINICAL_ACTIONABILITY', 'GENE'])))
delfos_df = delfos_df.rename(columns={'#CHROM': 'chrom', 'POS': 'pos', 'ID': 'id', 'REF': 'ref', 'ALT': 'alt'})
delfos_df[['chrom', 'pos', 'id', 'ref', 'alt', 'phenotype', 'interpretation', 'interpretation_reason', 'clinical_actionability', 'gene']]\
    .to_sql("DELFOS_Variants", conn, if_exists="append", index=False)
    
    
print("Done!")