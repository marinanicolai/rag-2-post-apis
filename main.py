
from dotenv import load_dotenv
load_dotenv()
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
from groq import Groq


# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

LLM_MODEL = "llama-3.3-70b-versatile"
def generate_answer_with_groq(query: str, similar_chunks: list) -> str:
    """
    Generate answer using Groq LLaMA 3.3 70B Versatile based on retrieved chunks.
    """

    # System instruction
    system_prompt = """
You are a friendly and intelligent Q&A assistant. Your purpose is to understand the user's questions and 
provide clear, simple, and accurate answers. Respond in an easy-to-understand way without adding unnecessary 
details.

Rules:
1️⃣ Listen carefully to the user's question.
2️⃣ Give a direct and helpful answer.
3️⃣ Keep explanations simple and clear.
4️⃣ Do not add extra information unless it helps the user.
5️⃣ Provide examples if needed.
"""

    # Merge all retrieved chunks into plain text
    context_text = "\n\n".join([chunk["text"] for chunk in similar_chunks])

    # Combined prompt for the model
    final_prompt = f"""
System Prompt:
{system_prompt}

Context:
{context_text}

Question:
{query}

Answer:
"""

    # LLM inference with Groq API
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_prompt}
        ],
        max_tokens=512,
        temperature=0.2
    )

    # ✅ Access content via attribute, not dictionary
    return response.choices[0].message.content