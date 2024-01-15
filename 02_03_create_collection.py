import utils
import weaviate.classes as wvc

client = utils.connect_to_my_db()  # Connect to our own database

client.collections.create(
    # Set the name of the collection
    name="Movie",

    # Set modules to be used
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),    # Set the vectorizer module
    generative_config=wvc.config.Configure.Generative.openai(),             # Set the generative module
    # Note: Could also explicitly set the model, e.g.:
    # generative_config=wvc.config.Configure.Generative.openai(model="gpt-4-1106-preview"),

    # Define the properties of the collection
    properties=[
        wvc.config.Property(
            # Set the name of the property
            name="title",
            # Set the data type of the property
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
