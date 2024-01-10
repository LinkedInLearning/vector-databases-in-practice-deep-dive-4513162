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

response = movies.query.hybrid(  # Hybrid search
    query="stellar",
    limit=3,
    return_metadata=wvc.query.MetadataQuery(score=True, explain_score=True),
)

for o in response.objects:
    print(o.properties["title"])  # Show which titles were found
    print(f"score: {o.metadata.score:.3f}")  # What was the distance?
    print(f"explain_score: {o.metadata.explain_score}")  # What was the distance?
    print()


alpha = 0  # Effectively a keyword search
response = movies.query.hybrid(
    query="stellar",
    limit=3,
    alpha=alpha,
    return_metadata=wvc.query.MetadataQuery(score=True, explain_score=True),
)

print(f"===== Results with alpha: {alpha} =====")
for o in response.objects:
    print(o.properties["title"])  # Show which titles were found
    print(f"score: {o.metadata.score:.3f}")  # What was the distance?
    print(f"explain_score: {o.metadata.explain_score}")  # What was the distance?
    print()