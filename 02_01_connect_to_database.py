import weaviate
import weaviate.classes as wvc  # Import helper classes

client = weaviate.connect_to_wcs(
    cluster_url="<YOUR_CLUSTER_URL>",  # Replace <YOUR_CLUSTER_URL> with your cluster URL
    auth_credentials=weaviate.AuthApiKey("<YOUR_API_KEY>"),  # Replace <YOUR_API_KEY> with your Admin API key
)

print(client.is_ready())  # Check connection status (i.e. is the Weaviate server ready)
