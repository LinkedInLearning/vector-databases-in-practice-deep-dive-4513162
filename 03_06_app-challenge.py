import utils
import streamlit as st
import weaviate.classes as wvc
from weaviate.util import generate_uuid5

client = utils.connect_to_my_db()       # Connect to the demo database
# client = utils.connect_to_demo_db()   # You can also connect to the demo database

try:  # Wrap everything in a try-finally block to ensure the connection is closed
    movies = client.collections.get("Movie")
    synopses = client.collections.get("Synopsis")

    # Show page title - ReelRecommender
    st.title("ReelRecommender")

    # Have multiple tabs, each one for different features (search / movie details / recommendations)
    search_tab, movie_tab, rec_tab = st.tabs(["Search", "Movie details", "Recommend"])

    with search_tab:

        st.header("Search for a movie")
        query_string = st.text_input(label="Search for a movie")

        srch_col1, srch_col2 = st.columns(2)
        with srch_col1:
            # ====================================================================================================
            # Challenge: App enhancements - add keyword search type
            # The UI element for this is already added below, but you will need to add the logic to filter the results
            # ====================================================================================================
            search_type = st.radio(
                label="How do you want to search?",
                options=["Vector", "Keyword", "Hybrid"]  # Keyword option added
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

        # Search results - movie summaries
        # ====================================================================================================
        # Challenge: App enhancements - add keyword search type
        # You will need to add the logic for the keyword search type

        # Challenge: App enhancements - add year range filter
        # You will need to add the logic for the year range filter
        # ====================================================================================================
        st.header("Search results")

        movie_filter = (
            wvc.query.Filter.by_property("rating").greater_or_equal(value_range[0])
            & wvc.query.Filter.by_property("rating").less_or_equal(value_range[1])
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
                st.write(f"**Movie rating**: {rating}, **ID**: {movie_id}")

                synopsis = movie.references["hasSynopsis"].objects[0].properties["body"]
                st.write("**Synopsis**")
                st.write(synopsis[:200] + "...")


    with movie_tab:
    # Detailed movie information

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
            movie_uuid = generate_uuid5(int(title_input))

            movie = movies.query.fetch_object_by_id(
                uuid=movie_uuid,
                return_references=[
                    wvc.query.QueryReference(
                        link_on="hasSynopsis", return_properties=["body"]
                    ),
                ],
            )

            title = movie.properties["title"]
            director = movie.properties["director"]
            rating = movie.properties["rating"]
            movie_id = movie.properties["movie_id"]
            year = movie.properties["year"]

            st.header(title)
            st.write(f"Director: {director}")
            st.write(f"Rating: {rating}")
            st.write(f"Movie ID: {movie_id}")
            st.write(f"Year: {year}")

            with st.expander("See synopsis"):
                st.write(movie.references["hasSynopsis"].objects[0].properties["body"])


    with rec_tab:
    # AI-powered recommendations
        st.header("Recommend me a movie")
        search_string = st.text_input(label="Recommend me a ...", value="")
        occasion = st.text_input(label="In this context ...", value="any occasion")

        # Only do something if the user fills in the search string and the context
        if len(search_string) > 0 and len(occasion) > 0:
            st.subheader("Recommendations")

            # ====================================================================================================
            # Challenge: App enhancements - add individual movie analysis
            # You will need to add a prompt that to analyse each movie individually
            # Hints:
            # The prompt should be similar to the one above, but for each movie.
            # What parameter do you need to add to the query to make it work?
            # Then, you will need to add a UI element to display the generated text.
            # Consider where the generated text is stored in the response object.
            # ====================================================================================================
            response = synopses.generate.hybrid(
                query=search_string,
                grouped_task=f"""
                The user is looking to watch
                {search_string} types of movies for {occasion}.
                Provide a movie recommendation
                based on the provided movie synopses.
                """,
                limit=3,
                return_references=[
                    wvc.query.QueryReference(
                        link_on="forMovie", return_properties=["title", "movie_id"]
                    ),
                ],
            )

            st.write(response.generated)

            st.subheader("Movies analysed")
            for i, m in enumerate(response.objects):
                movie_title = m.references["forMovie"].objects[0].properties["title"]
                movie_id = m.references["forMovie"].objects[0].properties["movie_id"]
                with st.expander(f"Movie title: {movie_title}, ID: {movie_id}"):
                    st.write(m.generated)
finally:
    client.close()  # Gracefully close the connection
