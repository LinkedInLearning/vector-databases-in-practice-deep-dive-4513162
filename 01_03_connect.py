import weaviate
import weaviate.classes as wvc  # Import helper classes
import os
from dotenv import load_dotenv

load_dotenv()

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("DEMO_WEAVIATE_URL"),  # Demo server
    auth_credentials=weaviate.AuthApiKey(os.getenv("DEMO_WEAVIATE_RO_KEY")),  # Demo server read-only API key
)

print(client.is_ready())  # Check connection status (i.e. is the Weaviate server ready)

# Additional code snippets will go here in furture examples
