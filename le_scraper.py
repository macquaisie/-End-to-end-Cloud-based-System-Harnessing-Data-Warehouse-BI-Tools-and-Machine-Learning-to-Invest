"""
##########################################################################################
# Author: Mark Antwi Acquaisie                                                           #
# Description:                                                                           #
# This script automates the process of downloading datasets related to life expectancy   #
# from various sources, including the World Bank and Kaggle. It handles the downloading, #
# extraction, renaming, and cleaning of datasets. The cleaned datasets are then uploaded #
# to a Google Cloud Storage bucket for further use. The script leverages various         #
# libraries and tools, including regular expressions for file renaming, the Google Cloud #
# Storage API for uploading, and subprocess for running shell commands.                  #
##########################################################################################
"""



import os
import zipfile
from urllib.request import urlretrieve
from google.cloud import storage
import subprocess
import re

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/markantwi2022/finalproject-38931-240c77bb1878.json'

# The URL where the file is
url = "https://api.worldbank.org/v2/en/indicator/SE.XPD.TOTL.GD.ZS?downloadformat=csv"

# The local filename where you want to store the file
filename = "data.zip"

# Download the file from `url` and save it locally under `filename`
urlretrieve(url, filename)

# Define the folder name where you want to save the files
folder_name = 'le'

# If the folder doesn't exist, create it
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Create a ZipFile Object and load file in it
with zipfile.ZipFile(filename, 'r') as zip_ref:
    # Extract all the contents of zip file in 'le' directory
    zip_ref.extractall(folder_name)

kaggle_api=['kaggle', 'datasets', 'download', '-d', 'kumarajarshi/life-expectancy-who']

unzip=['unzip', 'life-expectancy-who.zip', '-d', 'le/']

subprocess.run(kaggle_api)
subprocess.run(unzip)

# Delete the zip file after extraction
os.remove(filename)

def get_new_name(filename):
    # Pattern to rename: API_SE.XPD.TOTL.GD.ZS_DS2_en_csv_v2_<7 digits>.csv
    if re.match(r'API_SE\.XPD\.TOTL\.GD\.ZS_DS2_en_csv_v2_\d{7}\.csv', filename):
        return "api_educationexpenditure.csv"
    elif re.match(r'Metadata_Country_API_SE\.XPD\.TOTL\.GD\.ZS_DS2_en_csv_v2_\d{7}\.csv', filename):
        return "metadata_2.csv"
    elif re.match(r'Metadata_Indicator_API_SE\.XPD\.TOTL\.GD\.ZS_DS2_en_csv_v2_\d{7}\.csv', filename):
        return "not_useful.csv"
    elif filename == "Life Expectancy Data.csv":
        return "life_expectancy_data.csv"
    return filename

# Get list of files in the directory
files_in_directory = os.listdir(folder_name)
renamed_files = []

# Rename files based on the pattern
for old_name in files_in_directory:
    new_name = get_new_name(old_name)
    if new_name != old_name:
        old_path = os.path.join(folder_name, old_name)
        new_path = os.path.join(folder_name, new_name)
        os.rename(old_path, new_path)
        renamed_files.append(new_name)

with open('/home/markantwi2022/le/api_educationexpenditure.csv', 'r') as fin:
    data = fin.read().splitlines(True)

with open('/home/markantwi2022/le/api_educationexpenditure.csv', 'w') as fout:
    fout.writelines(data[4:])

# Create a storage client
storage_client = storage.Client()

# Replace 'your-bucket' with your Bucket name
bucket_name = 'le_data_bucket'
bucket = storage_client.get_bucket(bucket_name)

# Upload all renamed csv files to GCS
for csv_file in renamed_files:
    blob = bucket.blob(csv_file)
    blob.upload_from_filename(os.path.join(folder_name, csv_file))
    blob.make_public()

#    print(f'{csv_file} uploaded to {bucket_name}.')

# Optional: Delete the local CSV files after uploading to GCS
for csv_file in renamed_files:
    os.remove(os.path.join(folder_name, csv_file))
