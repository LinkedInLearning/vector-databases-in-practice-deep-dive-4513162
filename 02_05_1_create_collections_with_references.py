import utils
import weaviate.classes as wvc

client = utils.connect_to_my_db()  # Connect to our own database

# Delete our previously created collection
client.collections.delete("Movie")

# Add reviews first
reviews = client.collections.create(
    name="Review",
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
    generative_config=wvc.config.Configure.Generative.openai(),
    properties=[
        wvc.config.Property(
            name="body",
            data_type=wvc.config.DataType.TEXT,
        ),
    ],
)

# Add movies
movies = client.collections.create(
    name="Movie",
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
    generative_config=wvc.config.Configure.Generative.openai(),
    properties=[
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
    # A reference property with name "hasReview". Points to the "Review" collection
    references=[
        wvc.config.ReferenceProperty(
            name="hasReview",
            target_collection="Review",
        )
    ],
)


# Add synopses
synopses = client.collections.create(
    name="Synopsis",
    vectorizer_config=wvc.config.Configure.Vectorizer.text2vec_openai(),
    generative_config=wvc.config.Configure.Generative.openai(),
    properties=[
        wvc.config.Property(
            name="body",
            data_type=wvc.config.DataType.TEXT,
        ),
    ],
    # A reference property with name "forMovie". Points to the "Movie" collection
    references=[
        wvc.config.ReferenceProperty(
            name="forMovie",
            target_collection="Movie",
        )
    ],
)


# Add a reference property for the "Movie" collection, with name "hasSynopsis". Points to the "Synopsis" collection
movies.config.add_reference(
    wvc.config.ReferenceProperty(
        name="hasSynopsis",
        target_collection="Synopsis"
    )
)
# Now the "Movie" and "Synopsis" collections refer to each other

client.close()
