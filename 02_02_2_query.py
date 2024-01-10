import weaviate
import weaviate.classes as wvc
import os
from dotenv import load_dotenv

load_dotenv()

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("DEMO_WEAVIATE_URL"),  # Demo server
    auth_credentials=weaviate.AuthApiKey(os.getenv("DEMO_WEAVIATE_RO_KEY")),  # Demo server read-only API key
)

movies = client.collections.get("Movie")

response = movies.query.near_text(
    query="Romantic comedy",
    limit=2,
    return_metadata=wvc.query.MetadataQuery(distance=True)
)

for o in response.objects:
    print(o.properties)
    print(o.metadata.distance)
