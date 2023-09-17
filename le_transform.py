if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd

@transformer
def transform(data, *args, **kwargs):
    """
    Convert dictionary data back into pandas DataFrame.

    Args:
        data: The output from the upstream parent block (dictionary of dictionaries)
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Dictionary of pandas DataFrames.
    """
    dataframes = {}
    for key, value in data.items():
        dataframes[key] = pd.DataFrame.from_dict(value)

    api_educationexpenditure =dataframes['df_1']
    life_expectancy_data =dataframes['df_2']
    metadata_2 =dataframes['df_3']

    #metadata_2 TRANFORMATION
    metadata_2 = metadata_2.rename(columns={'ï»¿"Country Code"': 'Country Code'})
    
    codes_to_drop = ['AFE', 'AFW', 'ARB', 'CEB', 'CSS', 'EAP', 'EAR', 'EAS', 'ECA', 'ECS', 'EMU', 
           'EUU', 'FCS', 'HIC', 'HPC', 'IBD', 'IBT', 'IDA', 'IDB', 'IDX', 'LAC', 'LCN', 
           'LDC', 'LIC', 'LMC', 'LMY', 'LTE', 'MEA', 'MIC', 'MNA', 'NAC', 'OED', 'OSS', 
           'PRE', 'PSS', 'PST', 'SAS', 'SSA', 'SSF', 'SST', 'TEA', 'TEC', 'TLA', 'TMN', 
           'TSA', 'TSS', 'UMC', 'WLD', 'ASM', 'AND', 'ABW', 'BMU', 'VGB', 'CSS', 'CEB', 
           'CUW', 'EMU', 'PYF', 'GIB', 'GRL', 'GUM', 'HKG', 'IMN', 'XKX', 'LCN', 'LAC', 
           'TLA', 'LDC', 'LIE', 'MAC', 'NCL', 'NAC', 'MNP', 'PRI', 'MAF', 'SXM', 
           'TCA', 'VIR', 'PSE','CYM', 'CHI', 'FRO']

    df_meta_drop = metadata_2[~metadata_2['Country Code'].isin(codes_to_drop)]
    df_meta_drop.drop(['Unnamed: 5'], axis=1, inplace=True)

    # Add a new row using the loc function
    new_rows = pd.DataFrame({
    'Country Code': ['NIU', 'COK'],
    'Region': ['East Asia & Pacific', 'East Asia & Pacific'],
    'IncomeGroup': ['Upper middle income', 'Upper middle income'],
    'SpecialNotes': ['', ''],
    'TableName': ['Niue', 'Cook Islands']
    })

    # Concatenate original DataFrame and new_rows
    df_meta_drop = pd.concat([df_meta_drop, new_rows], ignore_index=True)

    # Replace the name
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'Bahamas, The': 'Bahamas'})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'Bolivia': 'Bolivia (Plurinational State of)'})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'Congo, Rep.': 'Congo'})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'Congo, Dem. Rep.': 'Democratic Republic of the Congo'})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Egypt, Arab Rep.": "Egypt"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'Gambia, The': 'Gambia'})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Iran, Islamic Rep.": "Iran (Islamic Republic of)"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Kyrgyz Republic": "Kyrgyzstan"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'Lao PDR': "Lao People's Democratic Republic"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Micronesia, Fed. Sts.": "Micronesia (Federated States of)"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Korea, Rep.": "Republic of Korea"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Moldova": "Republic of Moldova"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'St. Kitts and Nevis': "Saint Kitts and Nevis"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"St. Lucia": "Saint Lucia"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"St. Vincent and the Grenadines": "Saint Vincent and the Grenadines"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"São Tomé and Principe" : "Sao Tome and Principe"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'Slovak Republic': "Slovakia"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"North Macedonia": "The former Yugoslav republic of Macedonia"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Türkiye": "Turkey"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"CÃ´te d'Ivoire": "Cote d'Ivoire"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"United Kingdom": "United Kingdom of Great Britain and Northern Ireland"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Tanzania": "United Republic of Tanzania"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'United States': "United States of America"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Venezuela, RB": "Venezuela (Bolivarian Republic of)"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Vietnam": "Viet Nam"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({'Yemen, Rep.': "Yemen"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Eswatini": "Swaziland"})
    df_meta_drop['TableName'] = df_meta_drop['TableName'].replace({"Korea, Dem. People's Rep.": "Democratic People's Republic of Korea"})
    df_meta_drop['IncomeGroup'] = df_meta_drop['IncomeGroup'].fillna('Upper middle income')

    #api_educationexpenditure TRANFORMATION
    api_educationexpenditure.drop(['Indicator Name', 'Indicator Code', '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968', '1969', '1970', '1971', '1972', '1973', 
    '1974', '1975', '1976', '1977', '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', '1990', '1991', '1992', 
    '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2016', '2017', '2018', '2019', '2020', '2021', '2022', 'Unnamed: 67'], axis=1, inplace=True)

    id_vars = ['Country Name', 'Country Code']

    # Melt the DataFrame, keeping the id_vars columns unchanged
    melted_df_api = api_educationexpenditure.melt(id_vars=id_vars, var_name='Year', value_name='EducationExpenditure')
    codes_to_drop = ['AFE', 'AFW', 'ARB', 'CEB', 'CSS', 'EAP', 'EAR', 'EAS', 'ECA', 'ECS', 'EMU', 
            'EUU', 'FCS', 'HIC', 'HPC', 'IBD', 'IBT', 'IDA', 'IDB', 'IDX', 'LAC', 'LCN', 
            'LDC', 'LIC', 'LMC', 'LMY', 'LTE', 'MEA', 'MIC', 'MNA', 'NAC', 'OED', 'OSS', 
            'PRE', 'PSS', 'PST', 'SAS', 'SSA', 'SSF', 'SST', 'TEA', 'TEC', 'TLA', 'TMN', 
            'TSA', 'TSS', 'UMC', 'WLD', 'ASM', 'AND', 'ABW', 'BMU', 'VGB', 'CSS', 'CEB', 
            'CUW', 'EMU', 'PYF', 'GIB', 'GRL', 'GUM', 'HKG', 'IMN', 'XKX', 'LCN', 'LAC', 
            'TLA', 'LDC', 'LIE', 'MAC', 'NCL', 'NAC', 'MNP', 'PRI', 'MAF', 'SXM', 
            'TCA', 'VIR', 'PSE','CYM', 'CHI', 'FRO', 'INX']

    melted_df_api = melted_df_api[~melted_df_api['Country Code'].isin(codes_to_drop)]
    # Add a new row using the loc function
    new_rows1 = pd.DataFrame({
        'Country Name': ['Niue'] * 16 + ['Cook Islands'] * 16,
        'Country Code': ['NIU'] * 16 + ['COK'] * 16,
        'Year': [str(year) for year in range(2000, 2016)] * 2,
    })

    # Concat new rows to the DataFrame
    melted_df_api = pd.concat([melted_df_api, new_rows1], ignore_index=True)

    # Replace the name
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'Bahamas, The': 'Bahamas'})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'Bolivia': 'Bolivia (Plurinational State of)'})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'Congo, Rep.': 'Congo'})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'Congo, Dem. Rep.': 'Democratic Republic of the Congo'})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Egypt, Arab Rep.": "Egypt"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'Gambia, The': 'Gambia'})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Iran, Islamic Rep.": "Iran (Islamic Republic of)"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Kyrgyz Republic": "Kyrgyzstan"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'Lao PDR': "Lao People's Democratic Republic"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Micronesia, Fed. Sts.": "Micronesia (Federated States of)"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Korea, Rep.": "Republic of Korea"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Moldova": "Republic of Moldova"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'St. Kitts and Nevis': "Saint Kitts and Nevis"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"St. Lucia": "Saint Lucia"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"St. Vincent and the Grenadines": "Saint Vincent and the Grenadines"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"São Tomé and Principe" : "Sao Tome and Principe"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'Slovak Republic': "Slovakia"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"North Macedonia": "The former Yugoslav republic of Macedonia"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Turkiye": "Turkey"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"United Kingdom": "United Kingdom of Great Britain and Northern Ireland"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Tanzania": "United Republic of Tanzania"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'United States': "United States of America"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Venezuela, RB": "Venezuela (Bolivarian Republic of)"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Vietnam": "Viet Nam"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"CÃ´te d'Ivoire": "Cote d'Ivoire"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({'Yemen, Rep.': "Yemen"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Eswatini": "Swaziland"})
    melted_df_api['Country Name'] = melted_df_api['Country Name'].replace({"Korea, Dem. People's Rep.": "Democratic People's Republic of Korea"})


    # Sort both dataframes by 'Year' in ascending order
    melted_df_api = melted_df_api.sort_values(by='Country Code')
    df_meta_drop = df_meta_drop.sort_values(by='Country Code')

    # Left join melted_df_api's 'CountryCode' column to df_meta_drop
    melted_api_meta = melted_df_api.merge(df_meta_drop[['Region', 'IncomeGroup', 'Country Code']], on='Country Code', how='left')

    melted_api_meta = melted_api_meta.rename(columns={'Country Name': 'country_name', 'Country Code': 'country_code', 'Year': 'year'
    , 'EducationExpenditure': 'education_expenditure', 'Region': 'region', 'IncomeGroup': 'income_group'})

    life_expectancy_data = life_expectancy_data.rename(columns=lambda x: x.strip().replace(' ', '_'))
    life_expectancy_data.columns = life_expectancy_data.columns.str.lower().str.replace('-', '_')
    life_expectancy_data = life_expectancy_data.rename(columns={'country': 'country_name', 'hiv/aids': 'HIV_AIDS', 'gdp': 'GDP', 'thinness__1_19_years': 'thinness_10_19_years'})
    life_expectancy_data['country_name'] = life_expectancy_data['country_name'].replace({"CÃ´te d'Ivoire": "Cote d'Ivoire"})

    melted_api_meta['year'] = pd.to_datetime(melted_api_meta['year'], format='%Y')
    melted_api_meta['year'] = melted_api_meta['year'].dt.year

    life_expectancy_data = life_expectancy_data.sort_values(by=['country_name', 'year'])
    melted_api_meta = melted_api_meta.sort_values(by=['country_name', 'year'])

    df_flatfile = life_expectancy_data.merge(melted_api_meta[['country_name', 'country_code', 'year', 'education_expenditure', 'region', 'income_group']], 
                    on=['country_name', 'year'], 
                    how='left')

    #Modelling the dimension tables
#COUNTRY_DIM
    COUNTRY_DIM = df_flatfile[['country_code', 'country_name', 'region', 'population']].drop_duplicates().reset_index(drop=True)
    COUNTRY_DIM['country_id'] = COUNTRY_DIM.index
    COUNTRY_DIM= COUNTRY_DIM[['country_id','country_code', 'country_name', 'region', 'population']]

#DATE_DIM
    # Define a function that checks if a year is a leap year
    DATE_DIM = df_flatfile[['year']].drop_duplicates().reset_index(drop=True)

    def is_leap_year(year):
        if (year % 4) == 0:
            if (year % 100) == 0:
                if (year % 400) == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    # Create leap_year column
    DATE_DIM['leap_year'] = df_flatfile['year'].apply(is_leap_year)

    # Create decade column
    DATE_DIM['decade'] = (df_flatfile['year'] // 10) * 10

    # Convert year to data
    #df_le['Year'] = pd.to_datetime(df_le['Year'], format='%Y')
    DATE_DIM['year'] = df_flatfile['year']

#INCOME_GROUP_DIM
    INCOME_GROUP_DIM = df_flatfile[['income_group']].drop_duplicates().reset_index(drop=True)
    income_code_type = {
            'Low income' : 'LIC',
            'Lower middle income': 'LMC',
            'Upper middle income': 'UMC',
            'High income': 'HIC'
        }

    INCOME_GROUP_DIM['income_group_id'] = INCOME_GROUP_DIM.index
    INCOME_GROUP_DIM['income_group_code'] = INCOME_GROUP_DIM['income_group'].map(income_code_type)
    INCOME_GROUP_DIM = INCOME_GROUP_DIM[['income_group_id','income_group_code','income_group']]

#COUNTRY_STATUS_DIM
    COUNTRY_STATUS_DIM = df_flatfile[['status']].drop_duplicates().reset_index(drop=True)
    COUNTRY_STATUS_DIM['country_status_id'] = COUNTRY_STATUS_DIM.index
    COUNTRY_STATUS_DIM = COUNTRY_STATUS_DIM[['country_status_id','status']]

    LE_FACT_TABLE = df_flatfile.merge(COUNTRY_DIM, on=['country_code', 'country_name', 'region', 'population']) \
                    .merge(DATE_DIM, on='year') \
                    .merge(INCOME_GROUP_DIM, on='income_group') \
                    .merge(COUNTRY_STATUS_DIM, on='status') \
                    [['country_id', 'income_group_id', 'country_status_id', 'year', 'life_expectancy', 
            'adult_mortality', 'infant_deaths', 'alcohol', 'percentage_expenditure', 
            'hepatitis_b', 'measles', 'bmi', 'under_five_deaths', 'polio', 
            'total_expenditure', 'diphtheria', 'HIV_AIDS', 'GDP', 
            'thinness_10_19_years', 'thinness_5_9_years', 
            'income_composition_of_resources', 'schooling', 'education_expenditure']]

    LE_FACT_TABLE = LE_FACT_TABLE.sort_values(by='year')
    LE_FACT_TABLE = LE_FACT_TABLE.reset_index(drop=True)
    LE_FACT_TABLE['le_fact_table_id'] = LE_FACT_TABLE.index
    LE_FACT_TABLE = LE_FACT_TABLE[['le_fact_table_id','country_id', 'income_group_id', 'country_status_id', 'year', 'life_expectancy', 
            'adult_mortality', 'infant_deaths', 'alcohol', 'percentage_expenditure', 
            'hepatitis_b', 'measles', 'bmi', 'under_five_deaths', 'polio', 
            'total_expenditure', 'diphtheria', 'HIV_AIDS', 'GDP', 
            'thinness_10_19_years', 'thinness_5_9_years', 
            'income_composition_of_resources', 'schooling', 'education_expenditure']]


    return {"COUNTRY_DIM":COUNTRY_DIM.to_dict(orient="dict"),
    "DATE_DIM":DATE_DIM.to_dict(orient="dict"),
    "INCOME_GROUP_DIM":INCOME_GROUP_DIM.to_dict(orient="dict"),
    "COUNTRY_STATUS_DIM":COUNTRY_STATUS_DIM.to_dict(orient="dict"),
    "LE_FACT_TABLE":LE_FACT_TABLE.to_dict(orient="dict")}



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'