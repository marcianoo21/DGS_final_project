import pandas as pd

# Load delfos and clingen VCF files into DataFrames
delfos_file = "data/VCF_ulises.vcf"
clingen_file = "data/VCF_clingen.vcf"

def parse_vcf(vcf_file):
    # Read VCF file into a DataFrame
    df = pd.read_csv(vcf_file, sep="\t", comment="#")
    return df

# Load data
delfos_df = parse_vcf(delfos_file)
clingen_df = parse_vcf(clingen_file)

# Standardize interpretation labels
def standardize_interpretation(df):
    interpretation_map = {
        'ACCEPTED WITH STRONG EVIDENCE': 'Pathogenic',
        'ACCEPTED WITH MODERATE EVIDENCE': 'Likely Pathogenic',
        'Uncertain Significance': 'Uncertain Significance',
        'Benign': 'Benign',
        'Likely Benign': 'Likely Benign'
    }
    
    df['Standardized_Interpretation'] = df['INTERPRETATION'].map(interpretation_map)
    return df

# Standardize interpretations in both datasets
delfos_df = standardize_interpretation(delfos_df)
clingen_df = standardize_interpretation(clingen_df)

# Merge the two DataFrames based on variant ID or position and chromosome
merged_df = pd.merge(delfos_df[['CHROM', 'POS', 'VARIANT_ID', 'Standardized_Interpretation']],
                     clingen_df[['CHROM', 'POS', 'VARIANT_ID', 'Standardized_Interpretation']],
                     on=['CHROM', 'POS', 'VARIANT_ID'],
                     suffixes=('_delfos', '_clingen'))

# Compare interpretations
merged_df['Interpretation_Conflict'] = merged_df['Standardized_Interpretation_delfos'] != merged_df['Standardized_Interpretation_clingen']

# Display results with conflicts
conflicts_df = merged_df[merged_df['Interpretation_Conflict']]
print(conflicts_df[['CHROM', 'POS', 'VARIANT_ID', 'Standardized_Interpretation_delfos', 'Standardized_Interpretation_clingen']])
