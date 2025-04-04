# ✅ TODO – DGS Final Project (Database-Based Approach)

## 🧬 PART I: Knowledge Base Integration for Monogenic Diabetes

### 1. Hermes – Collect All Monogenic Diabetes-Related Variants
- [X] Research Monogenic Diabetes genes (e.g., HNF1A, GCK, etc.)
- [X] Extract related variants from public datasets (ClinVar, OMIM, etc.) using `scripts/HermesScript.R`
- [X] Integrate the data and perdform data preparation.
- [X] Save collected data as `db/hermes_data.json` and `db/relevant_genes.json`
- [ ] Documentation

### 2. Ulises – Identify Clinically Relevant Variants
- [X] Ulises
- [ ] Documentation

### 3. Delfos – Import Data into SQL Database
- [X] Delfos
- [ ] Documentation

### 4. Sibila – Visualize Variant–Phenotype Relationships
- [X] Save visual outputs in `results/`
- [ ] Documentation

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
