import gradio as gr
from huggingface_hub import InferenceClient
import os 
import pandas as pd 
from dotenv import load_dotenv
from huggingface_hub import HfApi
import json

from src.smartmovierecommender.smartmovierecommender import main

load_dotenv()

API_KEY = os.getenv("api_key")


def respond(prompt):
    if not prompt: 
        return json.dumps({"error": "Please enter a prompt"})
    
    try:
        cosine_model = main(prompt)
    except Exception as e:
        return json.dumps({"error": f"Error processing the query: {str(e)}"})
    
    if not cosine_model:
        return json.dumps({"error": "No results found for the given query."})
    
    results = [{"file": filepath, "score": float(score)} for filepath, score in cosine_model.items()]
    
    return json.dumps({"results": results})

demo = gr.Interface(
    fn=respond,
    inputs=gr.Textbox(label="Enter your query", placeholder="Type your query here..."),
    outputs=gr.JSON(label="Results"),
    title="Smart Movie Recommender",
    description="This tool provides movie recommendation using cosine similarity calculations."
)

if __name__ == "__main__":
    demo.launch(share=True)




