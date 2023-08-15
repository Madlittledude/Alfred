import streamlit as st
import openai
import os
# Set up the page layout
st.set_page_config(page_title="Alfred", page_icon="batman_logo.png", layout='wide')

# Function to display chat messages
def display_chat_message(role, content,avatar):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

def display_intro():
    st.title('Welcome, Master Kevin')
    st.write(':heart: Alfred')

keven = "https://raw.githubusercontent.com/Madlittledude/Alfred/main/keven_cape.png"
alfred = "https://raw.githubusercontent.com/Madlittledude/Alfred/main/alfred_flipped.png"
def display_chat_interface():

    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        avatar = alfred if message["role"] == "assistant" else keven
        display_chat_message(message["role"], message["content"],avatar)

    # User input
    prompt = st.chat_input()
    if prompt:
        # Set the state to indicate the user has sent their first message
        st.session_state.first_message_sent = True
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt,keven)

        with st.chat_message("assistant",avatar=alfred):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=([
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]),
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# Initialization logic
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": ("You are Alfred, Master Keven's generative AI butler. Serve him as if he were the Batman. So give him whatever he wants and ask him questions to clarify how he would like to be served best. If he is working through an idea, break his problem into parts and work through each one with him")
                    }]



if "first_message_sent" not in st.session_state:
    st.session_state.first_message_sent = False

openai.api_key = os.environ["OPENAI_API_KEY"]

# Display logic
if not st.session_state.first_message_sent:
    display_intro()

display_chat_interface()





