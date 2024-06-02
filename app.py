import streamlit as st
from openai import OpenAI
import dotenv
import os
from PIL import Image
import base64
from io import BytesIO

dotenv.load_dotenv()

with open('./css/style.css') as f:
    css = f.read()

# Query and stream the response from the LLM
def stream_llm_response(client, model_params):
    response_message = ""

    # Add instruction for optimizing images for colorblind individuals
    st.session_state.messages.append(
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": "Please optimize any provided images for colorblind individuals by adjusting the colors to enhance visibility and distinguishability. Then, return them in the response. Alternatively, if the response includes images, ensure they have suitable visibility for colorblind people."
                }
            ],
            "display": False
        }
    )

    for chunk in client.chat.completions.create(
        model=model_params["model"],
        messages=st.session_state.messages,
        temperature=model_params.get("temperature", 0.3),
        max_tokens=4096,
        stream=True,
    ):
        response_message += chunk.choices[0].delta.content or ""
        yield chunk.choices[0].delta.content or ""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": response_message,
                }
            ],
        }
    )

# Convert file to base64
def get_image_base64(image_raw):
    buffered = BytesIO()
    image_raw.save(buffered, format=image_raw.format)
    img_byte = buffered.getvalue()

    return base64.b64encode(img_byte).decode("utf-8")

# Add image to messages
def add_image_to_messages():
    if st.session_state.uploaded_img:
        for img_file in st.session_state.uploaded_img:
            img_type = img_file.type if img_file else "image/jpeg"
            raw_img = Image.open(img_file)
            img = get_image_base64(raw_img)
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{img_type};base64,{img}"
                            },
                        }
                    ],
                }
            )

# Reset messages
def reset_conversation():
    if "messages" in st.session_state and len(st.session_state.messages) > 0:
        st.session_state.pop("messages", None)

def main():

    # --- Page Config ---
    st.set_page_config(
        page_title="Color Compass",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    # --- Style ---
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

    # --- Header ---
    st.markdown(
        """<h1 style="text-align: center; color: #6ca395; margin-top: -35px;">🤖 <i>Color Compass</i> 💬</h1>""",
        unsafe_allow_html=True
    )

    # --- Side Bar ---
    with st.sidebar:
        # API Key Input
        default_openai_api_key = (
            os.getenv("OPENAI_API_KEY")
            if os.getenv("OPENAI_API_KEY") is not None
            else ""
        )  # only for development environment, otherwise it should return None
        with st.expander("🔐 OpenAI API Key"):
            openai_api_key = st.text_input(
                "Introduce your OpenAI API Key (https://platform.openai.com/)",
                value=default_openai_api_key,
                type="password",
            )

        st.markdown("---")

        # About
        st.markdown("## About")
        st.markdown("This chatbot is designed to enhance visual experiences by providing assistance and information related to color perception and accessibility.")
        st.markdown("### Features")
        st.markdown("- Ask questions related to color theory and perception.")
        st.markdown("- Upload images for analysis and advice.")
        st.markdown("- Receive recommendations for optimizing visuals for colorblind individuals.")
        st.markdown("### How it Works")
        st.markdown("Simply type your question or upload an image, and the chatbot will provide helpful insights and guidance.")
        st.markdown("### Supported Formats")
        st.markdown("- Images: PNG, JPG, JPEG")

    # --- Main Content ---
    # Checking if the user has introduced the OpenAI API Key, if not, a warning is displayed
    if openai_api_key == "" or openai_api_key is None or "sk-" not in openai_api_key:
        st.write("#")
        st.warning(
            "⬅️ Please introduce your OpenAI API Key (make sure to have funds) to continue..."
        )

    else:
        client = OpenAI(api_key=openai_api_key)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Displaying the previous messages if there are any
        for message in st.session_state.messages:
            if message.get("display", True):
                with st.chat_message(message["role"]):
                    for content in message["content"]:
                        if content["type"] == "text":
                            st.write(content["text"])
                        elif content["type"] == "image_url":
                            st.image(content["image_url"]["url"])
        
        # File uploader
        st.file_uploader(
            "Upload an image",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            key="uploaded_img",
            on_change=add_image_to_messages,
            label_visibility="collapsed"
        )

        # Prompt
        prompt = st.chat_input("Hi! Ask me anything...")
        if prompt:
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        }
                    ],
                }
            )

            # Displaying the new messages
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                st.write_stream(stream_llm_response(client, {"model": "gpt-4o-2024-05-13"}))

if __name__ == "__main__":
    main()
