import weaviate
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("DEMO_WEAVIATE_URL"),  # Demo server
    auth_credentials=weaviate.AuthApiKey(os.getenv("DEMO_WEAVIATE_RO_KEY")),  # Demo server read-only API key
)

readiness = client.is_ready()

print(readiness)

meta_info = client.get_meta()

print(json.dumps(meta_info, indent=2))
