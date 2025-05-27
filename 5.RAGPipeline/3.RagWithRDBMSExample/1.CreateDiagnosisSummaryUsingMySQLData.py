# MySQL DB Connection Utility
import mysql.connector
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

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
    You are a MySQL expert with access to the `case_service_db` database.

    Generate a SQL query based on the given question and schema.

    Rules:
    - Use only the provided schema.
    - Always join on ID columns, casting them to BINARY.
    - In WHERE clauses:
    - Prefer filtering by ID columns first.
    - Cast all columns to BINARY.
    - Use UPPER() for all comparisons.
    - Use LIKE for partial matches, with wildcards (%) between all parts of the search text.
    - Format LIKE clauses as: LIKE UPPER('%Part1%Part2%')
    - Return only the SQL query — no explanations, no markdown.

    Question: {question}
    Schema: {schema}
    """


    prompt_template = ChatPromptTemplate.from_template(template)
    model = ChatOllama(model="llama3", temperature=0.1)
    result = model.invoke(prompt_template.invoke({"question": question, "schema": schema+" schema"}))
    return result.content


def describe_the_diagnosis(text):
    model = ChatOllama(model="llama3", temperature=0.1)
    result = model.invoke("What do you understand from the text, give me summary in english. Dont apology just give transaction whatever you could : "+text)
    return result.content


schema = """

CREATE TABLE case_service_db.`case_diagnosis_info` (
  `case_diagnosis_id` bigint NOT NULL AUTO_INCREMENT,
  `case_id` varchar(255) DEFAULT NULL,
  `created_at` date DEFAULT NULL,
  `detailed_diagnosis_chikitsa` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `diagnosis_title` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `patient_id` varchar(255) DEFAULT NULL,
  `symptoms_lakshana` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `patient_name` varchar(255) DEFAULT NULL,
  `updated_diagnosis_date` date DEFAULT NULL,
  PRIMARY KEY (`case_diagnosis_id`)
) ENGINE=InnoDB AUTO_INCREMENT=267367 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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

query = create_query("give me last 5 case diagnosis title for patient name in english like 'Abdul'", schema)
#print ("Generated Query:", query)
result = execute_query(query)
diagnosis=[]
if result is not None:
    diagnosis.append(result)

result_string = str(result)

#print("Diagnosis Titles:", result_string)

summary = describe_the_diagnosis(result_string) 

print("Diagnosis Summary:", summary)