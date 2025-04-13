# import gradio as gr
# from deep_translator import GoogleTranslator
# import datetime
# import pickle
# import os
# from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# # Load BlenderBot model
# model_name = "facebook/blenderbot-400M-distill"
# tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
# model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

# # Translation
# def to_english(text):
#     try:
#         return GoogleTranslator(source='auto', target='en').translate(text)
#     except Exception as e:
#         return f"(Translation Error to English: {e})"

# def from_english(text, target_lang):
#     if target_lang == "English":
#         return text
#     try:
#         return GoogleTranslator(source='en', target=target_lang).translate(text)
#     except Exception as e:
#         return f"(Translation Error to {target_lang}: {e})"

# # Model
# def ask_blenderbot(prompt):
#     try:
#         inputs = tokenizer(prompt, return_tensors="pt")
#         reply_ids = model.generate(**inputs)
#         reply = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
#         return reply
#     except Exception as e:
#         return f"(Model Error: {e})"

# # Chat logic
# def chatbot_interface(message, history, lang):
#     user_input_en = to_english(message)
#     response_en = ask_blenderbot(user_input_en)
#     response_translated = from_english(response_en, lang)
#     history.append({"role": "user", "content": message})
#     history.append({"role": "assistant", "content": response_translated})
#     return history, history

# # Save .pkl
# def save_chat_history(history):
#     try:
#         with open("chat_history.pkl", "wb") as f:
#             pickle.dump(history, f)
#         return "✅ Chat history saved to chat_history.pkl"
#     except Exception as e:
#         return f"❌ Save Error: {e}"

# # Load history if exists
# def load_chat_history():
#     if os.path.exists("chat_history.pkl"):
#         with open("chat_history.pkl", "rb") as f:
#             return pickle.load(f)
#     return []

# def clear_chat():
#     return [], []

# # UI with inline option
# with gr.Blocks(theme=gr.themes.Soft()) as demo:
#     gr.Markdown("## ⚖️ JusticePal - Your Digital Safety Legal Hub")

#     chatbot = gr.Chatbot(label="Your Chat", height=400, type="messages")
#     state = gr.State(load_chat_history())

#     lang = gr.Dropdown(
#         choices=[
#             "English", "Hindi", "Marathi", "Tamil",
#             "Telugu", "Gujarati", "Bengali", "Punjabi", "Urdu"
#         ],
#         value="English",
#         label="Choose Language"
#     )

#     with gr.Row():
#         txt = gr.Textbox(show_label=False, placeholder="Type your message here…", scale=4)
#         send_btn = gr.Button("Send", scale=1)

#     with gr.Row(equal_height=True):
#         save_btn = gr.Button("💾 Save Chat History (PKL)", scale=1, size="sm", variant="primary")
#         clear_btn = gr.Button("🧹 Clear Chat", scale=1, size="sm", variant="stop")

    
#     send_btn.click(fn=chatbot_interface, inputs=[txt, state, lang], outputs=[chatbot, state])
#     txt.submit(fn=chatbot_interface, inputs=[txt, state, lang], outputs=[chatbot, state])
#     save_btn.click(fn=save_chat_history, inputs=[state], outputs=state)
#     clear_btn.click(fn=clear_chat, outputs=[chatbot, state])

# # This line only works inside Jupyter / Colab:
# demo.launch(share=True)

import gradio as gr
from deep_translator import GoogleTranslator
import pickle
import os
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from fpdf import FPDF  # For PDF saving functionality

# Load BlenderBot model
model_name = "facebook/blenderbot-400M-distill"
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

# Translation functions
def to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        return f"(Translation Error to English: {e})"

def from_english(text, target_lang):
    if target_lang == "English":
        return text
    try:
        return GoogleTranslator(source='en', target=target_lang).translate(text)
    except Exception as e:
        return f"(Translation Error to {target_lang}: {e})"

# Model response function
def ask_blenderbot(prompt):
    try:
        inputs = tokenizer(prompt, return_tensors="pt")
        reply_ids = model.generate(**inputs)
        reply = tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
        return reply
    except Exception as e:
        return f"(Model Error: {e})"

# Chat logic to handle user inputs and generate responses
def chatbot_interface(message, history, lang):
    # Make sure history is a list, initializing it if necessary
    if not isinstance(history, list):
        history = []

    # Convert user message to English, get model response, then translate to target language
    user_input_en = to_english(message)
    response_en = ask_blenderbot(user_input_en)
    response_translated = from_english(response_en, lang)

    # Append the current conversation (user message + assistant response) to history
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response_translated})

    return history, history  # Returning updated history

# Save chat history as .pkl file
def save_chat_history(history):
    try:
        with open("chat_history.pkl", "wb") as f:
            pickle.dump(history, f)
        return "✅ Chat history saved to chat_history.pkl"
    except Exception as e:
        return f"❌ Save Error: {e}"

# Load chat history if it exists
def load_chat_history():
    if os.path.exists("chat_history.pkl"):
        with open("chat_history.pkl", "rb") as f:
            return pickle.load(f)
    return []

# Function to save chat history as a PDF
def save_chat_history_as_pdf(history):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add messages to PDF
        for msg in history:
            role = msg["role"].capitalize()
            content = msg["content"]
            pdf.multi_cell(0, 10, f"{role}: {content}")

        pdf.output("chat_history.pdf")
        return "✅ Chat history saved to chat_history.pdf"
    except Exception as e:
        return f"❌ Save Error (PDF): {e}"

# Function to clear chat history
def clear_chat():
    return [], []  # Reset the chat history

# UI with inline option and buttons
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## ⚖️ JusticePal - Your Digital Safety Legal Hub")

    chatbot = gr.Chatbot(label="Your Chat", height=400, type="messages")
    state = gr.State(load_chat_history())  # Initialize with saved chat history or empty list

    # Language selection dropdown
    lang = gr.Dropdown(
        choices=[
            "English", "Hindi", "Marathi", "Tamil",
            "Telugu", "Gujarati", "Bengali", "Punjabi", "Urdu"
        ],
        value="English",
        label="Choose Language"
    )

    # Input textbox and send button
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Type your message here…", scale=4)
        send_btn = gr.Button("Send", scale=1)

    # Control buttons for saving and clearing
    with gr.Row(equal_height=True):
        save_btn = gr.Button("💾 Save Chat History (PKL)", scale=1, size="sm", variant="primary")
        clear_btn = gr.Button("🧹 Clear Chat", scale=1, size="sm", variant="stop")
        save_pdf_btn = gr.Button("📄 Save Chat as PDF", scale=1, size="sm", variant="primary")

    # Button actions
    send_btn.click(fn=chatbot_interface, inputs=[txt, state, lang], outputs=[chatbot, state])
    txt.submit(fn=chatbot_interface, inputs=[txt, state, lang], outputs=[chatbot, state])
    save_btn.click(fn=save_chat_history, inputs=[state], outputs=state)
    save_pdf_btn.click(fn=save_chat_history_as_pdf, inputs=[state], outputs=state)
    clear_btn.click(fn=clear_chat, outputs=[chatbot, state])

# Launching the Gradio app
demo.launch(share=True)

