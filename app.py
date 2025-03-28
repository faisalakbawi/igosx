import gradio as gr
import pandas as pd
from ai_cleaning import ai_cleaning
from model import ask_model

uploaded_df = None

def process(file):
    global uploaded_df
    uploaded_df = pd.read_csv(file.name)
    ai_guess = ask_model(f"What type of data is this?\n{uploaded_df.head(2).to_string()}")
    cleaned, log = ai_cleaning(uploaded_df)
    return ai_guess, "\n".join(log), cleaned

with gr.Blocks() as app:
    gr.Markdown("# 🤖 FaisalBot AI Data Cleaner (v3)")
    file = gr.File(label="Upload CSV")
    btn = gr.Button("🧠 Clean with AI")
    guess = gr.Textbox(label="AI Data Recognition", interactive=False)
    log = gr.Textbox(label="Cleaning Log", lines=10)
    table = gr.Dataframe(label="Cleaned Preview")
    btn.click(fn=process, inputs=file, outputs=[guess, log, table])

app.launch()