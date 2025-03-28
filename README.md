# 🧬 DGS Final Project – Monogenic Diabetes Variant Analysis

This project evaluates the clinical utility of the DELFOS platform by comparing its ability to identify Monogenic Diabetes-related genetic variants against ClinGen, the current gold standard.

The project is divided into two main parts:
1. **Knowledge Base Integration** using Hermes, Ulises, Delfos, and Sibila.
2. **Variant Comparison** using SQL-based evaluation of ClinGen vs DELFOS data.

---

## 📁 Project Structure

```
DGS_FINAL_PROJECT/
│
├── data/                         # Input/output data files
│   ├── hermes_raw_variants.csv
│   ├── ulises_filtered_variants.csv
│   ├── monogenic_variants.vcf
│   ├── VCF_clingen_GRCh38.vcf
│   └── patient_vcf_file.vcf
│
├── scripts/                      # All project scripts
│   ├── hermes_fetch.py
│   ├── ulises_filter.py
│   ├── ulises_to_vcf.py          # Provided by instructors
│   ├── delfos_db_insert.py
│   ├── compare_vcfs.py
│   └── sibila_visualization.py
│
├── db/                           # Database-related files
│   ├── delfos_schema.sql
│   └── delfos_data.sqlite
│
├── results/                      # Generated results and plots
│   ├── comparison_summary.csv
│   ├── statistics_report.csv
│   └── sibila_graph.png
│
├── reports/                      # Final documentation
│   ├── final_report.pdf
│   └── presentation_slides.pdf
│
├── docker-compose.yaml
├── LICENSE
├── TODO.md
├── README.md
└── .gitignore
```


## 🚀 How to Run the Project

```bash
# 1. Setup Database
sqlite3 db/delfos_data.sqlite < db/delfos_schema.sql

# 2. Hermes – Variant Collection
python scripts/hermes_fetch.py
# (Alternatively, manually place hermes_raw_variants.csv in the data/ directory)

# 3. Ulises – Clinical Filtering
python scripts/ulises_filter.py

# Then convert to VCF format
python scripts/ulises_to_vcf.py

# 4. Delfos – Insert into SQL Database
python scripts/delfos_db_insert.py

# 5. Sibila – Visualizations
python scripts/sibila_visualization.py

# 6. Comparison: DELFOS vs ClinGen
python scripts/compare_vcfs.py
```

## 👥 Authors

- **Marcin Grzelak**  
  📧 [mgrzela@upv.edu.es](mailto:mgrzela@upv.edu.es)

- **Zuzanna Pająk**  
  📧 [zpajak@upv.edu.es](mailto:zpajak@upv.edu.es)
