import weaviate
import os
from dotenv import load_dotenv

# Load environment variables (`DEMO_WEAVIATE_URL` and `DEMO_WEAVIATE_RO_KEY`)
# From the provided `.env` file
load_dotenv()


def connect_to_demo_db():
    """
    Helper function to connect to the demo Weaviate database.
    For queries only.
    This database instance has the necessary data loaded.
    """
    client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("DEMO_WEAVIATE_URL"),                                 # Demo server URL,
        auth_credentials=weaviate.AuthApiKey(os.getenv("DEMO_WEAVIATE_RO_KEY")),    # Demo server read-only API key

        # OpenAI API key for queries that require it
        # Edit this to provid your own
        headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")},
    )
    return client


def connect_to_my_db():
    """
    Helper function to connect to your own Weaviate instance.
    To be used for data loading as well as queries.
    """

    # client = weaviate.connect_to_wcs(
    #     # Your Weaviate URL - Edit this to match your own Weaviate instance
    #     cluster_url=os.getenv("DEMO_WEAVIATE_URL"),

    #     # Your Weaviate API Key - Edit this to match your own Weaviate instance
    #     auth_credentials=weaviate.AuthApiKey(os.getenv("DEMO_WEAVIATE_RO_KEY")),

    #     # OpenAI API key for queries that require it
    #     # Edit this to provid your own
    #     headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")},
    # )

    # FOR DEV WORK
    client = weaviate.connect_to_local(
        headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")}
    )

    return client


def main():
    client = connect_to_demo_db()
    print(client.is_ready())  # Check connection status (i.e. is the Weaviate server ready)
    client.close()


if __name__ == "__main__":
    main()
