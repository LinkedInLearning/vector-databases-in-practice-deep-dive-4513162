import weaviate
import weaviate.classes as wvc
import os
from dotenv import load_dotenv

load_dotenv()

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("DEMO_WEAVIATE_URL"),  # Demo server
    auth_credentials=weaviate.AuthApiKey(os.getenv("DEMO_WEAVIATE_RO_KEY")),  # Demo server read-only API key
)


movies = client.collections.create(
    name="Movie",
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
    generative_config=wvc.config.Configure.Generative.openai(),
    properties=[
        wvc.Property(
            name="title",
            data_type=wvc.DataType.TEXT,
        ),
        wvc.Property(
            name="description",
            data_type=wvc.DataType.TEXT,
        ),
        wvc.Property(
            name="movie_id",
            data_type=wvc.DataType.INT,
        ),
        wvc.Property(
            name="year",
            data_type=wvc.DataType.INT,
        ),
        wvc.Property(
            name="rating",
            data_type=wvc.DataType.NUMBER,
        ),
        wvc.Property(
            name="director",
            data_type=wvc.DataType.TEXT,
            skip_vectorization=True,
        ),
    ],
)
