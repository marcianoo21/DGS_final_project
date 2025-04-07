import sqlite3
import pandas as pd

# Function to load ClinGen variants from the database
def load_clingen_variants_from_db(db_path="db/variants.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query variants associated with Monogenic Diabetes from ClinGen table
    cursor.execute('''
        SELECT DISTINCT C.CHROM, C.POS, C.REF, C.ALT, C.EXPERT_PANEL
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

    # Query variants related to Monogenic Diabetes in Delfos table
    cursor.execute('''
        SELECT DISTINCT D.CHROM, D.POS, D.REF, D.ALT, D.PHENOTYPE
        FROM Delfos_Data D
        WHERE D.PHENOTYPE LIKE "%MONOGENIC DIABETES%"
    ''')

    delfos_variants = cursor.fetchall()
    conn.close()

    return delfos_variants

# Function to compare ClinGen and Delfos variants
def compare_variants(clingen_variants, delfos_variants):
    # Convert to DataFrames for easier manipulation
    clingen_df = pd.DataFrame(clingen_variants, columns=['chrom', 'pos', 'ref', 'alt', 'interpretation'])
    delfos_df = pd.DataFrame(delfos_variants, columns=['chrom', 'pos', 'ref', 'alt', 'phenotype'])

    # Merge the two DataFrames on chrom, pos, ref, alt to find common variants
    shared_df = pd.merge(clingen_df, delfos_df, how='inner', on=['chrom', 'pos', 'ref', 'alt'])
    unique_clingen_df = clingen_df[~clingen_df.apply(tuple,1).isin(shared_df.apply(tuple,1))]
    unique_delfos_df = delfos_df[~delfos_df.apply(tuple,1).isin(shared_df.apply(tuple,1))]

    return shared_df, unique_clingen_df, unique_delfos_df

# Save the results as CSV files
def save_results(shared_df, unique_clingen_df, unique_delfos_df):
    shared_df.to_csv("results/shared_variants.csv", index=False)
    unique_clingen_df.to_csv("results/unique_clingen.csv", index=False)
    unique_delfos_df.to_csv("results/unique_delfos.csv", index=False)

def main():
    # Load variants from the database
    clingen_variants = load_clingen_variants_from_db()
    delfos_variants = load_delfos_variants_from_db()
    
    # Compare the variants and generate the result DataFrames
    shared_df, unique_clingen_df, unique_delfos_df = compare_variants(clingen_variants, delfos_variants)

    # Save the results to CSV files
    save_results(shared_df, unique_clingen_df, unique_delfos_df)

    # Print the counts of variants
    print(f"Shared variants: {len(shared_df)}")
    print(f"Unique ClinGen variants: {len(unique_clingen_df)}")
    print(f"Unique Delfos variants: {len(unique_delfos_df)}")

if __name__ == "__main__":
    main()
