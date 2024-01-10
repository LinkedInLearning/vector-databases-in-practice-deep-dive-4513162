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

filter = (wvc.query.Filter("year").greater_or_equal(1990) & wvc.query.Filter("description").like("space"))

response = movies.query.near_text(
    query="science fiction",
    limit=2,
    filters=filter
)

for o in response.objects:
    print(f'ID: {o.properties["movie_id"]}, {o.properties["title"]}, year: {o.properties["year"]}')  # Show which titles were found
    print(o.properties["description"][:50] + "...")  # Show the description
