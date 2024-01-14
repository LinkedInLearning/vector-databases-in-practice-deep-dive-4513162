import utils
import weaviate.classes as wvc

client = utils.connect_to_demo_db()  # Connect to the demo database

movies = client.collections.get("Movie")

for query in ["love", "amorous", "adventure movie set in outer galaxy"]:  # Loop through multiple query terms
    response = movies.query.near_text(  # Vector search
        query=query,
        limit=2,
        return_metadata=wvc.query.MetadataQuery(distance=True),
    )

    print(f"===== Search results for '{query}'. =====")  # Print the query term
    for o in response.objects:
        print(o.properties["title"])            # Show which titles were found
        print(o.properties["description"])      # Show the description
        print(f"{o.metadata.distance:.3f}\n")   # What was the distance?


client.close()
