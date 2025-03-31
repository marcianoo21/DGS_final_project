#### DATA EXTRACTION #### 

#ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/ 
Expression = '"Monogenic Diabetes"[Disease/Phenotype]'
ClinVar = hermes::get_clinvar_data_by_expression(Expression, clean_phenotype = TRUE, keyword = "diabetes")

#GWAS: https://www.ebi.ac.uk/gwas/home 
GWAS = hermes::get_GWAS_data_by_phenotype("diabetes mellitus", FALSE)

#LOVD: https://www.lovd.nl
RelevantGenes <- c(
  "ABCC8", "APPL1", "BLK", "CEL", "EIF2AK3", "GATA6", "GCK",
  "GLIS3", "HNF1A", "HNF1B", "HNF4A", "HYMAI", "INS",
  "KCNJ11", "KLF11", "NARS2", "NEUROD1", "NEUROG3",
  "PAX4", "PDX1", "PLAGL1", "PTF1A", "RFX6", "SH2B1",
  "SLC19A2", "SLC2A2", "STAT3", "WFS1", "ZFP57"
)
LOVD = hermes::get_lovd_data_from_gene_list(RelevantGenes, TRUE, "diabetes")

#### INTEGRATION #### 
Integration= hermes::integrate_datasets(list(ClinVar, GWAS, LOVD))

#### DATA PREPARATION #### 

Hermes = hermes::prepare_data_for_ulises(Integration, FALSE, TRUE)


#### FILES GENERATION ####
HermestoJSON = hermes::to_json(Hermes)

script_dir <- dirname(rstudioapi::getActiveDocumentContext()$path)
results_dir <- file.path(script_dir, "local_results")
if (!dir.exists(results_dir)) dir.create(results_dir, recursive = TRUE)

hermes::write_json(HermestoJSON, file.path(results_dir, "hermes.json"))
jsonlite::write_json(RelevantGenes, file.path(results_dir, "relevant_genes.json"))

