# MySQL DB Connection Utility
import mysql.connector
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import re
from matplotlib import pyplot as plt
import json

def get_db_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='saas',
            password='',
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    

def close_db_connection(connection):
    """Close the MySQL database connection."""
    if connection:
        try:
            connection.close()
        except mysql.connector.Error as err:
            print(f"Error closing connection: {err}")
    else:
        print("No connection to close.")

def execute_query(query, params=None):
    """Execute a SQL query and return the result."""
    connection = get_db_connection()
    if connection is None:
        return None
    
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        return None
    finally:
        cursor.close()
        close_db_connection(connection)


def create_query(question, schema):
    # Create chat template
    template = """
    You are a MySQL expert with access to the database.

    Generate a SQL query based on the given question and schema.

    Rules:
    - Use only the provided schema/databse in query.
    - if required Join on ID columns, casting them to BINARY.
    - use schema name as prefix for all table names.
    - In WHERE clauses:
    - Prefer filtering by ID columns first.
    - Cast all columns to BINARY.
    - Use UPPER() for all comparisons.
    - Use LIKE for partial matches, with wildcards (%) between all parts of the search text.
    - Format LIKE clauses as: LIKE UPPER('%Part1%Part2%')
    - Do not generate any markdown.
    - Return only the SQL query — no explanations
    - Use inner queries as much as possible.
    Question: {question}
    Schema: {schema}
    """

    prompt_template = ChatPromptTemplate.from_template(template)
    model = ChatOllama(model="llama3", temperature=0.1)
    result = model.invoke(prompt_template.invoke({"question": question, "schema": schema+" schema"}))
    return result.content

def clean_sql_output(output):
    # Removes ```sql ... ``` or ```...``` wrappers
    return re.sub(r"^```(?:sql)?\s*|```$", "", output.strip(), flags=re.MULTILINE)


def understand_cateforize_context(question):
    template = """
    You are a Prompt Engineering expert.

    You need to understand the context of the given text and categorize it into specified categories & generate Prompt for the category to use in AI Model.

    Below are the categories:
          - SQLQueryGeneration
          - DataAnalysis
          - DataVisualization
    Rules:
        Create a JSON Object with the following structure, so that I can use it my code
                {{  
                    "SQLQueryGeneration": "Generate SQL Query......"                
                    "DataAnalysis":"DataAnalysis explanation......"                
                    "DataVisualization":"DataVisualization explanation......"                
                }}
        For any data required to generate SQL query, you can consider SQLQueryGeneration.
        Do not use any other format, just return JSON Object.
        Do not give any explanation, just return JSON Object.
        If question/prompt have reference to generate visualization, then add "DataVisualization" category with explanation to generate visualization.
        If question/prompt have reference to generate analysis, then add "DataAnalysis" category with explanation to generate analysis.
        If question/prompt have reference to generate SQL query, then add "SQLQueryGeneration" category with explanation to generate SQL query.
        Any required data must need to fetch from the database, so you can use SQL query to fetch data.
        You just generate proqmpt for the category, do not generate any SQL query.
    Question: {question}
    """


    prompt_template = ChatPromptTemplate.from_template(template)
    model = ChatOllama(model="llama3", temperature=0.1)
    result = model.invoke(prompt_template.invoke({"question": question}))
    return result.content

def generate_matplot_lib_compatible_data(text):
    template = """
    You are a Matplotlib expert.

    Rules:
        - Understand what kind of plot is needed based on the text.
        - Generate JSON object with the following structure:
                {{
                    "plot_type": "pie",  # or "bar", "line", etc.
                    "data": {{
                        "labels": ["label1", "label2", ...],
                        "values": [value1, value2, ...]
                    }},
                    "title": "Title of the plot"
                }}
        - Do not generate any SQL query.
        - Do not give any explanation, just return JSON Object.
        - Do not generate any markdown.
        - Do not generate any code.
        - Generate only JSON object with the required data for the plot.

    Text: {text}
    """

    prompt_template = ChatPromptTemplate.from_template(template)
    model = ChatOllama(model="llama3", temperature=0.1)
    result = model.invoke(prompt_template.invoke({"text": text}))
    return result.content


def main():

    schema = """
    -- patient_service_db.patient_info definition

    CREATE TABLE patient_service_db.`patient_info` (
    `patient_code` bigint NOT NULL AUTO_INCREMENT,
    `patient_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    `address` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `birth_date` date DEFAULT NULL,
    `date_create` date DEFAULT NULL,
    `date_modified` date DEFAULT NULL,
    `first_examination_date` date DEFAULT NULL,
    `patient_gender` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `patient_mobile` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `patient_name_english` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `patient_name_marathi` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `patient_status` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `RefferedBy` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `day_left` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `follow_up_date` date DEFAULT NULL,
    `last_examination_on` date DEFAULT NULL,
    `recent_case_no` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `e_mailid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    `media_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
    PRIMARY KEY (`patient_code`)
    ) ENGINE=InnoDB AUTO_INCREMENT=57259 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    """

    prompt = "Can you fetch data categorise patients in infants, kids, middle agae, old age with count according to date of birth. After generate data create pie chart for the same. Also give me summary of the data in english."
    #prompt = "Give me patient cound by geneder and create bar chart for the same."

    context_str = understand_cateforize_context(prompt)
    print("Context Understanding:", context_str)
    try:
        context = json.loads(context_str)
    except Exception as e:
        print("Error parsing context JSON:", e)
        context = {}

    query = context.get("SQLQueryGeneration", None)
    dataAnalysis = context.get("DataAnalysis", None)
    dataVisualizaion =  context.get("DataVisualization",None)


    query_result = None
    if(query is not None):
        query = create_query(prompt, schema)
        print ("Generated Query:", query)
        query_result = execute_query(clean_sql_output(query))
        print ("Query Result : ", query_result)

    if query_result is None or len(query_result) == 0: exit(0)

    if(dataAnalysis is not None):
        model = ChatOllama(model="llama3", temperature=0.1)
        result = model.invoke("I have data : "+str(query_result)+" and I need to analyse it as per the following instruction : "+dataAnalysis)
        print("Data Analysis Result:", result.content)

    dataVisualizaion=""
    if(dataVisualizaion is not None):
        result = generate_matplot_lib_compatible_data(query_result)
        result = json.loads(result)

        print("Data Visualization Result:", result)
        plt.title(result.get("title", "Generated Plot"))
        if result.get("plot_type") == "bar":
            plt.bar(result.get("data", {}).get("labels", []), result.get("data", {}).get("values", []))
        elif result.get("plot_type") == "line":
            plt.plot(result.get("data", {}).get("labels", []), result.get("data", {}).get("values", []))
        elif result.get("plot_type") == "pie":
            plt.pie(result.get("data", {}).get("values", []), labels=result.get("data", {}).get("labels", []))
        plt.show()