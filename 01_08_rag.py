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

response = movies.generate.near_text(
    query="science fiction",
    limit=3,
    single_prompt="""
    Summarize the description:
    {description} for this movie {title}.
    """
)

for o in response.objects:
    print(o.properties["title"])  # Show which titles were found
    print(o.generated)  # RAG output
    print()


response = movies.generate.near_text(
    query="science fiction",
    limit=10,
    grouped_task="""
    Are there any common themes in these movies?
    Explain 2 in very short points,  and list the relevant movies:
    """
)

print(response.generated)
