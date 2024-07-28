import os
import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Set your Groq API key
GROQ_API_KEY = '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'
UNSPLASH_ACCESS_KEY = 'UsP5NZq0aLWj9SPXZWSB4kWPGUbQ7P9U5VvVlsrNz_Y'

# Function to fetch images related to the topic
def fetch_images(topic):
    url = f"https://api.unsplash.com/search/photos?query={topic}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        images = response.json().get('results', [])
        return [image['urls']['small'] for image in images]
    return []

# Function to generate content using Groq API
def generate_content(content_type, topic):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",  # Replace with the actual model name from Groq API documentation
        "messages": [
            {"role": "system", "content": f"You are a helpful assistant."},
            {"role": "user", "content": f"Write a {content_type} about {topic}"}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Streamlit app interface
st.title("Content Generation Assistant")

content_type = st.selectbox(
    "Select the type of content you want to generate:",
    ("Story", "Informal Letter", "Formal Letter", "Blog", "Essay", "Interview Questions")
)

topic = st.text_input("Enter a topic for the content:")
if topic:
    st.subheader(f"Generated {content_type}")
    content = generate_content(content_type, topic)
    if content:
        st.write(content)

        st.subheader("Related Images")
        images = fetch_images(topic)
        for image_url in images:
            st.image(image_url)

# Ensure libraries are installed
try:
    import streamlit
    import requests
    from PIL import Image
except ImportError as e:
    st.error(f"Missing library: {e.name}. Please install it using 'pip install {e.name}'.")

# Debugging information
st.write("   " if GROQ_API_KEY else "GROQ_API_KEY is not set.")
st.write("    " if UNSPLASH_ACCESS_KEY else "UNSPLASH_ACCESS_KEY is not set.")
