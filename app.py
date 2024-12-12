







# import os
# import io
# import streamlit as st
# import logging
# import PyPDF2
# from dotenv import load_dotenv
# from typing import Optional, List

# # Fireworks imports
# from fireworks.client import Fireworks

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class PodcastGenerator:
#     def __init__(self, api_key: Optional[str] = None):
#         """
#         Initialize PodcastGenerator with Fireworks client.
        
#         Args:
#             api_key: Optional API key for Fireworks. 
#                      If not provided, will use environment variable.
#         """
#         # Load environment variables
#         load_dotenv()
        
#         # Validate and set API key
#         self.api_key = api_key or os.getenv('FIREWORKS_API_KEY')
#         self._validate_environment()
        
#         # Initialize Fireworks client
#         self.client = Fireworks(api_key=self.api_key)

#     def _validate_environment(self) -> None:
#         """Validate Fireworks API key is available."""
#         if not self.api_key:
#             raise EnvironmentError(
#                 "Fireworks API key not found. Please set FIREWORKS_API_KEY in .env file."
#             )

#     def extract_pdf_text(self, pdf_file) -> str:
#         """
#         Safely extract text from uploaded PDF using PyPDF2.
        
#         Args:
#             pdf_file: Uploaded PDF file object
        
#         Returns:
#             Extracted text from PDF
#         """
#         if not pdf_file:
#             raise ValueError("No PDF file provided")
        
#         try:
#             # Create a safe copy of the file in memory
#             pdf_bytes = pdf_file.read()
#             pdf_io = io.BytesIO(pdf_bytes)
            
#             pdf_reader = PyPDF2.PdfReader(pdf_io)
            
#             # Extract text with error handling
#             text_chunks = []
#             for page_num, page in enumerate(pdf_reader.pages):
#                 try:
#                     text_chunks.append(page.extract_text())
#                 except Exception as e:
#                     logger.warning(f"Error extracting text from page {page_num}: {str(e)}")
#                     continue
            
#             combined_text = " ".join(text_chunks)
            
#             # Implement reasonable length limit
#             MAX_LENGTH = 50000  # Reduced for better processing
#             if len(combined_text) > MAX_LENGTH:
#                 logger.warning(f"Text truncated to {MAX_LENGTH} characters")
#                 return combined_text[:MAX_LENGTH]
            
#             return combined_text
        
#         except Exception as e:
#             logger.error(f"PDF extraction error: {str(e)}")
#             raise

#     def generate_podcast_script(
#         self,
#         text: str,
#         topic: Optional[str] = None,
#         tone: str = "conversational",
#         length: str = "medium",
#         language: str = "English"
#     ) -> str:
#         """
#         Generate a podcast script using Fireworks AI.
        
#         Args:
#             text: Source text for podcast
#             topic: Optional specific topic focus
#             tone: Desired script tone
#             length: Desired podcast length
#             language: Script language
        
#         Returns:
#             Generated podcast script
#         """
#         if not text:
#             raise ValueError("No input text provided")
        
#         # Sanitize inputs
#         tone = tone.lower()
#         length = length.lower()
        
#         # Construct detailed prompt
#         prompt = self._construct_prompt(text, topic, tone, length, language)
        
#         try:
#             # Generate script using Fireworks client
#             response = self.client.chat.completions.create(
#                 model="accounts/fireworks/models/llama-v3p1-8b-instruct",  # Switched to a more reliable model
#                 messages=[
#                     {"role": "system", "content": "You are a professional podcast script writer."},
#                     {"role": "user", "content": prompt}
#                 ],
#                 max_tokens=2048,
#                 temperature=0.7,
#                 top_p=0.95
#             )
            
#             return response.choices[0].message.content
        
#         except Exception as e:
#             logger.error(f"Script generation error: {str(e)}")
#             raise

#     def _construct_prompt(self, text, topic, tone, length, language) -> str:
#         """
#         Construct a detailed prompt for script generation.
        
#         Args:
#             text: Source text preview
#             topic: Optional topic
#             tone: Desired tone
#             length: Podcast length
#             language: Script language
        
#         Returns:
#             Formatted prompt for AI
#         """
#         # Safely truncate text
#         text_preview = text[:3000]  # Reduced preview length
        
#         return f"""Generate a professional podcast script based on the following parameters:

# Input Context: {text_preview}
# Specific Topic: {topic or "General Discussion"}
# Desired Tone: {tone}
# Podcast Length: {length}
# Language: {language}

# Script Structure Requirements:
# 1. Engaging Introduction
#    - Create a captivating opening hook
#    - Briefly introduce the core topic
#    - Set context for listeners

# 2. Main Content Segments
#    - Divide key insights into clear, digestible sections
#    - Use smooth, natural transitions
#    - Provide in-depth analysis and storytelling
#    - Maintain listener engagement

# 3. Compelling Conclusion
#    - Summarize primary takeaways
#    - Offer a thought-provoking final statement
#    - Include optional call-to-action

# Scripting Guidelines:
# - Use natural, conversational language
# - Incorporate varied sentence structures
# - Include occasional verbal pauses or ad-libs
# - Maintain consistent {tone} tone
# - Ensure accessibility and clarity
# """

# def create_streamlit_ui():
#     """
#     Create Streamlit user interface for podcast generator.
    
#     Returns:
#         Dictionary of user-selected controls
#     """
#     st.set_page_config(page_title="PDF to Podcast Generator", page_icon="🎙️")
    
#     st.title("🎙️ PDF to Podcast Generator")
    
#     # Security and usage notice
#     st.info("""
#     📘 How to Use:
#     - Upload PDF documents
#     - Customize podcast parameters
#     - Click 'Generate Podcast' 
#     """)
    
#     # Sidebar controls
#     st.sidebar.header("Podcast Configuration")
    
#     controls = {
#         'files': st.sidebar.file_uploader(
#             "Upload PDF(s)",
#             type=['pdf'],
#             accept_multiple_files=True
#         ),
#         'topic': st.sidebar.text_input("Specific Topic/Focus (Optional)"),
#         'tone': st.sidebar.selectbox(
#             "Podcast Tone",
#             ["Conversational", "Academic", "Casual", "Professional"]
#         ),
#         'length': st.sidebar.selectbox(
#             "Podcast Length",
#             ["Short (5-10 min)", "Medium (10-20 min)", "Long (20-30 min)"]
#         ),
#         'language': st.sidebar.selectbox(
#             "Language",
#             ["English", "Spanish", "French", "German", "Chinese"]
#         )
#     }
    
#     return controls

# def main():
#     """
#     Main application logic with comprehensive error handling.
#     """
#     try:
#         # Create UI and get user controls
#         controls = create_streamlit_ui()
        
#         # Generate podcast button
#         if st.sidebar.button("Generate Podcast"):
#             try:
#                 # Initialize PodcastGenerator
#                 generator = PodcastGenerator()
                
#                 # Process PDF files
#                 if controls['files']:
#                     combined_text = ""
#                     for pdf_file in controls['files']:
#                         try:
#                             text = generator.extract_pdf_text(pdf_file)
#                             combined_text += text + "\n\n"
#                         except Exception as e:
#                             st.error(f"Error processing {pdf_file.name}: {str(e)}")
#                             continue
                    
#                     # Generate podcast script
#                     if combined_text.strip():
#                         try:
#                             podcast_script = generator.generate_podcast_script(
#                                 text=combined_text,
#                                 topic=controls['topic'],
#                                 tone=controls['tone'],
#                                 length=controls['length'],
#                                 language=controls['language']
#                             )
                            
#                             # Display generated script
#                             st.subheader("📜 Generated Podcast Script")
#                             st.text_area("Podcast Script", podcast_script, height=400)
                        
#                         except Exception as e:
#                             st.error(f"Script generation failed: {str(e)}")
#                     else:
#                         st.error("No valid text extracted from PDFs")
                
#                 else:
#                     st.warning("Please upload a PDF file")
            
#             except Exception as e:
#                 st.error(f"An unexpected error occurred: {str(e)}")
#                 logger.error(f"Application error: {str(e)}", exc_info=True)
    
#     except Exception as e:
#         st.error("Critical application error. Please contact support.")
#         logger.critical(f"Critical error: {str(e)}", exc_info=True)

# if __name__ == "__main__":
#     main()





import os
import io
import streamlit as st
import logging
import PyPDF2
from dotenv import load_dotenv
from typing import Optional, List

# Fireworks imports
from fireworks.client import Fireworks

# Text-to-Speech imports
import pyttsx3  # For local TTS
from gtts import gTTS  # For cloud-based TTS
import random

# Audio processing
import numpy as np
import scipy.io.wavfile as wavfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PodcastGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize PodcastGenerator with Fireworks client and TTS engine.
        
        Args:
            api_key: Optional API key for Fireworks. 
                     If not provided, will use environment variable.
        """
        # Load environment variables
        load_dotenv()
        
        # Validate and set API key
        self.api_key = api_key or os.getenv('FIREWORKS_API_KEY')
        self._validate_environment()
        
        # Initialize Fireworks client
        self.client = Fireworks(api_key=self.api_key)
        
        # Initialize local TTS engine
        self.tts_engine = pyttsx3.init()
        
        # Voice configurations
        self.voices = {
            'host': {
                'local': {
                    'name': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0',
                    'rate': 170,
                    'volume': 0.8
                },
                'cloud': 'en-us-Standard-C'  # Google Cloud Voice
            },
            'guest': {
                'local': {
                    'name': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_DAVID_11.0',
                    'rate': 150,
                    'volume': 0.7
                },
                'cloud': 'en-us-Standard-B'  # Google Cloud Voice
            }
        }

    def _validate_environment(self) -> None:
        """Validate Fireworks API key is available."""
        if not self.api_key:
            raise EnvironmentError(
                "Fireworks API key not found. Please set FIREWORKS_API_KEY in .env file."
            )

    def extract_pdf_text(self, pdf_file) -> str:
        """
        Safely extract text from uploaded PDF using PyPDF2.
        
        Args:
            pdf_file: Uploaded PDF file object
        
        Returns:
            Extracted text from PDF
        """
        if not pdf_file:
            raise ValueError("No PDF file provided")
        
        try:
            # Create a safe copy of the file in memory
            pdf_bytes = pdf_file.read()
            pdf_io = io.BytesIO(pdf_bytes)
            
            pdf_reader = PyPDF2.PdfReader(pdf_io)
            
            # Extract text with error handling
            text_chunks = []
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text_chunks.append(page.extract_text())
                except Exception as e:
                    logger.warning(f"Error extracting text from page {page_num}: {str(e)}")
                    continue
            
            combined_text = " ".join(text_chunks)
            
            # Implement reasonable length limit
            MAX_LENGTH = 50000  # Reduced for better processing
            if len(combined_text) > MAX_LENGTH:
                logger.warning(f"Text truncated to {MAX_LENGTH} characters")
                return combined_text[:MAX_LENGTH]
            
            return combined_text
        
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            raise

    def generate_podcast_script(
        self,
        text: str,
        topic: Optional[str] = None,
        tone: str = "conversational",
        length: str = "medium",
        language: str = "English"
    ) -> str:
        """
        Generate a podcast script using Fireworks AI.
        
        Args:
            text: Source text for podcast
            topic: Optional specific topic focus
            tone: Desired script tone
            length: Desired podcast length
            language: Script language
        
        Returns:
            Generated podcast script
        """
        if not text:
            raise ValueError("No input text provided")
        
        # Sanitize inputs
        tone = tone.lower()
        length = length.lower()
        
        # Construct detailed prompt
        prompt = self._construct_prompt(text, topic, tone, length, language)
        
        try:
            # Generate script using Fireworks client
            response = self.client.chat.completions.create(
                model="accounts/fireworks/models/llama-v3p1-8b-instruct",
                messages=[
                    {"role": "system", "content": "You are a professional podcast script writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2048,
                temperature=0.7,
                top_p=0.95
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Script generation error: {str(e)}")
            raise

    def _construct_prompt(self, text, topic, tone, length, language) -> str:
        """
        Construct a detailed prompt for script generation.
        
        Args:
            text: Source text preview
            topic: Optional topic
            tone: Desired tone
            length: Podcast length
            language: Script language
        
        Returns:
            Formatted prompt for AI
        """
        # Safely truncate text
        text_preview = text[:3000]  # Reduced preview length
        
        return f"""Generate a professional podcast script based on the following parameters:

Input Context: {text_preview}
Specific Topic: {topic or "General Discussion"}
Desired Tone: {tone}
Podcast Length: {length}
Language: {language}

Script Structure Requirements:
1. Engaging Introduction
   - Create a captivating opening hook
   - Briefly introduce the core topic
   - Set context for listeners

2. Main Content Segments
   - Divide key insights into clear, digestible sections
   - Use smooth, natural transitions
   - Provide in-depth analysis and storytelling
   - Maintain listener engagement

3. Compelling Conclusion
   - Summarize primary takeaways
   - Offer a thought-provoking final statement
   - Include optional call-to-action

Scripting Guidelines:
- Use natural, conversational language
- Incorporate varied sentence structures
- Include occasional verbal pauses or ad-libs
- Maintain consistent {tone} tone
- Ensure accessibility and clarity
"""

    def generate_audio_from_script(self, script: str, output_dir: str = 'podcast_audio') -> List[str]:
        """
        Generate audio files for podcast script with multiple voices.
        
        Args:
            script: Full podcast script
            output_dir: Directory to save audio files
        
        Returns:
            List of generated audio file paths
        """
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Split script into segments
        segments = self._split_script_into_segments(script)
        
        audio_files = []
        
        # Alternate between host and guest voices
        for i, segment in enumerate(segments):
            voice_type = 'host' if i % 2 == 0 else 'guest'
            
            # Try local TTS first, fallback to cloud
            try:
                audio_path = self._generate_local_tts(
                    segment, 
                    os.path.join(output_dir, f'segment_{i}_{voice_type}.wav'),
                    voice_type
                )
            except Exception as local_error:
                logger.warning(f"Local TTS failed: {local_error}. Trying cloud TTS.")
                try:
                    audio_path = self._generate_cloud_tts(
                        segment, 
                        os.path.join(output_dir, f'segment_{i}_{voice_type}.mp3'),
                        self.voices[voice_type]['cloud']
                    )
                except Exception as cloud_error:
                    logger.error(f"Cloud TTS failed: {cloud_error}")
                    continue
            
            audio_files.append(audio_path)
        
        return audio_files

    def _split_script_into_segments(self, script: str, max_segment_length: int = 500) -> List[str]:
        """
        Split script into segments for voice generation.
        
        Args:
            script: Full podcast script
            max_segment_length: Maximum length of each segment
        
        Returns:
            List of script segments
        """
        # Simple splitting logic
        sentences = script.split('.')
        segments = []
        current_segment = ""
        
        for sentence in sentences:
            if len(current_segment) + len(sentence) > max_segment_length:
                segments.append(current_segment.strip() + '.')
                current_segment = sentence
            else:
                current_segment += sentence + '.'
        
        if current_segment:
            segments.append(current_segment.strip())
        
        return segments

    def _generate_local_tts(self, text: str, output_path: str, voice_type: str = 'host') -> str:
        """
        Generate audio using local TTS engine.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            voice_type: Type of voice (host or guest)
        
        Returns:
            Path to generated audio file
        """
        # Configure voice
        voices = self.tts_engine.getProperty('voices')
        target_voice = next(
            (v for v in voices if v.id == self.voices[voice_type]['local']['name']), 
            None
        )
        
        if target_voice:
            self.tts_engine.setProperty('voice', target_voice.id)
        
        # Set rate and volume
        self.tts_engine.setProperty('rate', self.voices[voice_type]['local']['rate'])
        self.tts_engine.setProperty('volume', self.voices[voice_type]['local']['volume'])
        
        # Save audio
        self.tts_engine.save_to_file(text, output_path)
        self.tts_engine.runAndWait()
        
        return output_path

    def _generate_cloud_tts(self, text: str, output_path: str, voice_name: str) -> str:
        """
        Generate audio using Google Text-to-Speech.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            voice_name: Specific cloud voice to use
        
        Returns:
            Path to generated audio file
        """
        # Use gTTS for cloud-based TTS
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
        
        return output_path

def create_streamlit_ui():
    """
    Create Streamlit user interface for podcast generator.
    
    Returns:
        Dictionary of user-selected controls
    """
    st.set_page_config(page_title="PDF to Podcast Generator", page_icon="🎙️")
    
    st.title("🎙️ PDF to Podcast Generator")
    
    # Security and usage notice
    st.info("""
    📘 How to Use:
    - Upload PDF documents
    - Customize podcast parameters
    - Click 'Generate Podcast' 
    - Audio will be generated with multiple voices
    """)
    
    # Sidebar controls
    st.sidebar.header("Podcast Configuration")
    
    controls = {
        'files': st.sidebar.file_uploader(
            "Upload PDF(s)",
            type=['pdf'],
            accept_multiple_files=True
        ),
        'topic': st.sidebar.text_input("Specific Topic/Focus (Optional)"),
        'tone': st.sidebar.selectbox(
            "Podcast Tone",
            ["Conversational", "Academic", "Casual", "Professional"]
        ),
        'length': st.sidebar.selectbox(
            "Podcast Length",
            ["Short (5-10 min)", "Medium (10-20 min)", "Long (20-30 min)"]
        ),
        'language': st.sidebar.selectbox(
            "Language",
            ["English", "Spanish", "French", "German", "Chinese"]
        ),
        'generate_audio': st.sidebar.checkbox("Generate Audio", value=True)
    }
    
    return controls

def main():
    """
    Main application logic with comprehensive error handling.
    """
    try:
        # Create UI and get user controls
        controls = create_streamlit_ui()
        
        # Generate podcast button
        if st.sidebar.button("Generate Podcast"):
            try:
                # Initialize PodcastGenerator
                generator = PodcastGenerator()
                
                # Process PDF files
                if controls['files']:
                    combined_text = ""
                    for pdf_file in controls['files']:
                        try:
                            text = generator.extract_pdf_text(pdf_file)
                            combined_text += text + "\n\n"
                        except Exception as e:
                            st.error(f"Error processing {pdf_file.name}: {str(e)}")
                            continue
                    
                    # Generate podcast script
                    if combined_text.strip():
                        try:
                            podcast_script = generator.generate_podcast_script(
                                text=combined_text,
                                topic=controls['topic'],
                                tone=controls['tone'],
                                length=controls['length'],
                                language=controls['language']
                            )
                            
                            # Display generated script
                            st.subheader("📜 Generated Podcast Script")
                            st.text_area("Podcast Script", podcast_script, height=400)
                            
                            # Generate audio if checkbox is checked
                            if controls['generate_audio']:
                                st.subheader("🎧 Podcast Audio")
                                audio_files = generator.generate_audio_from_script(podcast_script)
                                
                                # Display audio files
                                for i, audio_file in enumerate(audio_files, 1):
                                    st.audio(audio_file, format='audio/wav', start_time=0)
                        
                        except Exception as e:
                            st.error(f"Script generation failed: {str(e)}")
                    else:
                        st.error("No valid text extracted from PDFs")
                
                else:
                    st.warning("Please upload a PDF file")
            
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
                logger.error(f"Application error: {str(e)}", exc_info=True)
    
    except Exception as e:
        st.error("Critical application error. Please contact support.")
        logger.critical(f"Critical error: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()