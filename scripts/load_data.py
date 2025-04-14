import sqlite3

DB_PATH = "db/variants.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS ClinGen_Variants;
DROP TABLE IF EXISTS DELFOS_Variants;
DROP TABLE IF EXISTS DELFOS_Variants_2;


CREATE TABLE ClinGen_Variants (
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

CREATE TABLE DELFOS_Variants (
    chrom TEXT,
    pos INTEGER,
    id TEXT,
    ref TEXT,
    alt TEXT,
    phenotype TEXT,
    interpretation TEXT,
    interpretation_reason TEXT,
    clinical_actionability TEXT,
    gene TEXT
);
""")

conn.close()

print("Data loaded succesfully!")