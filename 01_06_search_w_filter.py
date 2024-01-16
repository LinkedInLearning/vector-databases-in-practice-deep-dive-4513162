import utils
import weaviate.classes as wvc

client = utils.connect_to_demo_db()  # Connect to the demo database

movies = client.collections.get("Movie")

# Define the filter - look for the word "love" in the description
filter = (
    wvc.query.Filter.by_property("year").greater_or_equal(1990)
    & wvc.query.Filter.by_property("description").like("space")
)

response = movies.query.near_text(  # Vector search
    query="science fiction",
    limit=2,
    filters=filter  # With the filter
)

for o in response.objects:
    movie_id = o.properties["movie_id"]
    movie_title = o.properties["title"]
    movie_year = o.properties["year"]

    print(f"ID: {movie_id}, {movie_title}, year: {movie_year}")     # Show which titles were found
    print(o.properties["description"][:50] + "...\n")                 # Show the description


client.close()
