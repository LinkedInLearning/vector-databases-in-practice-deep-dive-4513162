import streamlit as st

# Show page title - ReelRecommender
st.title("ReelRecommender")

# Have multiple tabs, each one for different features (search / movie details / recommendations)
search_tab, movie_tab, rec_tab = st.tabs(["Search", "Movie details", "Recommend"])

with search_tab:

    st.header("Search for a movie")
    query_string = st.text_input(label="Search for a movie")

    srch_col1, srch_col2 = st.columns(2)
    with srch_col1:
        search_type = st.radio(
            label="How do you want to search?",
            options=["Vector", "Hybrid"]
        )

    with srch_col2:
        value_range = st.slider(label="Rating range", value=(0.0, 5.0), step=0.1)

    # Search results - movie summaries
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
            st.write(synopsis[:200] + "...")


with movie_tab:
# Detailed movie information

    st.header("Movie details")
    title_input = st.text_input(label="Enter the movie row ID here (0-120)", value="")
    if len(title_input) > 0:  # Only do something if there is an input

        # Placeholder data
        title = "Desert Dance"
        director = "Ahmed Al-Bakri"
        rating = 4.5
        movie_id = 18
        year = 2014

        st.header(title)
        st.write(f"Director: {director}")
        st.write(f"Rating: {rating}")
        st.write(f"Movie ID: {movie_id}")
        st.write(f"Year: {year}")

        with st.expander("See synopsis"):
            st.write("Movie synopsis goes here")


with rec_tab:
# AI-powered recommendations
    st.header("Recommend me a movie")
    search_string = st.text_input(label="Recommend me a ...", value="")
    occasion = st.text_input(label="In this context ...", value="any occasion")

    # Only do something if the user fills in the search string and the context
    if len(search_string) > 0 and len(occasion) > 0:
        st.subheader("Recommendations")

        st.write("Movie ABC is recommended here because..")

        st.subheader("Movies analysed")
        for i, m in enumerate(["Movie 1...", "Movie 2...", "Movie 3..."]):
            movie_title = m
            movie_id = i
            movie_description = "Movie description here"
            with st.expander(f"Movie title: {movie_title}, ID: {movie_id}"):
                st.write(movie_description)
