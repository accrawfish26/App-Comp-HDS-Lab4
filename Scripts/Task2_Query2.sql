--- table patients (stage, patient_id) & samples (tissue_source_site)

SELECT p.patient_id FROM patients p LEFT JOIN samples s ON s.patient_id = p.patient_id AND stage IN ('IV', 'IB', 'IIIA', 'IA', 'IIIB', 'IIB', 'IIA', ' ', 'II', 'I') GROUP BY p.patient_id;