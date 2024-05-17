import base64
import requests
import streamlit as st

def chat_flow():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        image = st.session_state.get('image', '')
        st.session_state.messages.append({"role": "user", "content": prompt, "images": [image]})
        body = {
            'model': 'llava-phi3',
            'messages': [{
                'role': m['role'],
                'content': m['content'],
                'images': m['images']
            } for m in st.session_state.messages],
            'stream': False
        }
        response = requests.post('http://localhost:11434/api/chat', json=body)
        data = response.json()
        llm_response = data['message']['content']
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(llm_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": llm_response, "images": []})

st.title("llava-phi3")

uploaded_file = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png', 'tiff'])
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    encoded_image = base64.b64encode(bytes_data)
    image = encoded_image.decode('utf-8')
    st.session_state.image = image

chat_flow()