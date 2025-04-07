import sqlite3

def create_tables(db_path="db/variants.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table for unique variants
    c.execute('''
        CREATE TABLE IF NOT EXISTS Variant (
            idVariant INTEGER PRIMARY KEY AUTOINCREMENT,
            chr TEXT,
            pos INTEGER,
            referenceAllele TEXT,
            altAllele TEXT
        )
    ''')

    # Table for ClinGen annotations
    c.execute('''
        CREATE TABLE IF NOT EXISTS ClinGen_Data (
            CHROM TEXT,
            POS INTEGER,
            ID TEXT,
            REF TEXT,
            ALT TEXT,
            QUAL TEXT,
            FILTER TEXT,
            INTERPRETATION TEXT,
            MET_CRITERIA TEXT,
            NOT_MET_CRITERIA TEXT,
            EXPERT_PANEL TEXT,
            VARIANT_ID INTEGER,
            FOREIGN KEY (VARIANT_ID) REFERENCES Variant(idVariant)
        )
    ''')

    # Table for Delfos annotations
    c.execute('''
        CREATE TABLE IF NOT EXISTS Delfos_Data (
            CHROM TEXT,
            POS INTEGER,
            ID TEXT,
            REF TEXT,
            ALT TEXT,
            QUAL TEXT,
            FILTER TEXT,
            PHENOTYPE TEXT,
            INTERPRETATION TEXT,
            INTERPRETATION_REASON TEXT,
            CLINICAL_ACTIONABILITY TEXT,
            GENE TEXT,
            VARIANT_ID INTEGER,
            FOREIGN KEY (VARIANT_ID) REFERENCES Variant(idVariant)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables("db/variants.db")
    print("Data loaded correctly!")
