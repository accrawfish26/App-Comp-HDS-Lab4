# AI Usage Transparency

## Prompt 1 
**Model:** UseAI Instant

**Error Message:** 
```
sqlite3.OperationalError: unable to open database file
```
**UseAI Instant response:** The path was build from `Path(__file__).resolve().parent`, which pointed at the `Scripts/` folder rather than the repo root, so the database was not where the script looked for it.

**UseAI Instant suggested fix:** Walk up one more level with `.parent.parent` and join the path with pathlib, so it does not depend on where the script is run from.

**My Edit:** I had not realized that I had ended up with an empty `cohort.db` in the wrong folder, which led to programming confusion. Once UseAI Instant pointed out that I was leaving the file, I found the appropriate file and set a parameter so that if the wrong path fails, it will print a "no such table" message using `assert DB.exists ()`. 

=============================================================

## Prompt 2
**Model:** UseAI Instant

**Error Message:** 
```
Parse error: near "AND": syntax error
```
**UseAI Instant response:** The gene filter used m.gene_symbol = 'TP53', 'KRAS', 'EGFR', 'STK11', 'KEAP1', which is not valid SQL — a comma-separated list cannot follow =. The correct operator is IN.

**UseAI Instant suggested fix:** m.gene_symbol IN ('TP53', 'KRAS', 'EGFR', 'STK11', 'KEAP1').

**My Edit:** This was an example of a bit of learning that occurred from time to time when I was frustrated, to realize it was a simple solution. It showed that if I wanted to create a list with SQL, it does not follow the natural lists I would expect with 'text '..., but rather, use `IN` with (list, list), which I ended up using to support the rest of the script writing. 

**UseAI Instant Response:** Extending the `IN` version to the grid meant giving each gene its own group, so the comparison had become `m.gene_symbol = g.gene_symbol` against a five-row gene list. 

**UseAI Instant Suggestion:** Build the gene list with `UNION ALL` and pair it with patients using `CROSS JOIN`.

**My Edit:** I ended up slowly learning how this worked: I had five gene names that needed to be assigned to one patient, and with `CROSS JOIN` I could do that by repeating the patient for each of the genes (5x566 = expected 2830 rows). Previous to the model suggestion, I had done `SELECT('TP53', 'KRAS',...) AS gene_symbol` that does not lead to the 2830 expected rows, as it returns one row containing five columns. 

=============================================================

## Prompt 3
**Model:** UseAI Instant

**Error Message:** 

No visible change after... code below. The blank sex count stayed at 52.
```
feature_table["sex"] = patients["sex"].replace("", pd.NA)
```
**UseAI Instant response:** The fill ran before the merge, and `merge` rebuilds the frame from `pateints`, so the replacement was overwritten.

**UseAI Instant suggested fix:** Move the fill below the merge, operating on `feature_table` itself.

**My Edit:** I realized that flow matters. The `feature_table` at the front only works if it was set chronologically prior to this line (which was not the case). So I simply moved it down. The outcome of 52 was related to the fact that blanks seem to remain even after the attempt to replace them with NA. I had later realize that they are being stored as `"NaN"` and was not sure where that was coming form or why `"NaN"` would not work as `"NaN", pd.NA`

**UseAI Instant response:** `nan == "NaN"` is always false, because `nan` is a float and `"NaN"` is a string, so `replace("NaN", pd.NA)` can never match.

**UseAI Instant suggested fix:** Drop the line; use `na_rep="NA"` in `to_csv` instead, since the blank fields in the TSV were a writing-format default, not a missing-data problem.

**My edit:** I ended up removing the original attempts to fill in missing data once this was made clear to me, and I added `na_rep="NA"` as part of the output step. I had different things overlapping that caused some confusion, along with a gap in knowledge about how Python/pandas handle important data/databases, which I will continue to grow as I gain more exposure.

=============================================================


