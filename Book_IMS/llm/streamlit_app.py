# streamlit_app.py
import streamlit as st
import requests
import pandas as pd

API_ENDPOINT = "http://127.0.0.1:8000/chat/"

st.title("Book Information Chatbot")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

user_message = st.text_input("You:", "")

def display_conversation():
    for msg in st.session_state['messages']:
        role = "User" if msg['role'] == "user" else "Bot"
        st.write(f"{role}: {msg['content']}")

if st.button("Send"):
    if user_message:
        st.session_state['messages'].append({"role": "user", "content": user_message})
        payload = {"messages": st.session_state['messages'], "num_books": 2}

        try:
            response = requests.post(API_ENDPOINT, json=payload, timeout=30)
            if response.status_code == 200:
                bot_response = response.json().get('response', "Sorry, there was an error processing your request.")
                st.session_state['messages'].append({"role": "bot", "content": bot_response})

                # Check if the response is a dict containing book details
                if isinstance(bot_response, dict):
                    book_details = pd.DataFrame([bot_response])
                    st.table(book_details)
                else:
                    st.write(f"Bot: {bot_response}")
            else:
                st.write("Bot: Sorry, there was an error processing your request.")
        except requests.exceptions.ReadTimeout:
            st.write("Bot: The request timed out. Please try again later.")
        except requests.exceptions.ConnectionError:
            st.write("Bot: Failed to connect to the server. Please ensure the server is running.")

display_conversation()
