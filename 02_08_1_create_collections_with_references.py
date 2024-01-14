import utils
import weaviate.classes as wvc

client = utils.connect_to_my_db()  # Connect to our own database

# Delete any previously created collections with the same name
client.collections.delete("Movie")
client.collections.delete("Review")
client.collections.delete("Synopsis")

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


# ====================================================================================================
# Add a collection for synopses (called "Synopsis")
# Use the same vectorizer and generative models as the "Movie" collection
# Add a property called "body" with data type TEXT
# Add a reference property with name "forMovie" that points to the "Movie" collection
# ====================================================================================================
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


# ====================================================================================================
# Add a reference property to the "Movie" collection with name "hasSynopsis".
# This points to the "Synopsis" collection
# Hint: use the "movies.config.add_reference" method
# ====================================================================================================
movies.config.add_reference(
    wvc.config.ReferenceProperty(
        name="hasSynopsis",
        target_collection="Synopsis"
    )
)

client.close()
