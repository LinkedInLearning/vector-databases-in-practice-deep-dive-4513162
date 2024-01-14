import utils
import weaviate.classes as wvc
import json

client = utils.connect_to_my_db()  # Connect to our own database

# Retrieve information from the client

print(client.is_ready())  # Check connection status (i.e. is the Weaviate server ready)

meta_info = client.get_meta()  # Get meta information about the Weaviate server

print(json.dumps(meta_info, indent=2))  # Print the meta information in a pretty format

client.close()

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
