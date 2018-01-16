import pandas
import glob
import os
import fnmatch
import re

import get_claim_number
import get_paid_amount

documents_file = 'C:\\Users\\anoopshar\\Desktop\\UHC\\sample_docid.csv'
documents = pandas.read_csv(documents_file, ',')['doc_id'].tolist()

filepath = 'C:\\Users\\anoopshar\\Desktop\\UHC\\Samples_Feature_Extraction'

# retrieve all the pages and their paths for a document
def get_all_images(document):
    all_images = []
    for root, dirnames, filenames in os.walk(filepath):
        for filename in fnmatch.filter(filenames, document + '*.tif'):
            all_images.append(os.path.join(root, filename))
    return all_images

def get_all_text(document):
    all_text = ''
    for root, dirnames, filenames in os.walk(filepath):
        for filename in fnmatch.filter(filenames, document + '*.txt'):
            text_file = open(os.path.join(root, filename),'r')
            all_text += text_file.read()
            # all_text += '\n------------------------------------------------------------------------------------\n'
            text_file.close()
            # all_text.append(os.path.join(root, filename))
    return all_text


features_df = pandas.read_csv('C:\\Users\\anoopshar\\Desktop\\UHC\\features.csv', ',')
features_list = pandas.read_csv('C:\\Users\\anoopshar\\Desktop\\UHC\\features.csv', ',')

document_features_list = []
for document in documents:
    for index, row in features_df.iterrows():

        feature_category = row['feature_category']
        feature_name = row['feature_name']
        feature_value = ''

        # --------------------------------------------------------------------- #
        if 'metadata' in feature_category:
            feature_value = 'from metadata'
        # --------------------------------------------------------------------- #



        # --------------------------------------------------------------------- #
        # elif feature_category in ['keywords__form_name', 'keywords__appeal', 'keywords__individual', 'keywords__urgent']:
        elif 'keywords__' in feature_category:
            all_text = get_all_text(document)
            keyword_match = re.search(feature_name, all_text, re.IGNORECASE)
            if keyword_match:
                feature_value = 1
            else:
                feature_value = 0
        # --------------------------------------------------------------------- #



        # --------------------------------------------------------------------- #
        elif feature_category in ['values__claim_number', 'values__paid_amount']:
            if feature_category == 'values__claim_number':
                feature_value = get_claim_number.get_claim_number()
            elif feature_category == 'values__paid_amount':
                feature_value = 'get_paid_amount()'
        # --------------------------------------------------------------------- #


        document_features_list.append([document, feature_category + '__' + feature_name, feature_value])
    break

document_features_df = pandas.DataFrame(data=document_features_list, columns=['document_id', 'feature', 'feature_value'])
document_features_df_pivot = document_features_df.pivot(index='document_id', columns='feature', values='feature_value')
document_features_df_pivot.to_csv('document_features.csv', sep=',')
# print document_features_df_pivot
