##########################################################################################
# Author: Mark Antwi Acquaisie                                                           #
# Description: This code is designed to extract data from multiple URLs and return it as #
#              a dictionary of dictionaries. It also includes a test function to ensure  #
#              the output is correctly formatted.                                        #
##########################################################################################



import io
import pandas as pd
import requests
import json
from pandas import json_normalize

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Load data from multiple URLs and return as a dictionary of dictionaries.
    """
    urls = [
        'https://storage.googleapis.com/le_data_bucket/api_educationexpenditure.csv',
        'https://storage.googleapis.com/le_data_bucket/life_expectancy_data.csv',
        'https://storage.googleapis.com/le_data_bucket/metadata_2.csv',
    ]

    dataframes = {}
    for i, url in enumerate(urls, 1):
        response = requests.get(url)
        df = pd.read_csv(io.StringIO(response.text), sep=',')
        dataframes[f'df_{i}'] = df.to_dict(orient='dict')

    return dataframes

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert isinstance(output, dict), 'The output should be a dictionary'
    for value in output.values():
        assert isinstance(value, dict), 'Each value in the dictionary should be a dictionary'
