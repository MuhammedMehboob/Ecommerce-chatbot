#we use semantic router for routing - its like classifying the prompt
from semantic_router import Route, IndexedRouter
from semantic_router.encoders import HuggingFaceEncoder

encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

faq = Route(
    name='faq',
    utterances=[
        "What is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payment methods are accepted?",
        "How long does it take to process a refund?",
    ]
)

sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
    ]
)

small_talk = Route(
    name='small_talk',
    utterances=[
        "hi",
        "hello",
        "hey there",
        "how are you?",
        "good morning",
        "thank you",
        "thanks a lot",
        "what is your name?",
        "who are you?",
        "what can you do?",
    ]
)

router = IndexedRouter(routes=[faq, sql, small_talk], encoder=encoder)

if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)