import sqlite3

def insert_variant(cursor, chrom, pos, ref, alt):
    """Insert variant if it doesn't already exist. Return variant_id."""
    cursor.execute('''
        SELECT idVariant FROM Variant
        WHERE chr = ? AND pos = ? AND referenceAllele = ? AND altAllele = ?
    ''', (chrom, pos, ref, alt))
    result = cursor.fetchone()

    if result:
        return result[0]
    else:
        cursor.execute('''
            INSERT INTO Variant (chr, pos, referenceAllele, altAllele)
            VALUES (?, ?, ?, ?)
        ''', (chrom, pos, ref, alt))
        return cursor.lastrowid


def load_clingen(vcf_path, db_path="db/variants.db"):
    print("Loading ClinGen VCF...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(vcf_path) as file:
        for line in file:
            if line.startswith("#"):
                continue
            fields = line.strip().split('\t')
            chrom, pos, _, ref, alt, _, _, info = fields[:8]

            significance = "unknown"
            for item in info.split(";"):
                if item.startswith("CLNSIG="):
                    significance = item.split("=")[1].lower()

            variant_id = insert_variant(cursor, chrom, int(pos), ref, alt)

            cursor.execute('''
                INSERT INTO ClinGen_Data (variant_id, clinical_significance)
                VALUES (?, ?)
            ''', (variant_id, significance))

    conn.commit()
    conn.close()
    print("✅ ClinGen data inserted.")


def load_delfos(vcf_path, db_path="db/variants.db"):
    print("Loading Delfos VCF...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(vcf_path) as file:
        for line in file:
            if line.startswith("#"):
                continue
            fields = line.strip().split('\t')
            chrom, pos, _, ref, alt, _, _, info = fields[:8]

            classification = "unknown"
            for item in info.split(";"):
                if item.startswith("STATUS="):
                    classification = item.split("=")[1].lower()

            variant_id = insert_variant(cursor, chrom, int(pos), ref, alt)

            cursor.execute('''
                INSERT INTO Delfos_Data (variant_id, classification)
                VALUES (?, ?)
            ''', (variant_id, classification))

    conn.commit()
    conn.close()
    print("✅ Delfos data inserted.")


if __name__ == "__main__":
    load_clingen("data/VCF_clingen.vcf")
    load_delfos("data/VCF_ulises.vcf")
