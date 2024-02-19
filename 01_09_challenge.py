# Provided code
import utils
import weaviate.classes as wvc

client = utils.connect_to_demo_db()  # Connect to the demo database

movies = client.collections.get("Movie")

response = movies.query.fetch_objects(limit=1)

for o in response.objects:
    print(f"Movie: {o.properties['title']}\n")


# ========== TASKS ==========

# Task 1:
# Write a hybrid search query on "Review" collection.
# This collection has just the one property ("body").
#
# The query can be any text.
# e.g. “fun for the whole family”.
#
# Try this with two different alpha values, 0.1 and 0.9.
# Retrieve & display the top 3 results & scores.


# Task 2:
# A RAG query, on the “Movie” collection
# Using a vector search for: “action adventure”.
# Fetch the top 5 results, and
# Prompt the language model to generate a tagline for each movie,
# based on the movie’s title and description properties.

client.close()  # Close the connection
