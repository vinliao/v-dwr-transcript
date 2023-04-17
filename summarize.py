import re
from typing import List
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_text(file_path: str):
    """Reads a text file and returns the contents as a string.

    Args:
        file_path (str): The path to the text file.

    Returns:
        str: The contents of the text file.
    """
    with open(file_path, "r") as f:
        return f.read()


def split_text_into_chunks(text: str, chunk_size: int) -> List[str]:
    chunks = []
    current_chunk = ""
    remaining_text = text

    while remaining_text:
        next_chunk = remaining_text[:chunk_size]
        last_punctuation = max(
            [next_chunk.rfind("."), next_chunk.rfind("?"), next_chunk.rfind("!")]
        )

        if last_punctuation == -1:  # no punctuation found in this chunk
            last_punctuation = chunk_size

        chunk = next_chunk[: last_punctuation + 1].strip()
        current_chunk += " " + chunk
        remaining_text = remaining_text[len(chunk) :].strip()

        if len(current_chunk) > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = ""

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def process_text(text: str, chunk_size: int = 1000) -> List[str]:
    sections = re.split(r"\n# .+?]", text)
    processed_sections = []

    for section in sections:
        if not section.strip():
            continue
        chunks = split_text_into_chunks(section, chunk_size)
        processed_sections.extend(chunks)

    return processed_sections


def summarize_chunk(text: str):
    prompt = "Please extract out the ideas and concepts, especially related to Farcaster, Ethereum, decentralized social media. Don't edit the text, just extract. Everything else should be left out. The result you give must be in first-person, and you should speak as if you're the explainer (the person explaining the ideas, not the interviewer). You should speak like, 'I think...' or just assert some fact about the topic at hand. Here's the text:"
    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful summarizer."},
            {"role": "user", "content": f"{prompt}\n\n{text}"},
        ],
        temperature=0,
    )

    return result["choices"][0]["message"]["content"]


text_chunks = process_text(get_text("./all.md"), chunk_size=4000)
with open("summary.md", "a") as f:
    for chunk in text_chunks:
        summary = summarize_chunk(chunk)
        print(summary)
        f.write(summary + "\n")
