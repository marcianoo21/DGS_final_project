# 🧬 DGS Final Project 
# – Monogenic Diabetes Variant Analysis

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
│
├── results/                      # Generated results and plots
│   └── hermes/
│       ├── hermes_data.json
│       └── relevant_genes.json
│
├── reports/                      # Final documentation pdf
│
├── docker-compose.yaml
├── LICENSE
├── TODO.md
├── README.md
└── .gitignore
```


## 🚀 How to Run the Project
// TODO: Add instructions on how to run the project


## 🧾 Technical Documentation
The final technical document must be written in scientific-article style and include the following sections:

### A. Introduction

- Background on Monogenic Diabetes and its relevance in genomic medicine.
- The importance of accurate genetic variant interpretation for clinical decision-making.
- Motivation for comparing the DELFOS platform with the ClinGen gold standard to assess clinical utility.

### B. Project Part I Results

- **Hermes:**  
  Overview of the methodology used to gather genetic variants related to Monogenic Diabetes using the Hermes module.  
  This involved retrieving all relevant variant data needed to enrich the Delfos knowledge base, enabling meaningful interpretation of patient-specific variants.

- **Ulises:**  
  Summary of the clinically relevant variants identified using the Ulises module.  
  These variants were filtered for clinical significance to ensure relevance for diagnosis and treatment decisions in Monogenic Diabetes.

- **Sibila:**  
  Visual insights generated using Sibila, focusing on relationships between variants and associated clinical features.  
  These visualizations supported interpretation by illustrating genotype–phenotype correlations, helping to validate the relevance of identified variants.


## 👨🏻‍🏫 Presentation
Click [here](https://www.canva.com/design/DAGjSsQyAbA/1Lu7jkZztlKkHk9UyDtXvA/edit?utm_content=DAGjSsQyAbA&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) to access the presentation.


## 👥 Authors

- **Marcin Grzelak**  
  📧 [mgrzela@upv.edu.es](mailto:mgrzela@upv.edu.es)

- **Zuzanna Pająk**  
  📧 [zpajak@upv.edu.es](mailto:zpajak@upv.edu.es)
