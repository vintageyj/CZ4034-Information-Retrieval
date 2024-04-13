# CZ4034-Information-Retrieval

Current stage:
  1. Ran Pretrained Model from pyabsa: https://github.com/yangheng95/PyABSA
  2. Used both AspectTermExtractionPolarityClassification (ATEPC) model and AspectPolarityClassification (APC) model
  3. As mentioned in meeting, APC model is bad, global sentiments predicted not good
  4. Only use results from ATEPC model - final aggregated sentiments
  5. In the CSVs uploaded, use company_atepc_result_filtered or company_atepc_apc_result_filtered
  6. Xlxs versions have pivottables that show model accuracy
  

final:
1. final_data:

raw_evaluation_data.csv - 1596 reviews randomly selected to be annotated/labelled for evaluation dataset

evaluation_data_raw_601_to_end_checked.csv and evaluation_data_raw_all_checked.csv - show the manual labelleing and checking of the reviews in the evaluation dataset

evaluation_data_labeled.csv - the final evaluation dataset of 1596 reviews manually labelled

2. final_codes:

sentimental-analysis-on-eval-data.ipynb - the codes used to perform ABSA, VADER on the evaluation dataset
*Note the path to the evaluation dataset has to be changed accordingly

sentimental-analysis-on-full-data.ipynb - the codes used to perform ABSA, VADER on the full dataset
*Note the path to the full dataset has to be changed accordingly

3. final_results:

eval_results_distilbert_finetuned_atepc_vader.csv - the automatic classification results of the evaluation dataset resulting from sentimental-analysis-on-eval-data.ipynb

full_results_distilbert_finetuned_atepc_vader.csv - the automatic classification results of the full dataset resulting from sentimental-analysis-on-full-data.ipynb
