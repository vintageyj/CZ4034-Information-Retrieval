# CZ4034-Information-Retrieval

Process:
  1. Manual Labelling of Evaluation Dataset
  2. Training/Finetuning of Distilbert model
  3. Automatic classification results from Distilbert model on both the Evaluation Dataset and Full Dataset
  4. Automatic classification results from ABSA and VADER model on both the Evaluation Dataset and Full Dataset
  	- Ran Pretrained Model from pyabsa: https://github.com/yangheng95/PyABSA, and Pretrained Model from VADER
	- need to pip install pyabsa and nltk

final:
1. Final Data folder:

raw_evaluation_data.csv - 1596 reviews randomly selected to be annotated/labelled for evaluation dataset

evaluation_data_raw_601_to_end_checked.csv and evaluation_data_raw_all_checked.csv - the manual labelling and checking of the reviews in the evaluation dataset

evaluation_data_raw_final.csv - the final evaluation dataset of 1596 reviews after manually labelling, has an extra column 'Sentiment' which is the labels

training-data for bert PLEASE ADD

2. Final Codes folder:

code for distilbert - description PLEASE ADD
- classification results from Distilbert model were appended to evaluation_data_raw_final.csv and final_sg_companies_reviews_clean_UID.csv (final_sg_companies_reviews_clean_UID.csv is under the parent data folder)
- output: validation_results.csv and glassdoor_data_distilbert_finetuned.csv


sentimental-analysis-on-eval-data.ipynb - the codes used to perform ABSA, VADER on the evaluation dataset which had the classification results from Distilbert model, validation_results.csv
- classification results from ABSA, VADER were appended to validation_results.csv
- output: eval_results_distilbert_finetuned_atepc_vader.csv

sentimental-analysis-on-full-data.ipynb - the codes used to perform ABSA, VADER on the full dataset which had the classification results from Distilbert model, glassdoor_data_distilbert_finetuned.csv
- classification results from ABSA, VADER were appended to glassdoor_data_distilbert_finetuned.csv
- output: full_results_distilbert_finetuned_atepc_vader.csv

3. Final Results folder:

validation_results.csv - the automatic classification results of the evaluation dataset from Distilbert model

glassdoor_data_distilbert_finetuned.csv - the automatic classification results of the full dataset from DistillBERT model

eval_results_distilbert_finetuned_atepc_vader.csv - the automatic classification results of the evaluation dataset resulting from ABSA and VADER

full_results_distilbert_finetuned_atepc_vader.csv - the automatic classification results of the full dataset resulting from ABSA and VADER
