# Lab 4

## Opening Database

### Clinical Database

**1. Put your terminal directory to the data folder from the cloned repro**

**2. Run SQL to open the `cohort.db`**

	2a. `SQLite 3 cohort.db`

**3. Test it worked by using `.tables` to view the expected headers of genes mutations patients samples.**

## Schema Understanding (10)

**1. Check what contents within the table with schema**

1a. .schema patients, .schema samples, .schema mutations, .schema genes

**2. Sum count of data entries of patients (all = 566 rows)**

2a. SELECT COUNT(\*) FROM patients, SELECT COUNT(\*) FROM samples, SELECT COUNT(\*) mutations, SELECT COUNT(\*) FROM genes

**3. List every table with its column, primary key and foreign keys**

3a. Patients: patient\_id (text) primary Key! Sex (text), age\_at\_diagnosis (real), stage (text), vital\_status (text), followup\_months (real)

3b. Samples: sample\_id (text) primary key! *patients(patient\_id)* (text), tissue\_source\_site (text), tmb\_nonsynonymous (real), aneuploidy\_score (reall), msi\_mantis\_score (real)

3c. Mutations: mutation\_id (text) primary key! *samples(sample\_id)* (text), *genes(gene\_symbol)* (text), variant\_classification (text), variant\_type (text), protein\_change (text), chromosome (text), start\_pos (integer), end\_pos (integer), t\_ref\_count (integer), t\_alt\_count (integer)

3d.Genes: gene\_symbol (text) primary key! entrez\_gene\_id (integer), chromosome (text),

**4. State the grain of each table in one sentence**

4a. Patients: one row as one patients.

4b. Samples: one row is one tumor sample from one patient.

4c. Mutations: one row is one mutation in one gene in one sample7d.

4d. Genes: one row is one gene from sample

**5. Describe how the tables relate in your own words, or with a simple diagram, based on what you checked in the database, not guessed from the column names.**

5a. The primary key are often the `_id` from each respective table. For the muations table, they had one-to-many foreign keys where it used samples and genes table to produce the columns `sample_id` and `gene_symbol`. In a similar manner, the sample table had a one-to-one foreign keys that used the patients table to create its `pateint_id` column. These were the key table relations I noticed when cchecking the database with `.schema`.

## SQL correctness (25)

Query 1: per patient and per gene (TP53, KRAS, EGFR, STK11, KEAP1), the count of protein-altering mutations, with Silent excluded. Join through samples to reach patients.

Note: Put filters on optional side of LEFT JOIN in ON (NOT WHERE)
Note: Save the script as a `.sql` file or labeled in script

```sql
--- Table & columns: patient, sample & mutation tables (sample_id, gene_symbol, variant_classification)
--- Join through samples: LEFT JOIN in mutations ON samples
--- mutations = m, patient = p, samples = s, genes = g.

SELECT p.patient_id, COUNT(m.protein_change) AS N_protein_chamge
FROM patients p LEFT JOIN samples s ON s.patient_id = p.patient_id
LEFT JOIN mutations m ON m.sample_id = s.sample_id
AND m.gene_symbol IN ('TP53', 'KRAS','EGFR', 'STK11', 'KEAP1')
AND m.variant_classification IS NOT 'Silent'
GROUP BY p.patient_id;
```

Row count expected: 566
Row count got:566

Differs why: There was no difference, as the output listed all 566 patient_id with corresponding counts in protein changes. Double check needs to be done for all datapoints that resulted in 0 counts to ensure gaps are not influencing these outcomes.

Query 2: patient per tissue source site per tumor stage. Count each patient once, and keep patients whose stage is missing (don't let them vanish from the result).

```
# table patients (stage, patient_id) & samples (tissue_source_site)

SELECT p.patient_id FROM patients p LEFT JOIN samples s ON s.patient_id = p.patient_id AND stage IN ('IV', 'IB', 'IIIA', 'IA', 'IIIB', 'IIB', 'IIA', ' ', 'II', 'I') GROUP BY p.patient_id;
```

Note: Put filters on optional side of LEFT JOIN in ON (NOT WHERE)
Note: Save the script as a `.sql` file or labeled in script

Row count expected: Since the grain (or subject of rows) is primarily focus on tissue cource site per tour stage, I could expect at least 512 rows. This comes from 512 rows in column `stages`. This was seen from doing `SELECT COUNT(stage) FROM patients;`.

Row count got: 142 as the total row count, with the sum of values stored as 566.

```
SELECT COUNT(*) FROM (SELECT s.tissue_source_site, p.stage, COUNT(DISTINCT
p.patient_id) AS N_patients_sites FROM patients p LEFT JOIN samples s ON s.patient_
id = p.patient_id GROUP BY s.tissue_source_site, p.stage);
```

Differs why: Each grain was a site containing how many patients had the tumor stage. The sum across all 142 rows was 566, meaning no patients were lost from the sql script. However, this does incorporate those 52 patients without stage data that was identified from row expected. These were stored as " " where I found them in the output as bellow:

St Joseph's Medical Center (MD)| |1
Washington University - Cleveland Clinic| |1
Washington University| |52

This would help show that no patient data was dropped, and did account for those with missing data at certain sites for stage of tissue progression.

## Feature Table Construction (25)

Create a table of 566 rows per patient and verify this count.

Table should include the columns of sex, age at diagnosis, stage, tissue source site, tumor mutation burden, and one count column per gene.


This was done through SQL style coding within a Python environment for pivoting purposes with the Pandas package. 

The table needs to be saved as a TSV file that in the results

```
# Command to rebuild the table from cohort.db from the READ.me file

```