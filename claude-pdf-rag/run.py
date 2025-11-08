import anthropic
from pathlib import Path
from dotenv import load_dotenv
import anthropic
import base64
import httpx

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)  

client = anthropic.Anthropic()

def summarize_pdf_url(question : str , url : str):
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "url",
                            "url": url
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ],
    )
    return message.content

# print(summarize_pdf_url( "What are the key findings in this document?" , "https://assets.anthropic.com/m/1cd9d098ac3e6467/original/Claude-3-Model-Card-October-Addendum.pdf"))