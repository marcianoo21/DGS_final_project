# ✅ TODO – DGS Final Project (Database-Based Approach)

## 🧬 PART I: Knowledge Base Integration for Monogenic Diabetes

### 1. Hermes – Collect All Monogenic Diabetes-Related Variants
- [ ] Research Monogenic Diabetes genes (e.g., HNF1A, GCK, etc.)
- [ ] Extract related variants from public datasets (ClinVar, OMIM, etc.)
- [ ] Save collected data as `data/hermes_raw_variants.csv`
- [ ] (Optional) Create `scripts/hermes_fetch.py` to simulate the collection process

### 2. Ulises – Identify Clinically Relevant Variants
- [ ] Filter Hermes output to retain only pathogenic / likely pathogenic variants
- [ ] Save filtered results to `data/ulises_filtered_variants.csv`
- [ ] Use `ulises_to_vcf.py` to convert to `data/monogenic_variants.vcf`

### 3. Delfos – Import Data into SQL Database
- [ ] Define schema in `db/delfos_schema.sql` (variants, genes, clinical_significance, etc.)
- [ ] Create and populate the SQL database (`delfos_data.sqlite` or PostgreSQL)
- [ ] Import:
  - `monogenic_variants.vcf` (Ulises output)
  - `VCF_clingen_GRCh38.vcf` (ClinGen gold standard)
- [ ] Store both datasets in separate tables (e.g., `delfos_variants`, `clingen_variants`)

### 4. Sibila – Visualize Variant–Phenotype Relationships
- [ ] Query variant-gene-condition relationships from the database
- [ ] Create visualizations using `scripts/sibila_visualization.py`
  - Network graph (e.g., NetworkX)
  - Frequency charts (e.g., Matplotlib/Seaborn)
- [ ] Save visual outputs in `results/`

---

## 🧪 PART II: Evaluation of DELFOS vs ClinGen

### 5. Prepare Data in the Database
- [ ] Ensure consistent format between both variant datasets (coordinate system, alleles)
- [ ] Normalize chromosome names if needed (e.g., `chr1` vs `1`)

### 6. Compare DELFOS and ClinGen Using SQL
- [ ] Implement SQL JOIN queries to:
  - Match by chromosome, position, ref/alt alleles
  - Compare clinical significance
- [ ] Identify matches and mismatches
- [ ] Store comparison results in a `results/comparison_summary.csv`

### 7. Statistical Evaluation
- [ ] Define metrics (e.g., precision, recall, total matches)
- [ ] Use SQL queries or Python analysis to compute stats
- [ ] Summarize in `results/statistics_report.csv`

---

## 📚 DOCUMENTATION & DELIVERY

### 8. Final Report
- [ ] Introduction
- [ ] Part I: Hermes → Ulises → Delfos → Sibila (with diagrams)
- [ ] Part II: SQL comparison logic + results
- [ ] Discussion on discrepancies
- [ ] Clinical utility of DELFOS
- [ ] Future enhancements

### 9. Presentation Slides
- [ ] Overview of each module’s purpose and results
- [ ] Key charts and graphs from Sibila
- [ ] SQL-based comparison insights
- [ ] Suggested improvements

---

## 🧹 Final Cleanup
- [ ] Verify correct file paths and data loading
- [ ] Document all SQL queries
- [ ] Add README with setup instructions
