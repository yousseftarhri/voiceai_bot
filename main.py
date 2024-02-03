import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from openai import OpenAI
import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi
import tiktoken

load_dotenv()

PORT = int(os.environ.get('PORT', 5000))
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key= OPENAI_API_KEY)
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
def generate_response(msg) :
  response = model.generate_content(
      msg,
      generation_config=genai.types.GenerationConfig(
          max_output_tokens=2048,
          temperature=0.5)
  )
  return response.text

def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)

def start(update, context):
    """Send a message when the command /start is issued."""
    bot = context.bot


    message = """ 
🎙️ *Welcome to SumVoiceAi - Your Intelligent Speech Summarizer!*

Are you tired of sifting through hours of recorded lectures or meetings? Introducing SumVoiceAi, the revolutionary Telegram bot that transforms your spoken words into concise summaries effortlessly.

🚀 *How It Works:*
- _Record_: Just record your thoughts or upload an MP3 audio file directly through Telegram.
- _Summarize_: Our AI will analyze and summarize the key points of your recording, saving you valuable time.

*YouTube Summary Wizard! 🪄*
- _Copy and paste the YouTube link_: Just provide the URL, and boom! Your video gets magically condensed into a digestible summary.
- _Command magic_: Use the simple /link + [URL] command to trigger the YouTube summarization.
- _Say goodbye to video marathons_: Get the key takeaways without sacrificing precious minutes.

🚀 *Ready to Get Started?*
Record, Summarize, and Conquer with SumVoiceAi!
 """


    bot.send_message(chat_id=update.message.chat_id, text=message,parse_mode= 'Markdown')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def voice_handler(update, context):

    try :
        #chat_id, user_name, file_id_voice, transcript_text, bot_response.
        try:
            duration = update.message.voice.duration
            file_id = update.message.voice.file_id

        except :
            duration = update.message.audio.duration
            file_id = update.message.audio.file_id

        chat_id = update.message.chat_id

        bot = context.bot
        file = bot.getFile(file_id)
        name_audio = f'voice_{chat_id}.mp3'
        bot.send_message(chat_id=chat_id, text='Summarizing...')
        file.download(name_audio)

        file_path = f'voice_{update.message.chat_id}.mp3'
        audio_file = open(file_path, "rb")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        print(transcript.text)

        prompt_template = f"""Write a concise summary of the following text and summary with the same language as the text.
        text : "{transcript.text}"
        CONCISE SUMMARY:"""

        ai = generate_response(prompt_template)

        bot.send_message(chat_id=chat_id, text=ai)

        if os.path.exists(file_path):
        # Delete the file
            os.remove(file_path)
            print(f"File {file_path} has been deleted.")
        else:
            print(f"File {file_path} does not exist.")



    except Exception as e:
        bot = context.bot
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text='We have a problem in our bot we gonna fix it ASAP')
        print(f"An unexpected error occurred: {e}")
    print("ok")

def command_link(update, context):
    try :
        bot = context.bot
        chat_id = update.message.chat_id
        user_input = update.message.text
        if user_input.startswith("/link"):
            # Extract the URL part after "/link"
            url = user_input.split("/link")[1].strip()
            # Define a regular expression pattern to match YouTube video IDs
            youtube_pattern = re.compile(r'(?:https?://)?(?:www\.)?(?:youtube\.com/.*?[?&]v=|youtu\.be/)([\w-]+)')

            # Search for the pattern in the user input
            match = youtube_pattern.search(url)

            # Check if a match is found
            if match:
                video_id = match.group(1)
                try:
                    subtitles = YouTubeTranscriptApi.get_transcript(video_id,languages=['en'])
                    result_string = ' '.join(item['text'] for item in subtitles)
                    print(result_string)
                except Exception as e:
                    print(e)
                    bot.send_message(chat_id=chat_id,text="Sorry, but subtitles are disabled for this video")
                    return None

                if count_tokens(result_string) > 30720 :
                    bot.send_message(chat_id=chat_id, text="We apologize for not accepting more tokens than 30720, however we are working on lengthier videos. The video is a little bit longer.")
                else :
                    bot.send_message(chat_id=chat_id, text="Summarizing...")
                    prompt_template = f"""Write a concise summary of the following text that is delimited in triple quotes. and summary with the same language as the text that is delimited in triple quotes.

                    text : ''' {result_string} '''
                    CONCISE SUMMARY:"""
                    ai = generate_response(prompt_template)

                    bot.send_message(chat_id=chat_id, text=ai)
            else:
                bot.send_message(chat_id=chat_id, text="Invalid YouTube link. Please enter a valid YouTube link.")
        else:
            bot.send_message(chat_id=chat_id, text="Invalid input. Please enter a link in the format /link 'url'.")
    except Exception as e:
        print(e)
        bot.send_message(chat_id=chat_id, text="We have a problem in the bot, we gonna fix it ASAP")


def main():
    """Start the bot."""

    updater = Updater(bot_token)
    dp = updater.dispatcher
    #dp = ApplicationBuilder().token(bot_token).build()

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("link", command_link))

    #dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.voice, voice_handler))
    dp.add_handler(MessageHandler(Filters.audio, voice_handler))
    dp.add_handler(MessageHandler(Filters.text, start))

    # log all errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
