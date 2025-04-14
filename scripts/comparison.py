import sqlite3
import pandas as pd

# Function to load ClinGen variants from the database
def load_clingen_variants_from_db(db_path="db/variants.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT DISTINCT C.CHROM, C.POS, C.REF, C.ALT, C.INTERPRETATION, C.EXPERT_PANEL
        FROM ClinGen_Data C
        WHERE C.EXPERT_PANEL LIKE "%Monogenic Diabetes%"
    ''')

    clingen_variants = cursor.fetchall()
    conn.close()
    return clingen_variants

# Function to load Delfos variants from the database
def load_delfos_variants_from_db(db_path="db/variants.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT DISTINCT D.CHROM, D.POS, D.REF, D.ALT, D.PHENOTYPE, D.INTERPRETATION
        FROM Delfos_Data D
        WHERE D.PHENOTYPE LIKE "%MONOGENIC DIABETES%"
    ''')

    delfos_variants = cursor.fetchall()
    conn.close()
    return delfos_variants

# Compare variants and keep both interpretations
def compare_variants(clingen_variants, delfos_variants):
    # Convert to DataFrames
    clingen_df = pd.DataFrame(clingen_variants, columns=['chrom', 'pos', 'ref', 'alt', 'clingen_interpretation', 'expert_panel'])
    delfos_df = pd.DataFrame(delfos_variants, columns=['chrom', 'pos', 'ref', 'alt', 'phenotype', 'delfos_interpretation'])

    # Merge shared variants with both interpretations
    shared_df = pd.merge(
        clingen_df[['chrom', 'pos', 'ref', 'alt', 'clingen_interpretation']],
        delfos_df[['chrom', 'pos', 'ref', 'alt', 'delfos_interpretation']],
        on=['chrom', 'pos', 'ref', 'alt'],
        how='inner'
    )

    # Find unique ones
    clingen_keys = clingen_df[['chrom', 'pos', 'ref', 'alt']].apply(tuple, axis=1)
    delfos_keys = delfos_df[['chrom', 'pos', 'ref', 'alt']].apply(tuple, axis=1)
    shared_keys = shared_df[['chrom', 'pos', 'ref', 'alt']].apply(tuple, axis=1)

    unique_clingen_df = clingen_df[~clingen_keys.isin(shared_keys)]
    unique_delfos_df = delfos_df[~delfos_keys.isin(shared_keys)]

    return shared_df, unique_clingen_df, unique_delfos_df

# Save results
def save_results(shared_df, unique_clingen_df, unique_delfos_df):
    shared_df.to_csv("results/shared_variants.csv", index=False)
    unique_clingen_df.to_csv("results/unique_clingen.csv", index=False)
    unique_delfos_df.to_csv("results/unique_delfos.csv", index=False)


# Load from DB
clingen_variants = load_clingen_variants_from_db("db/variants.db")
delfos_variants = load_delfos_variants_from_db("db/variants.db")

# Compare
shared_df, unique_clingen_df, unique_delfos_df = compare_variants(clingen_variants, delfos_variants)

# Save
save_results(shared_df, unique_clingen_df, unique_delfos_df)

# Summary
print(f"✅ Shared variants: {len(shared_df)}")
print(f"🧬 Unique ClinGen variants: {len(unique_clingen_df)}")
print(f"🧬 Unique Delfos variants: {len(unique_delfos_df)}")
