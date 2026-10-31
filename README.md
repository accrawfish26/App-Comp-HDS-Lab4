# Lab 4
## What is the purpose?
The repository uses a cohort dataset from the TCGA Lung Adenocarcinoma PanCancer Atlas study (566 patients) to ensure reproducibility of the feature table, along with additional SQL-based query scripts. 

## Accessing the Database & Reproduce Features Table Script
1. Cloning the repository

```
git clone https://github.com/accrawfish26/App-Comp-HDS-Lab4.git
```
2. Set the working directory to the repository root
3. Open Conda to open the `environment.yml` file
4. The Scripts/feature_table.py should run with the expected packages 
```shell
#Presumes an available Python interpreter set on the computer for python3

conda env create -f environment.yml
conda activate Lab4
python3 Scripts/feature_table.py
```
5. The feature table produced would be saved in `Results/feature_table.tsv`

## Running SQL Queries 
**Note: Another place to view these information is `Scripts/query1.sql` & `Scripts/query2.sql` file.**

**Set Up**

1. Initial download of Pandas with SQLite3 was done in the data file of the repository (contains the `cohort.db`
2. Call upon the `cohort.db` by using SQLITE3
3. You should expect 4 tables when you run `.tables`: `genes`, `mutations`, `patients`, and `samples`.
```shell
#An indication sqlite3 loaded is if sqlite> appears at the start of the command line
#An indicator sqlite 3 loaded in cohort.db is using .tables to see 4 tables
.table

pip install pandas
sqlite3 cohort.db
```
### Outcome from SQL Queries

**Schemas**
To view contents within a table, use `.schema`

1. Here is one example from patients: `.schema patients`
2. Note: look for which column found in patients is the primary key
```sql
-- output obtained:
-- CREATE TABLE patients (patient_id TEXT PRIMARY KEY, sex TEXT, age_at_diagnosis REAL, stage TEXT, vital_status TEXT, followup_months REAL);

.schema patients
```

**Row Sums**
To sum the row count within a table, use `COUNT(*)`
Here is one example to sum rows as patient count: 566 as output
```sql
-- output obtained: 566

SELECT COUNT(*) FROM patients;
```

**Primary and Foreign Keys** 
Part 1 on `.schema` can help find areas of joins between tables with the below summarized primary and foreign keys:

|  Keys | Patinets | Samples | Mutations | Genes |
|-------|---------|---------|-----------|-------|
| Primary Key | patient_id | sample_id | mutation_id | gene_symbol |
| Foreign Key | NA | patient_id | sample_id & gene_symbol | NA |

> If you want to join from genes to patients table, one must use its foreign key to > create ties to their respective primary key:  
> gene gene_symbol -> mutation gene_symbol, sample_id -> sample sample_id patient_id -> patients patient_id  

**Grain of data**
Grain is the topic of the rows within a table. For example:
1. Table Patients: one row is one patient
2. Table Samples: one row is one tumor sample from one patient
3. Table Mutations: one row is one mutation in one gene in one sample
4. Table Genes: one row is one gene from one sample

**Schemas, Keys, & Grains**

The primary keys are often the `_id` fields in each table that define each row of data. This helps define the grain's topic for the row. For each additional detail held, foreign keys can help indicate that the gene is related to a sample belonging to a patient, for example. The idea of a one-to-many foreign key is that it allows mutations to connect both `gene_symbols` and `sample_id` to tie two separate tables. But for one-to-one, there is only one point of connection: the patients table with its `patient_id`, which can be referenced by the foreign key in the samples table. 

### Query Questions
View the `Scripts/` folder to see the query scripts that correspond to the tasks below that show how SQL can be utilized from previous concepts:

**Query 1:** Per patient and per gene (TP53, KRAS, EGFR, STK11, KEAP1), the count of protein-altering mutations, with Silent excluded. Join through samples to reach patients.

Findings showed that the row count was 566. After running the script, 566 patients were still included! The addition of silent excluded ensures that only protein-altering mutations are counted, as mutations that do not change the protein would otherwise be included.

The before/after row output ended up listing all 566 patients with the `patient_id`. This was expected, as changes were made to the genes, not the patients, which were left alone as the grain for the table.

**Query 2:** patient per tissue source site per tumor stage. Count each patient once, and keep patients whose stage is missing (don't let them vanish from the result).

I ran a query to see how many data points were missing for the tumor stage and found that 54 were missing (512 total - 566 possible patients = 54 without tumor stage). I would expect the output from running query 2 to show either 512 or 566, depending on how it handles missing data (running `SELECT DISTINCT stage` acknowledges blanks as a data point).

When I ran the query, I got 142 rows. This was concerning at first, until I realized that this represents 142 sites from which tumor tissue was sourced. Adding the values representing the number of patients yields a sum of 566, suggesting no patients were lost. As for where those 54 with no data went, it was found to be stored in the rows shown below:

St Joseph's Medical Center (MD)| |1
Washington University - Cleveland Clinic| |1
Washington University| |52

This would help confirm that no patient data was dropped when querying certain sites and stages of tissue progression.

## Last Comments

### Feature Table (acknowledging missing data)

Notes about how gaps were handled in terms of sex, age at diagnosis, count for gene mutations, and stages of tumor tissue were listed in inline comments in the `/Scripts/feature_table.py`. But in brief, there were many gaps across all variables. But it was found that the Pandas package treats these as `NaN` floats, and after merging the patient and gene tables, we used `na_rep="NA"` to fill these missing values with NA. Additionally, the 0 found under each gene column indicates a count of 0 for that column, not missing data. 

Clarification on metadata:

| Table | Columns | Meaning | Unit if Apply |
|-------|---------|---------|
| patients | patient_id | patient "barcode" | |
| patients | sex | Sex listed for patient | |
| patients | age_at_diagnosis | patient age at tumor diagnosis | year |
| patients | stage | Stage tumor | |
| sources | tissue_source_site | Where tumor sample sourced from | |
| sources | tumor_mutation_burden | mutations per megabase |
| mutations | TP53 | Count of protein-altering mutations in TP53 | count |
| mutations | KRAS | Count of protein-altering mutations in KRAS | count |
| mutations | EGFR | Count of protein-altering mutations in EGFR | count |
| mutations | STK11 | Count of protein-altering mutations in STK11 | count |
| mutations | KEAP1 | Count of protein-altering mutations in KEAP1 | count |


Columns: Patients (patient demographics & id) 

### git.ignore

The file was set as the default for Python, but was changed to allow for `.tsv` files for the `feature_table.tsv` and prevent the commit of the `cohort.db` file.

### AI_Usage

Honest usage of AI and related interactions were documented here. The assistant helped me find new SQL commands to complete the task I desired (CROSS JOIN & UNION ALL) and helped me discover that I can use `na_rep="NA". There was no AI use when it came to writing my own interpretations and in-program comments left in scripts, outside of Grammarly, to support minor writing suggestions. 
