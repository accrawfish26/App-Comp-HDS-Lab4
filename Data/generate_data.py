#!/usr/bin/env python3
"""Build cohort.db (Lab 4) from the cBioPortal TCGA LUAD PanCancer Atlas files."""

import sqlite3, pandas as pd
con = sqlite3.connect("cohort.db")
pd.read_sql("SELECT * FROM samples LIMIT 5", con)
