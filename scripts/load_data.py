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
            idClinGen INTEGER PRIMARY KEY AUTOINCREMENT,
            variant_id INTEGER,
            clinical_significance TEXT,
            FOREIGN KEY (variant_id) REFERENCES Variant(idVariant)
        )
    ''')

    # Table for Delfos annotations
    c.execute('''
        CREATE TABLE IF NOT EXISTS Delfos_Data (
            idDelfos INTEGER PRIMARY KEY AUTOINCREMENT,
            variant_id INTEGER,
            classification TEXT,
            FOREIGN KEY (variant_id) REFERENCES Variant(idVariant)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
