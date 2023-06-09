import chromadb

client = chromadb.Client()

objects_collection = client.get_or_create_collection("objects")

agents_collection = client.get_or_create_collection("agents")

events_collection = client.get_or_create_collection("events")

locations = client.get_or_create_collection("locations")