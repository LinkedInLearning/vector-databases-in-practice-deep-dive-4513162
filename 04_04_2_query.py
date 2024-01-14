import utils
from pathlib import Path
import json

query = "how vector databases are different from relational databases"

client = utils.connect_to_demo_db()  # Connect to the demo database

wiki_chunks = client.collections.get(name="WikiChunk")

# Query the chunks
response = wiki_chunks.generate.near_text(
    query=query,
    limit=10,
    grouped_task=f"""
    Tell us
    {query}
    using the information in these passages.
    Summarise into a few concise, short point form messages.
    3-5 points altogether will suffice.
    """
)

print(response.generated)
print("Source data:")
for o in response.objects:
    print(o.properties["title"], "Chunk:", o.properties["chunk_number"])
