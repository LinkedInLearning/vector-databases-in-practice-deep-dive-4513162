import utils
import streamlit as st
import weaviate.classes as wvc
from weaviate.util import generate_uuid5

client = utils.connect_to_my_db()       # Connect to the demo database
# client = utils.connect_to_demo_db()   # You can also connect to the demo database

movies = client.collections.get("Movie")
synopses = client.collections.get("Synopsis")

# Show page title - ReelRecommender
st.title("ReelRecommender")

# Have multiple tabs, each one for different features (search / movie details / recommendations)
search_tab, movie_tab, rec_tab = st.tabs(["Search", "Movie details", "Recommend"])

with search_tab:
# Search - what do they want to watch?
# Components:
# - Search bar - text input for query terms
# - Radio selection for search type
# - Filter (multi-select) for minimum rating
    st.header("Search for a movie")
    query_string = st.text_input(label="Search for a movie")

    srch_col1, srch_col2 = st.columns(2)
    with srch_col1:
        # ====================================================================================================
        # Challenge: App enhancements - add keyword search type
        # The UI element for this is already added below, but you will need to add the logic to filter the results
        # ====================================================================================================
        search_type = st.radio(
            label="How do you want to search?", options=["Vector", "Keyword", "Hybrid"]  # Keyword option added
        )

    with srch_col2:
        value_range = st.slider(label="Rating range", value=(0.0, 5.0), step=0.1)
        # Get inputs for year range
        # ====================================================================================================
        # Challenge: App enhancements - add year range filter
        # The UI element for this is already added below, but you will need to add the logic to filter the results
        # ====================================================================================================
        year_min = st.number_input(label="Year from", value=1960, step=1)
        year_max = st.number_input(label="Year to", value=2023, step=1)

# Search results (top N movies)
# Movie summary information
    # ====================================================================================================
    # Challenge: App enhancements - add keyword search type
    # You will need to add the logic for the keyword search type

    # Challenge: App enhancements - add year range filter
    # You will need to add the logic for the year range filter
    # ====================================================================================================
    st.header("Search results")

    movie_filter = (
        wvc.query.Filter("rating").greater_or_equal(value_range[0])
        & wvc.query.Filter("rating").less_or_equal(value_range[1])
    )
    synopsis_xref = wvc.query.QueryReference(
        link_on="hasSynopsis", return_properties=["body"]
    )

    if len(query_string) > 0:  # Only run a search if there is an input

        if search_type == "Vector":
            response = movies.query.near_text(
                query=query_string,
                filters=movie_filter,
                limit=5,
                return_references=[synopsis_xref],
            )
        else:
            response = movies.query.hybrid(
                query=query_string,
                filters=movie_filter,
                limit=5,
                return_references=[synopsis_xref],
            )
    else:
        response = movies.query.fetch_objects(
            filters=movie_filter,
            limit=5,
            return_references=[synopsis_xref],
        )

    for movie in response.objects:
        with st.expander(movie.properties["title"]):
            rating = movie.properties["rating"]
            movie_id = movie.properties["movie_id"]
            synopsis = movie.references["hasSynopsis"].objects[0].properties["body"]
            st.write(f"**Movie rating**: {rating}, **ID**: {movie_id}")
            st.write("**Synopsis**")
            if len(synopsis) > 200:
                st.write(synopsis[:200] + "...")
            else:
                st.write(synopsis[:200])


with movie_tab:
# See detailed movie information
# Movie title, director, synopsis, and any reviews

    # ====================================================================================================
    # Challenge: App enhancements - add reviews
    # You will need to fetch the corresponding review data for each movie,
    # and then display the review text in the UI
    # Hints:
    # Movie reviews are stored in the "Review" collection
    # Refer to the collection definition from chapter 2 for the property names
    # ====================================================================================================
    st.header("Movie details")
    title_input = st.text_input(label="Enter the movie row ID here (0-120)", value="")
    if len(title_input) > 0:  # Only do something if there is an input
        movie = movies.query.fetch_object_by_id(
            uuid=generate_uuid5(int(title_input)),
            return_references=[
                wvc.query.QueryReference(
                    link_on="hasSynopsis", return_properties=["body"]
                ),
            ],
        )

        st.header(movie.properties["title"])

        director = movie.properties["director"]
        rating = movie.properties["rating"]
        movie_id = movie.properties["movie_id"]
        year = movie.properties["year"]
        st.write(f"Director: {director}")
        st.write(f"Rating: {rating}")
        st.write(f"Movie ID: {movie_id}")
        st.write(f"Year: {year}")

        with st.expander("See synopsis"):
            st.write(movie.references["hasSynopsis"].objects[0].properties["body"])


with rec_tab:
# AI-powered recommendations
# Recommend a movie based on user input
# Based on search criteria (search for similar movies) and occasion (with kids, date night, film study, etc.)
    st.header("Recommend me a movie")
    search_string = st.text_input(label="Recommend me a ...", value="")
    occasion = st.text_input(label="In this context ...", value="any occasion")

    # Only do something if the user fills in the search string and the context
    if len(search_string) > 0 and len(occasion) > 0:
        st.subheader("Recommendations")

        response = synopses.generate.hybrid(
            query=search_string,
            grouped_task=f"""
            Provide top 2 recommendations on what to watch
            out of the provided information of movie synopses.
            The recommendations should be based on the user's criteria
            of {search_string} types of movies for {occasion}.
            """,
            single_prompt=f"""
            Evaluate the synopsis to concisely state
            whether it will be a good fit
            for the user's criteria
            of {search_string} movies for {occasion},
            and the reasons why.
            The movie synopsis is {{body}}.
            """,
            limit=5,
            return_references=[
                wvc.query.QueryReference(
                    link_on="forMovie", return_properties=["title", "movie_id"]
                ),
            ],
        )

        st.write(response.generated)

        st.subheader("Movie analysis")
        for i, m in enumerate(response.objects):
            movie_title = m.references["forMovie"].objects[0].properties["title"]
            movie_id = m.references["forMovie"].objects[0].properties["movie_id"]
            with st.expander(movie_title):
                st.write(m.generated)
                st.subheader("Synopsis")
                st.write(m.properties["body"])
                st.write(f"Movie id: {movie_id}")
