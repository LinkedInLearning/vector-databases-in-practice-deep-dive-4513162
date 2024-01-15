import streamlit as st

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
        search_type = st.radio(
            label="How do you want to search?", options=["Vector", "Keyword", "Hybrid"]
        )

    with srch_col2:
        value_range = st.slider(label="Rating range", value=(0.0, 5.0), step=0.1)

# Search results (top N movies)
# Movie summary information
    st.header("Search results")

    response = [
        {
            "title": f"Title {i}",
            "rating": 4.0,
            "movie_id": i,
            "director": f"Director {i}",
        }
        for i in range(5)
    ]  # Placeholder response

    for movie in response:
        with st.expander(movie["title"]):
            rating = movie["rating"]
            movie_id = movie["movie_id"]
            synopsis = "Synopsis here"
            st.write(f"**Movie rating**: {rating}, **ID**: {movie_id}")
            st.write("**Synopsis**")
            if len(synopsis) > 200:
                st.write(synopsis[:200] + "...")
            else:
                st.write(synopsis[:200])


with movie_tab:
# See detailed movie information
# Movie title, director, synopsis, and year
    st.header("Movie details")
    title_input = st.text_input(label="Enter the movie row ID here (0-120)", value="")
    if len(title_input) > 0:  # Only do something if there is an input
        # Placeholder data
        st.header("Desert Dance")

        director = "Ahmed Al-Bakri"
        rating = 4.5
        movie_id = 18
        year = 2014
        st.write(f"Director: {director}")
        st.write(f"Rating: {rating}")
        st.write(f"Movie ID: {movie_id}")
        st.write(f"Year: {year}")

        with st.expander("See synopsis"):
            st.write("Movie synopsis goes here")


with rec_tab:
# AI-powered recommendations
# Recommend a movie based on user input
# Based on search criteria (search for similar synopses) and occasion (with kids, date night, film study, etc.)
    st.header("Recommend me a movie")
    search_string = st.text_input(label="Recommend me a ...", value="")
    occasion = st.text_input(label="In this context ...", value="any occasion")

    st.subheader("Recommendations")

    st.write("Movie ABC is recommended here because..")

    st.subheader("Movie analysis")
    for i, m in enumerate(["Movie 1...", "Movie 2...", "Movie 3..."]):
        movie_title = m
        movie_id = i
        with st.expander(movie_title):
            st.write("This movie is/not suitable because...")
            st.subheader("Synopsis")
            st.write("Synopsis goes here")
            st.write(f"Movie id: {movie_id}")
