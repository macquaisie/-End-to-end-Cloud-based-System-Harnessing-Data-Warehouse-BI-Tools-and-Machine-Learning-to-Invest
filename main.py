import sqlite3
import streamlit as st
from streamlit import session_state as state
import streamlit.components.v1 as components
import pickle
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_array, check_is_fitted
from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer
import numpy as np
from xgboost import XGBRegressor
import pandas as pd




class OutlierHandler(BaseEstimator, TransformerMixin):
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors
        self.imputer = KNNImputer(n_neighbors=self.n_neighbors)

    def fit(self, X, y=None):
        self.IQR = X.quantile(0.75) - X.quantile(0.25)
        self.Q1 = X.quantile(0.25)
        self.Q3 = X.quantile(0.75)
        return self

    #def transform(self, X):
    #    X_out = X.copy()
    #    X_out[((X_out < (self.Q1 - 1.5 * self.IQR)) | (X_out > (self.Q3 + 1.5 * self.IQR)))] = np.nan
    #    X_out = pd.DataFrame(self.imputer.fit_transform(X_out), columns=X.columns)
    #    return X_out

    def transform(self, X, y=None):
        X_out = X.copy()
        for col in X_out.columns:
            bool_series = ((X_out[col] < (self.Q1[col] - 1.5 * self.IQR[col])) |
                          (X_out[col] > (self.Q3[col] + 1.5 * self.IQR[col])))
            X_out[col][bool_series] = np.nan
        return X_out

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)


#Pass this function inside FunctionTransformer instead of passing just np.log to avoid cases with values equal zerodef log_transform(X):
def log_transform(X):
    return np.log(X + 10e-5)


# loading the saved models

le_model = pickle.load(open('gb_model_2.sav', 'rb'))



# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create table - USERS
c.execute('''CREATE TABLE IF NOT EXISTS USERS
             ([generated_id] INTEGER PRIMARY KEY,[username] text, [password] text)''')

def validate(username, password):
    c.execute(f'SELECT * FROM USERS WHERE username="{username}" AND password="{password}"')
    if c.fetchone():
        return True
    return False

def add_user(username, password):
    c.execute(f'SELECT * FROM USERS WHERE username="{username}"')
    if c.fetchone():
        return False
    else:
        c.execute(f'INSERT INTO USERS (username,password) VALUES ("{username}", "{password}")')
        conn.commit()
        return True

def main():
    # At the top of your app.py, after imports
    l = st.empty()
    logo = l.image("logo.png", use_column_width=True)

    if 'auth' not in state:
        state.auth = False

    if not state.auth:
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')

            if st.button("Login"):
                if validate(username, password):
                    st.success("Logged in Successfully")
                    state.auth = True
                    # Redirect to Project Overview page after login
                    state.page = "Project Overview"
                else:
                    st.error("Incorrect username or password")

        elif choice == "Register":
            st.title("Registration Page")
            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type='password')

            if st.button("Register"):
                if add_user(new_user, new_password):
                    st.success("User registered successfully")
                else:
                    st.error("Username already taken")

    if state.auth:
        st.sidebar.image("logo.png", use_column_width=True)
        menu = ["Project Overview", "Life Expectancy Prediction", "Life Expectancy Dashboard", "System Architecture & Data Dictionary", "Logout"]
        choice = st.sidebar.selectbox("Menu", menu, index=menu.index(state.page if 'page' in state else "Project Overview"))

        if choice == "Project Overview":
            l.empty()
            state.page = "Project Overview"
            st.title('Project Overview')
            st.subheader("Abstract")
            st.write("The life expectancy gap between developed, and developing countries is a frightening global health concern. Numerous factors, including socioeconomic conditions such as GDP, healthcare systems tackling chronic diseases and pandemics, and lifestyle factors such as excessive alcohol consumption, smoking, and obesity, just to name a few, contribute to these disparities. This study aims to provide a comprehensive, end-to-end, cloud-based, data-driven system to analyze the life expectancy gap by leveraging the strengths of Data Warehouse, Business Intelligence Tools, and Machine Learning techniques with much focus on Data Warehouse. A fully automated cloud base Data Warehouse will be designed and developed to integrate and harmonize data from various sources, such as the World Bank, World Health Organization, and UN, facilitating the investigation and visualization of complex data relationships between life expectancy and multiple determinants.  A Machine learning model is then generated based on the life expectancy Data Warehouse for different countries analyzed to identify key factors influencing life expectancy and a web application to serve these findings in a user-friendly interface. By combining Data Warehouse, Business Intelligence Tools, and Machine Learning methodologies, this research project seeks to uncover trends, disparities, and potential interventions to reduce the life expectancy gap and promote health equity across different countries and populations. The findings of this study will contribute to a better understanding of the drivers of life expectancy disparities and best inform policymakers and decision-makers with strategies for addressing these challenges in global policies and practices.")
            st.subheader("Problem statement")
            st.write("One major problem faced in the world, especially in the developing parts of the world is the decline and failing control of LE. This over the years has been due to many reasons for which social, economic, health and lifestyle have contributed to. It is important therefore to have an end-to-end fully automated cloud-based system that is cost-effective, easy to implement, and highly efficient in identifying the key factors affecting LE. This could also serve as a framework or blueprint to assist guide government, policymakers, and all stakeholders in developing more sustainable strategies for promoting health equity and positively improving overall LE.")
            st.subheader("Research Aim")
            st.write("This project aims to design and develop a fully automated cloud-based end-to-end system that comprises a Data Warehouse, visualizations of the data, a predictive ML model, and a web application that bundles all together in determining major trends, disparities, and potential interventions to reduce LE. It seeks to provide the needed insights for individuals and guide decision-makers and policymakers in designing and implementing targeted interventions. The focus is on developing a fully automated cloud-based Data Warehouse. This system will scrape data from the World Bank, and Kaggle datasets that consist of World Health Organization, and UN datasets of 193 countries over a 16-year period, clean and preprocess the data and store it in a well-designed Data Warehouse for visualization, analysis, and generate predictive ML model which, will inform strategies for promoting health and economic equity across different countries.")
            st.subheader("Research Objective")
            st.write('The primary objectives of this project are to:')
            st.markdown('<ol><li>Demonstrate the importance of building a data warehouse for Life Expectancy. </li><li>Design a fully automated cloud-based data warehouse using a star schema for efficient storage and querying of Life Expectancy data and related factors.</li><li>Analyze and visualize the relationships between Life Expectancy and its influencing key factors to identify the main trends and disparities causing the slow decline in  LE by creating a dashboard.</li><li>Train and evaluate a model using 3 machine learning algorithms to predict Life Expectancy and the key features causing the slow decline of LE based on key selected metrics.</li><li>Develop an API and web application for easy access to the insights of Life Expectancy data, dashboard, and machine learning model.</li><li>Provide insights and recommendations for policies and interventions aimed at reducing the life expectancy gap, and promoting health equity.</li></ol>', unsafe_allow_html=True)
    
        
        elif choice == "Life Expectancy Prediction":
            state.page = "Life Expectancy Prediction"
            # page title
            l.empty()
            st.title('Life Expectency Prediction using ML')
            
            
            # getting the input data from the user
            col1, col2, col3 = st.columns(3)
                
            with col1:
                adult_mortality = st.text_input('Adult Mortality Rate', value="0.0")
                
            with col2:
                alcohol = st.text_input('Alcohol Consumption', value="0.0")
            
            with col3:
                bmi = st.text_input('BMI Value', value="0.0")
            
            with col1:
                diphtheria = st.text_input('Diphtheria Immunization Rate', value="0.0")
            
            with col2:
                education_expenditure = st.text_input('Education Expenditure Value', value="0.0")
            
            with col3:
                GDP = st.text_input('GDP Value', value="0.0")
            
            with col1:
                hepatitis_b = st.text_input('Hepatitis B Immunization Rate', value="0.0")
            
            with col2:
                HIV_AIDS = st.text_input('HIV/AIDS Prevalence Rate', value="0.0")
            with col3:
                infant_deaths = st.text_input('Number of Infant Deaths', value="0.0")
            
            with col1:
                income_composition_of_resources = st.text_input('Income Composition Value', value="0.0")
            
            with col2:
                measles = st.text_input('Number of Measles Cases', value="0.0")
            with col3:
                percentage_expenditure = st.text_input('Percentage Expenditure on Health', value="0.0")
            
            with col1:
                polio = st.text_input('Polio Immunization Rate', value="0.0")
            
            with col2:
                schooling = st.text_input('Average Schooling Years', value="0.0")
            with col3:
                thinness_5_19_years = st.text_input('Thinness Rate (5-19 Years)', value="0.0")
            
            with col1:
                total_expenditure = st.text_input('Total Expenditure on Health', value="0.0")
            
            with col2:
                under_five_deaths = st.text_input('Number of Deaths (Under Five Years)', value="0.0")
            
            # Check if any input is empty
            input_list = [adult_mortality, alcohol, bmi, diphtheria, education_expenditure, GDP, hepatitis_b, HIV_AIDS, infant_deaths, income_composition_of_resources, measles, percentage_expenditure, polio, schooling, thinness_5_19_years, total_expenditure, under_five_deaths]

            def is_valid_number(value):
                try:
                    # Check for float
                    float(value)
                    return True
                except ValueError:
                    return False

            invalid_inputs = [input_value for input_value in input_list if input_value == "" or not is_valid_number(input_value)]

            if invalid_inputs:
                st.warning("Please ensure all input fields are filled and contain valid numbers (integers or floats)!")
            else:
                input_data = pd.DataFrame({
                'GDP': [GDP], 
                'HIV_AIDS': [HIV_AIDS], 
                'adult_mortality': [adult_mortality], 
                'alcohol': [alcohol], 
                'bmi': [bmi],
                'diphtheria': [diphtheria],
                'education_expenditure': [education_expenditure],
                'hepatitis_b': [hepatitis_b],
                'infant_deaths': [infant_deaths],
                'income_composition_of_resources': [income_composition_of_resources],
                'measles': [measles],
                'percentage_expenditure': [percentage_expenditure],
                'polio': [polio],
                'schooling': [schooling],
                'thinness_5_19_years': [thinness_5_19_years],
                'total_expenditure': [total_expenditure],
                'under_five_deaths': [under_five_deaths]
                }).astype(float)

            #input_name =[GDP, HIV_AIDS, adult_mortality, alcohol, bmi, diphtheria, education_expenditure, hepatitis_b, infant_deaths, income_composition_of_resources, measles, percentage_expenditure, polio, schooling, thinness_5_19_years, total_expenditure, under_five_deaths

            #input_data[input_name].replace('', 0, inplace=True)
            #input_data = input_data.astype(float)   
                
            # code for Prediction
            le_years = ''
            
            # creating a button for Prediction
            
            if st.button('Life Expectency Prediction'):
                le_prediction = le_model.predict(input_data)
                
                if (le_prediction[0] >= 72.27):
                    le_years = f'{le_prediction[0]:.2f}years  is above the World\'s Life Expectancy Average Age'
                    st.success(le_years)
                else:
                    le_years = f'{le_prediction[0]:.2f}years is below the World\'s Life Expectancy Average Age'
                    st.warning(le_years)
            st.write('The core idea was to distill the essence of the vast dataset, narrowing our focus solely to those key factors that bear a palpable impact on LE.')   
            st.write('Our research delved into the exploration of three machine learning algorithms: the Decision Tree, the ever-resourceful Random Forest, and the versatile XGBoost. Each of these models underwent rigorous training, fortified by the application of cross-validation techniques on the training subset.')
            st.write('A decision was then made to choose the best (ie. Gradient Boosting Model) based on below Cross Validation Scores.')
            # Create a sample dataframe
            data = {
                'Algorithm': ['Decision Tree', 'Random Forest', 'Gradient Boosting'],
                'Mean RMSE in CV': [3.547635, 2.662035, 2.703505],
                'Mean R2 in CV': [0.858987, 0.920033, 0.917711],
                'Mean MSE in CV': [12.637347, 7.187212, 7.394130],
                'Mean MAE in CV': [2.046559, 1.569685, 1.696369],
                'Mean Adjusted R2 in CV': [0.857876, 0.919403, 0.917064]
            }
            df = pd.DataFrame(data)

            # Display the dataframe as a table in Streamlit
            st.table(df)
            st.write('Below is also a plot of feature importance for Gradient Boosting Model.') 
            st.image("Feature Importance.png", use_column_width=True)
            
        elif choice == "Life Expectancy Dashboard":
            l.empty()
            state.page = "Life Expectancy Dashboard"
            st.title('Life Expectancy Dashboard')
            components.iframe("https://lookerstudio.google.com/embed/reporting/28c9c128-fb66-4573-ae70-b28b468ac04a/page/B2WUD", width=900, height=900)
            st.subheader('**Some Facts**')
            st.write('**Data source: From the World Bank, and Kaggle which consists of data from the World Health Organization (WHO), and the United Nations (UN).')
            st.write('**Data spectrum: Covers diverse indicators, from demographic data to health infrastructure and lifestyle metrics.')   
            st.write('**Date Collection Period: 2000 to 2015 (16years) period.')
            st.write('**Some examples of Data spectrum: factors like Education Expenditure, BMI, HIV/AIDS, Total expenditure, and GDP just to name a few.')
            
            
        elif choice == "System Architecture & Data Dictionary":
            l.empty()
            st.title('System Architecture')
            st.image("LE ARCHITECTURE.png", use_column_width=True)
            st.title('Data Dictionary') 
            # Data for the table
            data1 = {
                'Feature Name': [
                    'country_code', 'country_name', 'region', 'population', 'status',
                    'year', 'leap_year', 'decade', 'income_group_code', 'income_group',
                    'life_expectancy', 'adult_mortality', 'infant_deaths', 'alcohol',
                    'percentage_expenditure', 'hepatitis_b', 'measles', 'bmi', 'under_five_deaths',
                    'polio', 'total_expenditure', 'diphtheria', 'HIV_AIDS', 'GDP',
                    'thinness_10_19_years', 'thinness_5_9_years', 'income_composition_of_resources',
                    'schooling', 'education_expenditure'
                ],
                'Description': [
                    'Country Code: Unique identifier for each country.',
                    'Various countries in alphabetical order.',
                    'Region: Geographical area where the country is located.',
                    'Population of the country.',
                    'Developed or developing status of the country.',
                    'Years from 2000 – 2015.',
                    'Leap Year: Indicates if the year is a leap year (True or False).',
                    'Decade: The decade to which the year belongs.',
                    'Income Group Code: Code representation of the income group of the country.',
                    'Income Group: Classification based on the country\'s income (e.g., High, Medium).',
                    'Life Expectancy in age.',
                    'Mortality rates of Adults for both males and females.',
                    'Number of infant deaths per 1000 population.',
                    'Alcohol, recorded per capita (15+) consumption in liters of pure alcohol.',
                    'Expenditure on health as a percentage of Gross Domestic Product per capita (in%).',
                    'Hepatitis B (HepB) immunization coverage among 1-year-olds (in%).',
                    'Number of reported cases of measles per 1000 population.',
                    'Average Body Mass Index of the entire population.',
                    'Number of under-five deaths per 1000 population.',
                    'Polio (Pol3) immunization coverage among 1-year-olds (in%).',
                    'General government expenditure on health as a percentage of total government expenditure (in%).',
                    'Diphtheria Tetanus toxoid and Pertussis (DTP3) immunization coverage among 1-year-olds (%).',
                    'Deaths per 1 000 live births HIV/AIDS (0–4 years).',
                    'Gross Domestic Product per capita (in USD).',
                    'Prevalence of thinness among children and adolescents for Age 1 to 19 (%).',
                    'Prevalence of thinness among children and adolescents for Age 5 to 9 (%).',
                    'Income composition of resources.',
                    'Number of years of Schooling(years).',
                    'Education Expenditure: Percentage of GDP spent on education.'
                ]
            }

            # Convert data dictionary to pandas DataFrame
            df_1 = pd.DataFrame(data1)

            # Display the DataFrame as a table in Streamlit
            st.table(df_1)   
            
    
        elif choice == "Logout":
            state.auth = False
            st.sidebar.empty()
            st.info("Logged out")

if __name__ == "__main__":
    main()

