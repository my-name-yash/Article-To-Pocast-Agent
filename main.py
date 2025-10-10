import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.eleven_labs import ElevenLabsTools
from agno.tools.firecrawl import FirecrawlTools
from agno.agent import RunOutput
from agno.utils.audio import write_audio_to_file
from agno.utils.log import logger
import streamlit as st
import uuid

# Load all environment variables from the .env file
load_dotenv()

st.set_page_config(page_title="Ai Podcaster", page_icon="🎙️")
st.title("Blog Post to Podcast")

# The sidebar is no longer used for API keys
st.sidebar.header("About")
st.sidebar.info(
    "This app uses AI to scrape a webpage, summarize its content, and generate an audio podcast."
)

# Check that the API keys were loaded from the .env file
keys_loaded = all(
    [
        os.getenv("GEMINI_API_KEY"),
        os.getenv("ELEVEN_LABS_API_KEY"),
        os.getenv("FIRECRAWL_API_KEY"),
    ]
)

url = st.text_input("Enter the URL of the site:", "")
gen_btn = st.button("Generate Podcast", disabled=not keys_loaded)

if not keys_loaded:
    st.warning(
        "API keys not found. Please create a .env file and add your GEMINI_API_KEY, ELEVEN_LABS_API_KEY, and FIRECRAWL_API_KEY."
    )

if gen_btn:
    if url.strip() == "":
        st.error("Please enter a valid URL.")
    else:
        # No need to set os.environ here; load_dotenv() already did it.
        with st.spinner("Generating podcast..."):
            try:
                blog_to_podcast_agent = Agent(
                    name="Blog to Podcast Agent",
                    model=Gemini(
                        id="gemini-2.5-flash",  # Note: Changed from 2.0 to 1.5 as 2.0 is not a public model ID
                        search=False,
                        grounding=False,
                        temperature=0.7,
                    ),
                    tools=[
                        ElevenLabsTools(
                            voice_id="EXAVITQu4vr4xnSDxMaL",
                            model_id="eleven_multilingual_v2",
                            target_directory="podcasts",
                        ),
                        FirecrawlTools(enable_scrape=True),
                    ],
                    description="You are an ai agent that generates audio using the ElevenLabs API",
                    instructions=[
                        "Given a URL, you will scrape the content of the page and generate a podcast episode in mp3 format.",
                        "1. Use the FireCrawl tool to scrape the content of the page.",
                        "2. Summarize the content into a script that is NO MORE THAN 2000 characters long, for a podcast episode.",
                        "3. Ensure the script is engaging and suitable for an audio format. Do not include any mentions of images or visual content. Make it sound natural and conversational.",
                        "4. Use the ElevenLabs tool to generate an audio file from the script.",
                        "Ensure the summary is within the 2000 character limit to avoid ElevenLabs API limitations.",
                    ],
                    markdown=True,
                    debug_mode=True,
                )

                podcast: RunOutput = blog_to_podcast_agent.run(
                    f"Generate a podcast episode from this URL: {url}"
                )

                save_dir = "podcasts"
                os.makedirs(save_dir, exist_ok=True)

                if podcast.audio and len(podcast.audio) > 0:
                    filename = f"{save_dir}/podcast_{str(uuid.uuid4())[:8]}.wav"
                    write_audio_to_file(
                        audio=podcast.audio[0].base64_audio, filename=filename
                    )

                    st.success("Podcast generated successfully!")
                    audio_bytes = open(filename, "rb").read()

                    st.audio(audio_bytes, format="audio/wav")

                    st.download_button(
                        label="Download Podcast",
                        data=audio_bytes,
                        file_name="generated_podcast.wav",
                        mime="audio/wav",
                    )

                else:
                    st.error("Failed to generate podcast audio.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"An error occurred: {str(e)}")