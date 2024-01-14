# Provided code
import utils
import weaviate.classes as wvc

client = utils.connect_to_demo_db()  # Connect to the demo database

movies = client.collections.get("Movie")

response = movies.query.fetch_objects(limit=1)

for o in response.objects:
    print(f"Movie: {o.properties['title']}")


# ========== TASKS ==========

# Task 1:
# Write a hybrid search query on a collection called Review.
# This collection has just the one property, called "body".
#
# The query can be any text you’d like to search for in a movie review.
# For example, I will use the phrase “fun for the whole family”.
#
# Try this with two different alpha values, 0.1 and 0.9 - see if the results differ at all.
# Retrieving the top 3 results should be plenty


reviews = client.collections.get("Review")


for alpha in [0.1, 0.9]:
    response = reviews.query.hybrid(
        query="fun for the whole family",
        alpha=alpha,
        limit=3,
    )

    print(f"Search results with alpha: {alpha}")
    for o in response.objects:
        print(o.properties["body"])


# Task 2:
# Write a RAG query, with:
# A vector search for the string “action adventure”,
# to retrieve the top 5 results, and then
# prompt the language model to generate a tagline for each movie,
# based on the movie’s "title" and "description" properties.

response = movies.generate.near_text(
    query="action adventure",
    limit=3,
    single_prompt="""
    Suggest a tagline for this film based on the title and description.
    Title: {title}
    Description: {description}
    """
)

print(f"Generated results:")
for o in response.objects:
    print("---- Movie informaton ----")
    print(o.properties["title"])
    print(o.properties["description"])
    print("---- Generated tagline ----")
    print(o.generated)


client.close()
