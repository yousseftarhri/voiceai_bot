# voicai_bot

# SumVoiceAi - Your Intelligent Speech Summarizer 🎙️

SumVoiceAi is a Telegram bot that leverages the power of the **Gemini Google AI Language Model (LLM)** and the **Whisper OpenAI Language Model (LLM)** to transform your spoken words into concise summaries effortlessly. Whether you want to summarize recorded lectures, meetings, or YouTube videos, SumVoiceAi has got you covered!

## Features

- **Voice Summarization:** Record your thoughts or upload an MP3 audio file directly through Telegram, and SumVoiceAi will analyze and summarize the key points for you.

- **YouTube Summary Wizard:** Easily condense YouTube videos into digestible summaries by providing the video URL or using the /link + [URL] command.

## Getting Started

### Prerequisites

- Python 3.x
- [Telegram Bot Token](https://core.telegram.org/bots#botfather) - Get your bot token from the BotFather on Telegram.
- [OpenAI API Key](https://beta.openai.com/signup/) - Sign up for an OpenAI API key.
- [Google API Key](https://ai.google.dev/) - Create a project on Google Cloud Platform and enable the necessary APIs.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yousseftarhri/voiceai_bot.git
    cd voicai_bot
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    Create a `.env` file in the project root and add the following:

    ```env
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    OPENAI_API_KEY=your_openai_api_key
    GOOGLE_API_KEY=your_google_api_key
    ```

4. Run the bot:

    ```bash
    python main.py
    ```

## Usage

- Start the bot by sending the `/start` command in your Telegram chat.
- Record or upload an audio file to receive a summarized response.
- Use the `/link` command followed by a YouTube video URL to get a summary of the video.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


## Acknowledgments

- Thanks to OpenAI, Google, and other contributors for their amazing tools and libraries.
