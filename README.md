# Blog Post to Podcast

This project is a Streamlit application that converts any blog post or article into a podcast episode. It uses AI to scrape the content of a webpage, summarize it, and generate an audio file.

## How it works

The application takes a URL as input and performs the following steps:

1.  **Scrapes Content:** It uses Firecrawl to scrape the content of the provided URL.
2.  **Summarizes:** The scraped content is then summarized into a podcast script using Google's Gemini model.
3.  **Generates Audio:** The script is converted into an audio file using the ElevenLabs API.
4.  **Displays and Downloads:** The generated podcast is displayed on the Streamlit UI, and you can download it as a `.wav` file.

## Dependencies

The project uses the following Python libraries:

*   `firecrawl-py`
*   `google-genai`
*   `elevenlabs`
*   `agno`
*   `streamlit`

You can install them using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## How to Run

1.  Clone the repository.
2.  Create a `.env` file in the root directory and add your API keys:

    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ELEVEN_LABS_API_KEY="YOUR_ELEVEN_LABS_API_KEY"
    FIRECRAWL_API_KEY="YOUR_FIRECRAWL_API_KEY"
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Run the Streamlit application:

    ```bash
    streamlit run main.py
    ```

## To-Do

There is a known conflict between the `agno` and `streamlit` libraries that needs to be resolved. Due to this conflict, the application logic runs as intended and saves the generated podcast in the `podcasts` directory, but the Streamlit UI does not update to show the generated podcast.

## Example

The `podcasts` directory contains example podcasts generated from the Wikipedia page of [Chris Pratt](https://en.wikipedia.org/wiki/Chris_Pratt).