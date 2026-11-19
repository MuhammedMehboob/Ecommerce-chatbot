import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
groq_client = Groq()

small_talk_prompt = """You are a friendly assistant for an online shoe store.
You can help customers with two things:
1. Store policies: returns, refunds, payments, delivery, discounts.
2. Finding shoes by brand, price, discount or rating.

Reply to the customer's message briefly and naturally (1-2 sentences).
Only greet them if they greeted you. If it fits, mention what you can help with."""


def talk(query):
    completion = groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[
            {"role": "system", "content": small_talk_prompt},
            {"role": "user", "content": query},
        ],
        temperature=0.5,
        max_tokens=1024,
    )
    return completion.choices[0].message.content