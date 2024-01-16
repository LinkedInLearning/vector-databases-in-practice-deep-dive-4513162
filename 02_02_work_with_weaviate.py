import utils
import weaviate.classes as wvc

# Run a query

client = utils.connect_to_demo_db()  # Connect to the demo database

movies = client.collections.get("Movie")

response = movies.query.near_text(
    query="Romantic comedy",
    limit=2,
    return_metadata=wvc.query.MetadataQuery(distance=True)
)

for o in response.objects:
    print(o.properties)
    print(o.metadata.distance)

client.close()
