print("Staring Scrapping process from Cook with Manali")

import spacy
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import rdflib
nlp = spacy.load("en_core_web_sm")
# Load the FoodON OWL file
g = rdflib.Graph()
g.parse("http://purl.obolibrary.org/obo/foodon.owl", format="xml")

uri = "mongodb+srv://ajaiarjun2003:FNW7AHsFyAxfiWPZ@recipefinder.mdlzb.mongodb.net/?retryWrites=true&w=majority&appName=RecipeFinder"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client["Recipe_DB"]  # replace with your actual database name
    collection = db["recipes"]  # replace with your actual collection name
except Exception as e:
    print(e)