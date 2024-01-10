import weaviate
import weaviate.classes as wvc
import os

client = weaviate.connect_to_wcs(
    cluster_url="https://juofherxrfgo1cki4ierfa.c1.europe-west3.gcp.weaviate.cloud",
    auth_credentials=weaviate.AuthApiKey("RfyaBcQcbicZifmJp4fi0AmgnvGM5bUJYYjm"),
    headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")  # Replace with your own API key
    },
)

movies = client.collections.get("Movie")

for query in ["love", "amorous", "adventure movie set in outer galaxy"]:
    response = movies.query.near_text(  # Vector search
        query=query,
        limit=2,
        return_metadata=wvc.query.MetadataQuery(distance=True),
    )

    print(f"===== Search results for '{query}'. =====")
    for o in response.objects:
        print(o.properties["title"])  # Show which titles were found
        print(o.properties["description"])  # Show the description
        print(f"{o.metadata.distance:.3f}")  # What was the distance?
        print()
