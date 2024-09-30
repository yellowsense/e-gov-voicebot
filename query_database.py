import pandas as pd
from assets.api import GOOGLE_API_KEY
import google.generativeai as genai

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

df = pd.read_csv(r"c:\\Users\\Hemanth\\Desktop\\python-bhashini\\data.csv")
query = "How many people benefited in Gujarat from the year 2018 to 2019?"

prompt = f"{query}.  Use the following data as context:\n{df}.  Keep the answer short and simple."

response = model.generate_content(prompt)

# print(response.text)

def get_query_result(query: str)->str:
    
    prompt = f"{query}.  Use the following data as context:\n{df}.  Keep the answer short and simple."
    response = model.generate_content(prompt)
    
    return response.text  