import sqlite3
import pandas as pd

def compare_variants(db_path="db/variants.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    SELECT
        v.idVariant,
        v.chr AS Chromosome,
        v.pos AS Position,
        v.referenceAllele AS REF,
        v.altAllele AS ALT,
        c.INTERPRETATION AS ClinGen_Interpretation,
        d.INTERPRETATION AS Delfos_Interpretation,
        CASE
            WHEN LOWER(c.INTERPRETATION) = LOWER(d.INTERPRETATION) THEN 'Match'
            ELSE 'Discrepancy'
        END AS Interpretation_Comparison
    FROM Variant v
    JOIN ClinGen_Data c ON v.idVariant = c.VARIANT_ID
    JOIN Delfos_Data d ON v.idVariant = d.VARIANT_ID
    WHERE
        v.chr = c.CHROM AND
        v.chr = d.CHROM AND
        v.pos = c.POS AND
        v.pos = d.POS AND
        v.referenceAllele = c.REF AND
        v.referenceAllele = d.REF AND
        v.altAllele = c.ALT AND
        v.altAllele = d.ALT;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Show summary
    print("✅ Variant Comparison Results:")
    print(df)
    print("\n📊 Summary:")
    print(df["Interpretation_Comparison"].value_counts())

    # Optionally, save to CSV
    df.to_csv("reports/comparison_results.csv", index=False)
    print("\n📁 Saved to 'reports/comparison_results.csv'")

if __name__ == "__main__":
    compare_variants()
