openai_api = "sk-6k8_kpBRmMS1BhileZZMRZiZvRLRn9LydNPQeyzzrHT3BlbkFJdnZTH-frDQv8accDvEWD78422F9aYysyvhwVBMJ4kA"

import pandas as pd
import openai  # Assuming you're using OpenAI's GPT API

# Sample DataFrame
data = {
    'resource_id': [
        '72fd6ff5-6ef3-4fc7-b0dd-d60da63d1af5',
        '450fe5d1-3b7f-424b-b47d-beb6098d94dd',
        '2c87a4b3-f9d5-4b23-bb09-927855bbe555',
        'df1eeda1-e8c2-4526-923d-806f70ef0ee9',
        '3fe14604-7b57-4de2-b6a6-bbbd7fe1f02d',
        'caf36831-061a-4ec5-ad4f-9baf5baf4d20',
        'a58e4c50-ad01-449f-8cd4-0d3aac75a252',
        'ae6c452d-c7e9-4706-8741-a470ab3a51c4',
        '46750a42-4201-4a38-aff8-75031b5d2393',
        'a6e7356b-f34d-4d58-bc62-b373242c45be'
    ],
    'title': [
        'State/UT-wise Number of OBC Candidates who have...',
        'State/UT-wise Details of Fund Released under P...',
        'State/ UT-wise Number of Skill Development Cen...',
        'District-wise Number of Persons Placed in the ...',
        'Year-wise Details of Candidates Trained and Re...',
        'Details of Trainings Provided in Tourism and H...',
        'State/UT-wise Number of Candidates Enrolled, T...',
        'Caste-wise details of Trainings Provided to SC...',
        'State/UT-wise Total Number of Skill Developmen...',
        'State/UT-wise list of the Candidate Trained an...'
    ]
}

search_data = pd.DataFrame(data)

# Initialize OpenAI API
openai.api_key = 'your_api_key_here'

# Define the prompt
search_title = "Get the resource_id for the title containing 'OBC Candidates'."

# Interact with the LLM
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": search_title}
    ]
)

# Extract relevant information from the LLM's response
response_text = response['choices'][0]['message']['content']

# Assuming the response gives you the title directly, you can filter the DataFrame
result = search_data[search_data['title'].str.contains(response_text, case=False)]

# Get the resource_id(s)
resource_ids = result['resource_id'].tolist()

print(resource_ids)
