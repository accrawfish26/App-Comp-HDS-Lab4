--- Table & columns: patient, sample & mutation tables (sample_id, gene_symbol, variant_classification)
--- Join through samples: LEFT JOIN in mutations ON samples
--- mutations = m, patient = p, samples = s, genes = g.

SELECT p.patient_id, COUNT(m.protein_change) AS N_protein_chamge
FROM patients p LEFT JOIN samples s ON s.patient_id = p.patient_id
LEFT JOIN mutations m ON m.sample_id = s.sample_id
AND m.gene_symbol IN ('TP53', 'KRAS','EGFR', 'STK11', 'KEAP1')
AND m.variant_classification IS NOT 'Silent'
GROUP BY p.patient_id;