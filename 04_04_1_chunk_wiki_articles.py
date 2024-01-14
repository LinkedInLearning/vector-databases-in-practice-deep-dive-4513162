from typing import List
from mediawikiapi import MediaWikiAPI
from pathlib import Path
import json

mediawikiapi = MediaWikiAPI()

page_names = [
    "History of computing",
    "Artificial intelligence",
    "Generative artificial intelligence",
    "Large language model",
    "Foundation model",
    "Deep learning",
    "Vector database",
    "Database"
]


# Split the text into units (words, in this case)
def word_splitter(source_text: str) -> List[str]:
    """
    Split the text into units (words, in this case)
    :param source_text: The text to split
    :return: A list of words
    """
    import re
    source_text = re.sub("\s+", " ", source_text)  # Replace multiple whitespces
    return re.split("\s", source_text)  # Split by single whitespace


def get_chunks_fixed_size(text: str, chunk_size_max: int = 100, overlap: float = 0.1) -> List[str]:
    """
    Split the text into chunks of a fixed size, with a given overlap.
    :param text: The text to split
    :param chunk_size_max: The maximum size of each chunk (in words). default: 100
    :param overlap: The overlap between chunks, as a fraction of the chunk size. default: 0.1
    :return: A list of chunks
    """
    text_words = word_splitter(text)
    overlap_int = int(chunk_size_max * overlap)
    chunks = []
    for i in range(0, len(text_words), chunk_size_max):
        chunk_words = text_words[max(i - overlap_int, 0): i + chunk_size_max]
        chunk = " ".join(chunk_words)
        chunks.append(chunk)
    return chunks


# Get the chunks for each page
chunked_pages = dict()
for page_name in page_names:
    page = mediawikiapi.page(page_name, auto_suggest=False)
    page_chunks = get_chunks_fixed_size(page.content)
    chunked_pages[page_name] = page_chunks
    print(f"Page {page_name} has {len(page_chunks)} chunks")


# Save the chunked pages to a file
chunks_path = Path("chunks.json")
with chunks_path.open("w", encoding="utf-8") as outfile:
    json.dump(chunked_pages, outfile, indent=2)
