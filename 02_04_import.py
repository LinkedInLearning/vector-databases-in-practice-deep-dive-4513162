from weaviate.util import generate_uuid5
import weaviate
import weaviate.classes as wvc
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("DEMO_WEAVIATE_URL"),  # Demo server
    auth_credentials=weaviate.AuthApiKey(os.getenv("DEMO_WEAVIATE_RO_KEY")),  # Demo server read-only API key
    headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")},  # Replace with your own API key
)

movie_df = pd.read_csv("data/movies_data.csv")

movies = client.collections.get("Movie")


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

    movie_uuid = generate_uuid5(row["ID"])
    data_obj = wvc.DataObject(
        properties=props,
        uuid=movie_uuid,
    )
    movie_objs.append(data_obj)

response = movies.data.insert_many(movie_objs)

print(f"Insertion complete with {len(response.all_responses)} objects.")
print(f"Insertion errors: {len(response.errors)}.")
