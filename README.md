# PDF to Podcast Generator

This project is a Streamlit application that converts PDF documents into engaging podcasts using AI. It leverages the Fireworks AI API to generate high-quality podcast scripts from the text extracted from your PDFs and then uses Text-to-Speech (TTS) to create an audio version with distinct voices for a host and a guest.

## Features

-   **PDF to Text**: Upload any PDF file and automatically extract its text content.
-   **AI-Powered Script Generation**: Uses Fireworks AI to generate a natural and conversational podcast script from the extracted text.
-   **Dual-Voice Synthesis**: Creates a dynamic listening experience by using different voices for the podcast host and guest.
-   **Local and Cloud TTS**: Supports both local `pyttsx3` and cloud-based `gTTS` for audio generation.
-   **Interactive UI**: A simple and intuitive web interface built with Streamlit to manage the entire process.
-   **Direct Playback**: Listen to the generated podcast audio directly in your browser.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.8 or higher
-   A Fireworks AI API key

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/KimavathBalajiNayak210/pdf_to_Podcast_generater_with_voice.git
    cd pdf_to_Podcast_generater_with_voice
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    python -m venv my_env
    source my_env/bin/activate  # On Windows, use `my_env\\Scripts\\activate`
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    -   Create a file named `.env` in the root directory of the project.
    -   Add your Fireworks AI API key to the `.env` file as follows:
        ```
        FIREWORKS_API_KEY="YOUR_API_KEY_HERE"
        ```

### Usage

1.  **Run the Streamlit application:**
    ```sh
    streamlit run app.py
    ```

2.  **Open your web browser** and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).

3.  **Upload a PDF file** using the file uploader.

4.  **Click the "Generate Podcast" button** to start the conversion process.

5.  Once the process is complete, the podcast audio segments will appear, and you can play them directly on the page.

## Dependencies

The project relies on the following Python libraries:

-   `streamlit`
-   `transformers`
-   `python-dotenv`
-   `huggingface_hub`
-   `torch`
-   `PyPDF2`
-   `requests`
-   `fireworks-ai`
-   `pyttsx3`
-   `gtts`
-   `scipy`

All dependencies are listed in the `requirements.txt` file.
