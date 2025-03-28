from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "teknium/OpenHermes-2.5-Mistral-7B"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    trust_remote_code=True
)
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=256)

def ask_model(prompt):
    return pipe(prompt)[0]["generated_text"]
