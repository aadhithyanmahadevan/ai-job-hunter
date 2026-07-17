from google import genai

client = genai.Client(api_key="AQ.Ab8RN6JXkjAfBnMoQxMm9B14fR-v3mO8_GOv2zSethmrFeMetw")

for model in client.models.list():
    if "generateContent" in model.supported_actions:
        print(model.name)
