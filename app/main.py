import streamlit as st
from FAQ import ingest_faq_data,FAQ_chain
from sql import sql_chain
from router import router
from small_talk import talk
from pathlib import Path


faqs_path = Path(__file__).parent / "resources/faq_data.csv"
ingest_faq_data(faqs_path)

def ask(query):
    route = router(query).name
    print(f"[router] {query!r} -> {route}")
    if route == 'faq':
        return FAQ_chain(query)
    elif route == 'sql':
        return sql_chain(query)
    elif route == 'small_talk':
        return talk(query)
    else:
        return "Sorry, I can only help with store policies and product searches."

st.title("E-commerce Bot")

query = st.chat_input("Write your query")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if query:
    with st.chat_message("user"):
        st.markdown(query)
    st.session_state.messages.append({"role":"user", "content":query})

    response = ask(query)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


