import sqlite3
import pandas as pd
import os

def connect_db(db_path="db/variants.db"):
    return sqlite3.connect(db_path)

def query_all_variant_interpretations(conn):
    query = '''
    SELECT 
        v.chr,
        v.pos,
        v.referenceAllele,
        v.altAllele,
        c.INTERPRETATION AS ClinGen_Interpretation,
        d.INTERPRETATION AS Delfos_Interpretation
    FROM Variant v
    LEFT JOIN ClinGen_Data c ON v.idVariant = c.VARIANT_ID
    LEFT JOIN Delfos_Data d ON v.idVariant = d.VARIANT_ID
    '''
    return pd.read_sql_query(query, conn)

def query_conflicting_interpretations(conn):
    query = '''
    SELECT 
        v.chr,
        v.pos,
        v.referenceAllele,
        v.altAllele,
        c.INTERPRETATION AS ClinGen_Interpretation,
        d.INTERPRETATION AS Delfos_Interpretation
    FROM Variant v
    INNER JOIN ClinGen_Data c ON v.idVariant = c.VARIANT_ID
    INNER JOIN Delfos_Data d ON v.idVariant = d.VARIANT_ID
    WHERE c.INTERPRETATION IS NOT NULL AND d.INTERPRETATION IS NOT NULL
      AND c.INTERPRETATION != d.INTERPRETATION
    '''
    return pd.read_sql_query(query, conn)

def query_actionable_variants(conn):
    query = '''
    SELECT 
        v.chr,
        v.pos,
        v.referenceAllele,
        v.altAllele,
        d.CLINICAL_ACTIONABILITY,
        d.INTERPRETATION,
        d.PHENOTYPE,
        d.GENE
    FROM Variant v
    INNER JOIN Delfos_Data d ON v.idVariant = d.VARIANT_ID
    WHERE d.CLINICAL_ACTIONABILITY IS NOT NULL AND d.CLINICAL_ACTIONABILITY != ''
    '''
    return pd.read_sql_query(query, conn)

def export_to_excel(dfs: dict, filename: str):
    os.makedirs("reports", exist_ok=True)
    filepath = os.path.join("reports", filename)

    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        for sheet_name, df in dfs.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Excel sheet names max = 31 chars
    print(f"📁 Excel file exported to: {filepath}")

def run_all_reports():
    conn = connect_db()

    dfs = {
        "All_Variant_Interpretations": query_all_variant_interpretations(conn),
        "Conflicting_Interpretations": query_conflicting_interpretations(conn),
        "Actionable_Variants": query_actionable_variants(conn)
    }

    export_to_excel(dfs, "variant_report.xlsx")
    conn.close()
    print("✅ All reports saved to Excel!")

if __name__ == "__main__":
    run_all_reports()
