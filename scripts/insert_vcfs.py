import sqlite3

def insert_variant(cursor, chrom, pos, ref, alt):
    """Insert variant if not exists, return its ID."""
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



def parse_info(info_field):
    info_dict = {}
    for entry in info_field.split(';'):
        if '=' in entry:
            key, value = entry.split('=', 1)
            info_dict[key] = value
    return info_dict


def load_clingen(vcf_path):
    with open(vcf_path, 'r') as file:
        conn = sqlite3.connect("db/variants.db")
        cursor = conn.cursor()

        for line in file:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            chrom, pos, id_, ref, alt, qual, filt, info = parts
            info_dict = parse_info(info)
            print("INFO DICT", info_dict.get('INTERPRETATION'))
            variant_id = insert_variant(cursor, chrom, int(pos), ref, alt)

            cursor.execute('''
                INSERT INTO ClinGen_Data (
                    CHROM, POS, ID, REF, ALT, QUAL, FILTER,
                    INTERPRETATION, MET_CRITERIA, NOT_MET_CRITERIA,
                    EXPERT_PANEL, VARIANT_ID
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                chrom,
                int(pos),
                id_,
                ref,
                alt,
                qual,
                filt,
                info_dict.get('INTERPRETATION'),
                info_dict.get('MET_CRITERIA'),
                info_dict.get('NOT_MET_CRITERIA'),
                info_dict.get('EXPERT_PANEL'),
                variant_id
            ))

        conn.commit()
        conn.close()
        print("✅ ClinGen data inserted.")



def load_delfos(vcf_path):
    with open(vcf_path, 'r') as f:
        conn = sqlite3.connect("db/variants.db")
        cursor = conn.cursor()

        for line in f:
            line = line.strip()
            if line.startswith('##'):
                continue
            if line.startswith('#CHROM'):
                headers = line[1:].split('\t')
                continue
            if not line:
                continue

            fields = line.split('\t')
            record = dict(zip(headers, fields))
            info_fields = dict(item.split('=') for item in record['INFO'].split(';'))

            # Insert variant and get its ID
            variant_id = insert_variant(
                cursor,
                record['CHROM'],
                int(record['POS']),
                record['REF'],
                record['ALT']
            )

            values = (
                record['CHROM'],
                int(record['POS']),
                record['ID'],
                record['REF'],
                record['ALT'],
                record['QUAL'],
                record['FILTER'],
                info_fields.get('PHENOTYPE', ''),
                info_fields.get('INTERPRETATION', ''),
                info_fields.get('INTERPRETATION_REASON', ''),
                info_fields.get('CLINICAL_ACTIONABILITY', ''),
                info_fields.get('GENE', ''),
                variant_id
            )

            cursor.execute('''
                INSERT INTO Delfos_Data (
                    CHROM, POS, ID, REF, ALT, QUAL, FILTER,
                    PHENOTYPE, INTERPRETATION, INTERPRETATION_REASON,
                    CLINICAL_ACTIONABILITY, GENE, VARIANT_ID
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)

        conn.commit()
        conn.close()
        print("✅ Delfos data inserted.")



if __name__ == "__main__":
    load_clingen("data/VCF_clingen.vcf")
    load_delfos("data/VCF_ulises.vcf")
