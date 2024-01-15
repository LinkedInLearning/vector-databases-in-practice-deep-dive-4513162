import utils
import weaviate.classes as wvc
from weaviate.util import generate_uuid5
import pandas as pd

client = utils.connect_to_my_db()  # Connect to our own database

movies = client.collections.get("Movie")
reviews = client.collections.get("Review")
# Also load the synopses collection
synopses = client.collections.get("Synopsis")

movie_df = pd.read_csv("data/movies_data.csv")


# Import reviews first
review_objs = list()
for i, row in movie_df.iterrows():
    for c in [1, 2, 3]:  # There are three reviews per movie in this dataset
        col_name = f"Critic Review {c}"
        if len(row[col_name]) > 0:
            props = {
                "body": row[col_name],
            }
            review_uuid = generate_uuid5(row[col_name])
            data_obj = wvc.data.DataObject(properties=props, uuid=review_uuid)
            review_objs.append(data_obj)

response = reviews.data.insert_many(review_objs)

print(f"Insertion complete with {len(response.all_responses)} objects.")
print(f"Insertion errors: {len(response.errors)}.")


# Import movies
movie_objs = list()
for i, row in movie_df.iterrows():
    props = {
        "title": row["Movie Title"],
        "description": row["Description"],
        "rating": row["Star Rating"],
        "director": row["Director"],
        "movie_id": row["ID"],
        "year": row["Year"],
    }
    # Add references to reviews
    review_uuids = list()
    for c in [1, 2, 3]:
        col_name = f"Critic Review {c}"
        if len(row[col_name]) > 0:
            review_uuid = generate_uuid5(row[col_name])  # Identify the review IDs to refer to
            review_uuids.append(review_uuid)  # Collect the review IDs

    movie_uuid = generate_uuid5(row["ID"])
    data_obj = wvc.data.DataObject(
        properties=props,
        uuid=movie_uuid,
        references={"hasReview": wvc.data.Reference.to(review_uuids)},
    )
    movie_objs.append(data_obj)

response = movies.data.insert_many(movie_objs)

print(f"Insertion complete with {len(response.all_responses)} objects.")
print(f"Insertion errors: {len(response.errors)}.")

# ====================================================================================================
# Add synopses data, similarly to how we added movies
# The synopsis data is in the same CSV file, but in the "Synopsis" column
# ====================================================================================================

# Create a list of synopsis objects

# Iterate over the rows in the CSV file

    # Create a dictionary of properties

    # Generate a UUID for the synopsis (use the same UUID as the movie)
    # Note: this is okay as the synopsis and movie are in different collections
    # Create a reference to the movie in the "forMovie" property

    # Add the synopsis object to the list

# Insert the synopsis objects into the collection


# ====================================================================================================
# Add references from movies to synopses
# Hints:
# - use the "wvc.data.DataReference" class to create the reference objects
# - use the "movies.data.reference_add_many" method to add the references to the collection
# ====================================================================================================
# Create a list of references

# Iterate over the rows in the CSV file
    # Generate a UUID for the movie

    # Create a reference object with the "hasSynopsis" property
    # Hint: use the "wvc.data.DataReference" class
    # Add the reference object to the list

# Add the references to the collection
# Hint: use the "movies.data.reference_add_many" method

client.close()
