import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import pandas as pd
from pathlib import Path
from groq import Groq
import os

load_dotenv()
faq_data = Path(__file__).parent/"resources/faq_data.csv"

ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='sentence-transformers/all-MiniLM-L6-v2')

chroma_client = chromadb.Client()
collection_name_faq = 'faqs'
groq_client = Groq()


def ingest_faq_data(path):
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data into ChromDB.........")
        collection = chroma_client.get_or_create_collection(
            name=collection_name_faq,
            embedding_function=ef
        )
        df = pd.read_csv(path)
        docs = df['question'].to_list()
        metadata = [{'answer': ans} for ans in df['answer'].to_list()]  # this is need coz ChromaDB wants metadatas as a list of dictionaries.
        ids = ids = [f"id_{i}" for i in     range(len(docs))]  # this is needed coz There’s no ID column in the CSV, so the loop makes them
        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )
        print(f"FAQ data successfully ingested into chroma collection : {collection_name_faq}")
    else:
        print(f"Collection {collection_name_faq} already exist!.......")

def get_relevant_qa(query):
    collection = chroma_client.get_collection(name= collection_name_faq, embedding_function= ef)
    result = collection.query(
        query_texts = [query],
        n_results=2
    )
    return result

def FAQ_chain(query):
    result = get_relevant_qa(query)
    context = "".join([r.get('answer') for r in result['metadatas'][0]])
    answer = generate_answer(query, context)
    return answer

def generate_answer(query, context):
    prompt = f'''Given the following context and question, generate answer based on this context only.
    If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.
    

        CONTEXT: {context}

        QUESTION: {query}
        '''

    completion = groq_client.chat.completions.create(
        model=os.environ['GROQ_MODEL'],
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return completion.choices[0].message.content

if __name__ == '__main__':
    ingest_faq_data(faq_data)
    query = "Do you take cash as the payment option"
    answer = FAQ_chain(query)
    print("answer:", answer)

