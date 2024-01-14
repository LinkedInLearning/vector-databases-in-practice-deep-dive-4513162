import utils
import weaviate.classes as wvc

client = utils.connect_to_my_db()  # Connect to our own database

client.collections.create(
    name="Movie",                                                           # Set the name of the collection
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),    # Set the vectorizer
    generative_config=wvc.config.Configure.Generative.openai(),             # Set the generative model
    properties=[                                                            # Define the properties
        wvc.config.Property(
            name="title",
            data_type=wvc.config.DataType.TEXT,
        ),
        wvc.config.Property(
            name="description",
            data_type=wvc.config.DataType.TEXT,
        ),
        wvc.config.Property(
            name="movie_id",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="year",
            data_type=wvc.config.DataType.INT,
        ),
        wvc.config.Property(
            name="rating",
            data_type=wvc.config.DataType.NUMBER,
        ),
        wvc.config.Property(
            name="director",
            data_type=wvc.config.DataType.TEXT,
            skip_vectorization=True,
        ),
    ],
)

client.close()
