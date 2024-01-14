import utils
import weaviate.classes as wvc

client = utils.connect_to_demo_db()  # Connect to the demo database

movies = client.collections.get("Movie")

filter = wvc.query.Filter("description").like("love")  # Define the filter - look for the word "love" in the description
response = movies.query.fetch_objects(
    filters=filter,
    limit=3
)

for o in response.objects:
    print(o.properties["title"])                # Show which titles were found
    print(o.properties["description"], "\n")    # Show the description


client.close()
