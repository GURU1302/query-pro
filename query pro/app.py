import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure our API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Google Gemini Model and provide SQL query as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the SQL database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define Your Prompt
prompt = [
"""
You are an expert in converting English questions to SQL queries!
The SQL database has the name REVIEW and contains reviews of clothing items. Here are some details about the unique values in certain columns:

- Unique values in the division name: ['General' 'General Petite' 'Intimates']
- Unique values in the department name: ['Dresses' 'Bottoms' 'Tops' 'Intimate' 'Jackets' 'Trend']
- Unique values in the class name: ['Dresses' 'Pants' 'Blouses' 'Knits' 'Intimates' 'Outerwear' 'Lounge'
 'Sweaters' 'Skirts' 'Fine gauge' 'Sleep' 'Jackets' 'Swim' 'Trend' 'Jeans'
 'Shorts' 'Legwear' 'Layering' 'Casual bottoms' 'Chemises']

You can ask questions related to the REVIEW table using these column values to filter the results.

For example:
- How many reviews are there for dresses in the Dresses department?
  SQL: SELECT COUNT(*) FROM REVIEW WHERE department_name = 'Dresses' AND class_name = 'Dresses';

- What is the average rating for tops in the General division?
  SQL: SELECT AVG(rating) FROM REVIEW WHERE division_name = 'General' AND department_name = 'Tops';

- Can you provide the review text for intimate clothing items?
  SQL: SELECT review_text FROM REVIEW WHERE department_name = 'Intimate';
  also the SQL code should not have ``` in beginning or end and SQL word in output
"""
]

# Streamlit App
st.set_page_config(page_title="SQL Query Retrieval", page_icon=":bar_chart:")

# Page Title and Description
st.title("Review Retrieval System")
st.markdown("""
An interactive application to retrieve reviews based on the queries.
""")

# Input Box for User's Question
question = st.text_area("Input your question here:", key="input")

# Button to Generate Query
submit = st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    data = read_sql_query(response, "review.db")
    
    st.subheader("The Response is")
    for row in data:
        st.write(row)
    
    # Convert data to a string representation
    data_str = "\n".join([str(row) for row in data])

    # Store the data and question for later use
    st.session_state.data = data_str
    st.session_state.question = question

# Button to Draw Conclusion
if "data" in st.session_state:
    conclusion_button = st.button("Draw Conclusion")

    if conclusion_button:
        combined_text = f"{st.session_state.question}\n\n{st.session_state.data}"
        new_prompt = [
            """
                "You are an expert in drawing smart and decisive conclusions based on input lines 
                separated by a two-line gap. The first line represents a question asked, 
                which is converted into a SQL query. The second line represents the answer received 
                when running that query on the database. Your expertise lies in analyzing both the question 
                and its corresponding answer to provide insightful recommendations. Your conclusions are 
                aimed at guiding recommendations, determining the quality of items, and making decisive judgments. 
                Your conclusions may encompass recommendations on whether something is good or bad, whether it is 
                recommended or not, and various other decisive insights derived from the input provided." 
            """
        ]
        new_response = get_gemini_response(combined_text, new_prompt)
        st.subheader("Conclusion:")
        st.write(new_response)

# Footer
st.markdown("---")
st.markdown("ALL RIGHTS RESERVED")

# Optionally, you can add some custom CSS to further improve the styling
st.markdown(
    """
    <style>
        body {
            color: #333;
            background-color: #f0f2f6;
            font-family: Arial, sans-serif;
        }
        .stTextInput>div>div>textarea {
            border-radius: 8px;
            padding: 10px;
            background-color: #ffffff;
        }
        .stButton>button {
            border-radius: 8px;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            transition: background-color 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stCodeBlock {
            border-radius: 8px;
            padding: 10px;
            background-color: #f7f7f7;
        }
    </style>
    """,
    unsafe_allow_html=True
)