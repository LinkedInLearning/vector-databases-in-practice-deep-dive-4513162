import utils

client = utils.connect_to_demo_db()  # Connect to the demo database

movies = client.collections.get("Movie")

response = movies.generate.near_text(
    query="science fiction",
    limit=3,
    single_prompt="""
    Summarize the description:
    {description} for this movie {title}.
    """
)

for o in response.objects:
    print(o.properties["title"])    # Show which titles were found
    print(o.generated)              # RAG output
    print()


response = movies.generate.near_text(
    query="science fiction",
    limit=10,
    grouped_task="""
    Are there any common themes in these movies?
    Explain 2 in very short points,  and list the relevant movies:
    """
)

print(response.generated)  # Print the generated text


client.close()
