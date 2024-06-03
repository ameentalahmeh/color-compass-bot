# 🎨 Color Compass Bot

Enhance visual experiences for colorblind individuals.

## Overview

Color Compass is a chatbot designed to assist individuals with color blindness by enhancing their perception of colors in both photos and text. Leveraging the advanced capabilities of the ChatGPT-4 model, Color Compass aims to make visual information more accessible and comprehensible.

### Features

- **Text and Image Processing:** Analyzes both textual and visual content to improve color distinction.
- **OpenAI GPT-4 Integration:** Utilizes the powerful GPT-4 model for advanced color interpretation and assistance.
- **Accessible Color Information:** Provides detailed and user-friendly color information to aid in color differentiation.

### Get Your OpenAI API Key

To access the full capabilities of Color Compass Bot, you'll need your own OpenAI API key. Here's how to get started:

1. Navigate to [OpenAI API Keys](https://platform.openai.com/account/api-keys).
   
2. Click on the `+ Create new secret key` button.
   
3. Provide an identifier name (optional) and click `Create secret key`.

## Getting Started

### Requirements

- Python 3.8+
- Virtual environment (venv)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ameentalahmeh/color-compass-bot.git
   ```

   ```
   cd color-compass-bot
   ```

2. **Set up the virtual environment:**
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a .env file:**
   
   Create a file named `.env` in the root directory project (`color-compass-bot`) and add your OpenAI API key:
   
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the application:**
   
   ```bash
   streamlit run app.py
   ```

## Team Members:
 - [Zahraa Shabana](https://github.com/ZahraaShabana)
 - [Amin Talahmeh](https://github.com/ameentalahmeh)
 - [Momin Arafa](https://github.com/Momen-G-Ar)
