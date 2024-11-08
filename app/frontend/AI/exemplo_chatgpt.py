import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Set your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to send a question to GPT-4
def pergunte_ao_chatgpt(pergunta: str):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": ""}
        ]
    )
    # Extracting the actual content message from the response
    return response.choices[0].message.content

# Asking the question
question = "Quanto eu vendi ontem?"
answer = pergunte_ao_chatgpt(question)

# Print the response
print(f"Resposta do ChatGPT: {answer}")