import utils
import weaviate.classes as wvc

client = utils.connect_to_demo_db()  # Connect to the demo database

movies = client.collections.get("Movie")

response = movies.query.bm25(  # Keyword search for the word "love"
    query="love",
    limit=3,
    return_metadata=wvc.query.MetadataQuery(score=True),
)

for o in response.objects:
    print(o.properties["title"])        # Show which titles were found
    print(o.properties["description"])  # Show the description
    print(f"{o.metadata.score:.3f}\n")  # What was the score?


client.close()
