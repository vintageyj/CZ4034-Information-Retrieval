# CZ4034-Information-Retrieval

Current stage:
  1. Ran Pretrained Model from pyabsa: https://github.com/yangheng95/PyABSA
  2. Used both AspectTermExtractionPolarityClassification (ATEPC) model and AspectPolarityClassification (APC) model
  3. As mentioned in meeting, APC model is bad, global sentiments predicted not good
  4. Only use results from ATEPC model - final aggregated sentiments
  5. In the CSVs uploaded, use company_atepc_result_filtered or company_atepc_apc_result_filtered
  6. Xlxs versions have pivottables that show model accuracy
