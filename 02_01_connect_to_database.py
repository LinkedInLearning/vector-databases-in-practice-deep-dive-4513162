import utils

client = utils.connect_to_my_db()  # Helper function from utils.py

print(client.is_ready())  # Check connection status (i.e. is the Weaviate server ready)

client.close()
