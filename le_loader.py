"""
##########################################################################################
# Author: Mark Antiw Acquaisie                                                           #
# Description:                                                                           #
# This script is designed to loadd data to Google BigQuery as part of ETL. It sets up the#
# environment, creates a new dataset, and defines tables within that dataset. The script #
# also  provides functionality to export data to BigQuery and defines primary and foreign#
# keys for the tables. The main goal is to structure and manage data related to          #
# life expectancy in a BigQuery data warehouse.                                          #
##########################################################################################
"""



import os
from google.cloud import bigquery
from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/markantwi2022/finalproject-38931-240c77bb1878.json"

# Construct a BigQuery client object.
client = bigquery.Client()

# Specify your dataset ID
dataset_id = "{}.LE_DATA_WAREHOUSE".format(client.project)

# Construct a full Dataset object to send to the API.
dataset = bigquery.Dataset(dataset_id)

# Specify the geographic location where the dataset should reside.
#dataset.location = "US"

# Check if the dataset exists
try:
    client.get_dataset(dataset_id)  # Make an API request.
    print("Dataset {} already exists.".format(dataset_id))
    
    # Delete dataset if it exists
    client.delete_dataset(
        dataset_id, delete_contents=True, not_found_ok=True
    )  # Make an API request.
    print("Deleted dataset '{}'.".format(dataset_id))
except:
    print("Dataset {} does not exist.".format(dataset_id))

# Create a new dataset
dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

# Queries to create tables
queries = [
    """
    CREATE TABLE `{}.LE_DATA_WAREHOUSE.COUNTRY_DIM` 
    (country_id INT64, country_code STRING, country_name STRING, region STRING)
    """.format(client.project),
    """
    CREATE TABLE `{}.LE_DATA_WAREHOUSE.DATE_DIM` 
    (year INT64, leap_year BOOL, decade INT64)
    """.format(client.project),
    """
    CREATE TABLE `{}.LE_DATA_WAREHOUSE.INCOME_GROUP_DIM` 
    (income_group_id INT64, income_group_code STRING, income_group STRING)
    """.format(client.project),
    """
    CREATE TABLE `{}.LE_DATA_WAREHOUSE.COUNTRY_STATUS_DIM` 
    (country_status_id INT64, status STRING)
    """.format(client.project),
    """
    CREATE TABLE `{}.LE_DATA_WAREHOUSE.LE_FACT_TABLE` 
    (le_fact_table_id INT64, country_id INT64, income_group_id INT64, country_status_id INT64, year INT64, 
    life_expectancy FLOAT64, adult_mortality FLOAT64, infant_deaths INT64, alcohol FLOAT64, percentage_expenditure FLOAT64, 
    hepatitis_b FLOAT64, measles INT64, bmi FLOAT64, under_five_deaths INT64, polio FLOAT64, total_expenditure FLOAT64, 
    diphtheria FLOAT64, HIV_AIDS FLOAT64, GDP FLOAT64, thinness_10_19_years FLOAT64, 
    thinness_5_9_years FLOAT64, income_composition_of_resources FLOAT64, schooling FLOAT64, education_expenditure FLOAT64)
    """.format(client.project),
      #

]  # as defined above

for query in queries:
    # Start the query, passing in the extra configuration.
    query_job = client.query(query)  # Make an API request.
    
    # Wait for the job to complete.
    query_job.result()
    print("Query completed")


@data_exporter
def export_data_to_big_query(data, **kwargs) -> None:
    """
    Template for exporting data to a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery

    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    for key, value in data.items():
        table_id = '{}.LE_DATA_WAREHOUSE.{}'.format(client.project, key)
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            DataFrame(value),
            table_id,
            #if_exists='fail',  # Specify resolution policy if table name already exists
        )


    queries2 = [
        """
        ALTER TABLE `{}.LE_DATA_WAREHOUSE.COUNTRY_DIM` 
        ADD PRIMARY KEY (country_id) NOT ENFORCED;
        """.format(client.project),
        """
        ALTER TABLE `{}.LE_DATA_WAREHOUSE.DATE_DIM` 
        ADD PRIMARY KEY (year) NOT ENFORCED;
        """.format(client.project),
        """
        ALTER TABLE `{}.LE_DATA_WAREHOUSE.INCOME_GROUP_DIM` 
        ADD PRIMARY KEY (income_group_id) NOT ENFORCED;
        """.format(client.project),
        """
        ALTER TABLE `{}.LE_DATA_WAREHOUSE.COUNTRY_STATUS_DIM` 
        ADD PRIMARY KEY (country_status_id) NOT ENFORCED;
        """.format(client.project),
        """
        ALTER TABLE `{}.LE_DATA_WAREHOUSE.LE_FACT_TABLE` 
        ADD PRIMARY KEY (le_fact_table_id) NOT ENFORCED;
        """.format(client.project),
        """
        ALTER TABLE `{}.LE_DATA_WAREHOUSE.LE_FACT_TABLE` 
        ADD FOREIGN KEY (country_id) REFERENCES `{}.LE_DATA_WAREHOUSE.COUNTRY_DIM`(country_id) NOT ENFORCED,
        ADD FOREIGN KEY (income_group_id) REFERENCES `{}.LE_DATA_WAREHOUSE.INCOME_GROUP_DIM`(income_group_id) NOT ENFORCED,
        ADD FOREIGN KEY (country_status_id) REFERENCES `{}.LE_DATA_WAREHOUSE.COUNTRY_STATUS_DIM`(country_status_id) NOT ENFORCED,
        ADD FOREIGN KEY (year) REFERENCES `{}.LE_DATA_WAREHOUSE.DATE_DIM`(year) NOT ENFORCED;
        """.format(client.project, client.project, client.project, client.project, client.project),
        #

    ] 




    for query in queries2:
        # Start the query, passing in the extra configuration.
        query_job = client.query(query)  # Make an API request.
        
        # Wait for the job to complete.
        query_job.result()
        print("Query completed")
