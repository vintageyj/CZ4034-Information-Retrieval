# CZ4034-Information-Retrieval

Process:
  1. Manual labelling of Evaluation Dataset
  2. Fine-tuning of DistilBERT model
  3. Automatic classification results from DistilBERT model on both the Evaluation Dataset and Full Dataset
     	- need to pip install torch and transformers
  4. Automatic classification results from ABSA and VADER model on both the Evaluation Dataset and Full Dataset
     	- Ran Pretrained Model from pyabsa: https://github.com/yangheng95/PyABSA, and Pretrained Model from VADER
     	- need to pip install pyabsa and nltk

**Final Structure**

**1. Final Data folder:**

_evaluation_data_raw.csv_ - 1,596 reviews randomly selected to be annotated/labelled for evaluation dataset

_evaluation_data_raw_601_to_end_checked.csv_ and _evaluation_data_raw_all_checked.csv_ - the manual labelling and checking of the reviews in the evaluation dataset

_evaluation_data_raw_final.csv_ - the final evaluation dataset of 1,596 reviews after manually labelling, has an extra column 'Sentiment' which is the labels

_kaggle_TRAIN_balanced_final_36000.csv_ - the training data used to obtain our finetuned DistilBERT model, contains 36,000 reviews with an equal split of Positive and Negative polarities

**2. Final Codes folder:**

_BERT (distilbert) finetuning.ipynb_ - the code used to fine-tune the DistilBERT model to our purposes, and obtain classification results on both the evaluation and full datasets
- classification results from DistilBERT model were appended to evaluation_data_raw_final.csv and final_sg_companies_reviews_clean_UID.csv (final_sg_companies_reviews_clean_UID.csv is under the parent data folder)
- output: validation_results.csv and glassdoor_data_distilbert_finetuned.csv

_sentimental-analysis-on-eval-data.ipynb_ - the code used to perform ABSA, VADER on the evaluation dataset which had the classification results from DistilBERT model, validation_results.csv
- classification results from ABSA, VADER were appended to validation_results.csv
- output: eval_results_distilbert_finetuned_atepc_vader.csv

_sentimental-analysis-on-full-data.ipynb_ - the code used to perform ABSA, VADER on the full dataset which had the classification results from DistilBERT model, glassdoor_data_distilbert_finetuned.csv
- classification results from ABSA, VADER were appended to glassdoor_data_distilbert_finetuned.csv
- output: full_results_distilbert_finetuned_atepc_vader.csv

**3. Final Results folder:**

_validation_results.csv_ - the automatic classification results of the evaluation dataset from DistilBERT model

_glassdoor_data_distilbert_finetuned.csv_ - the automatic classification results of the full dataset from DistillBERT model

_eval_results_distilbert_finetuned_atepc_vader.csv_ - the automatic classification results of the evaluation dataset resulting from ABSA and VADER

_full_results_distilbert_finetuned_atepc_vader.csv_ - the automatic classification results of the full dataset resulting from ABSA and VADER
