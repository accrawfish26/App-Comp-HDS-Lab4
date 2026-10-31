#Feature Table Construction (Task 3) (25)

#Reshape with SQL & Python to have patient grain data with:
#Sex, age at diagnosis, stage, tissue source site, tumor mutation burden, one count column per gene
#Involved varibales: patient_id, sex, age_at_diagnosis, stage, tissue_source_site, tmb_nonsynonymous, mutation_id/gene_symbol

import sqlite3, pandas as pd
from pathlib import Path

#Help with reproducibility using a cloned repository
REPO = Path(__file__).resolve().parent.parent #repo root
DB = REPO/ "Data/cohort.db"
con = sqlite3.connect(DB)

# Count from a table = 566 patients
print(pd.read_sql("SELECT COUNT(*) FROM patients", con))

# Setting Wide Table on Patients (one row per patient)
patients =  pd.read_sql("SELECT p.patient_id, p.sex, p.age_at_diagnosis, p.stage, s.tissue_source_site, s.tmb_nonsynonymous FROM patients p LEFT JOIN samples s ON s.patient_id = p.patient_id", con)

# Missing Data Check = Found 4 Missing Data in samples. Addressed using "THEN NULL ELSE" for patients without gene mutation data
print(pd.read_sql("SELECT COUNT(*) FROM samples s WHERE NOT EXISTS(SELECT 1 FROM mutations m WHERE m.sample_id = s.sample_id)", con))

# Setting Table on Genes (one row per patient per gene)
# Note: CROSS JOIN is used to help join genes with patient data as 5 row data per patients
# Note: UNION ALL is used to help put the counts of names into rows that joint through the CROSS JOIN to patient table
# Note: Silent mutations of the 5 genes were removed using IS NOT SILENT from the variant_classification
gene = pd.read_sql("SELECT p.patient_id, g.gene_symbol, CASE WHEN NOT EXISTS(SELECT 1 FROM mutations m WHERE m.sample_id = s.sample_id) THEN NULL ELSE COUNT (m.mutation_id) END AS gene_count FROM patients p CROSS JOIN (SELECT 'TP53' AS gene_symbol UNION ALL SELECT 'KRAS' UNION ALL SELECT 'EGFR' UNION ALL SELECT 'STK11' UNION ALL SELECT 'KEAP1') g LEFT JOIN samples s ON s.patient_id = p.patient_id LEFT JOIN mutations m ON m.sample_id = s.sample_id AND m.gene_symbol = g.gene_symbol AND m.variant_classification IS NOT 'Silent' GROUP BY p.patient_id, g.gene_symbol", con)

# Initial varification tables were produced with desired headers
print(patients.head())
print(gene.head())

#Outcome 566 patients table (none data loss)
print(len(patients))
# Outcome of 2830 gene table (5 gene per patient in patients table, no data loss)
print(len(gene))

# Creating the merged Feature Table
# Pivot gene table to have patient grain
wide = (gene.pivot(index="patient_id", columns="gene_symbol", values="gene_count"))

# Outcome of 566 patient rows (No data was lost)
print(len(wide))

# Feature Table with Python (Join wide gene with patient table)
feature_table = patients.merge(wide, on="patient_id",how="left", validate="one_to_one")

#Identify gaps in the Feature Table
#Proof of having missing data in sex variable (nmiss = 52)
print(pd.read_sql("SELECT COUNT(*) FROM patients WHERE sex IS NULL", con))

#Proof of having missing data in stages variable (nmiss= 54)
print(pd.read_sql("SELECT COUNT(*) FROM patients WHERE stage IS NULL", con))

#Proof of having missing data in age_at_diagnosis variable (nmiss= 71)
print(pd.read_sql("SELECT COUNT(*) FROM patients WHERE age_at_diagnosis IS NULL", con))

# Found missing datas were marked as NaN by Pandas package as floats in all 3 variables
# Note: they are dealt with already and used na_rep="NA" during export of file to fill these as NA
print(pd.read_sql("SELECT DISTINCT sex FROM patients",con))
print(pd.read_sql("SELECT DISTINCT stage FROM patients",con))
print(pd.read_sql("SELECT DISTINCT age_at_diagnosis FROM patients",con))

# Verify no patient was lost during the process: 566 rows per patients
print(feature_table.head())
print(len(feature_table))

#Saving table as a TSV file to Results in repo
OUT = REPO/"results"/"feature_table.tsv"
feature_table.to_csv(OUT, sep="\t", index=False, na_rep="NA")
print("file saved at", OUT)