
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://ajaiarjun2003:FNW7AHsFyAxfiWPZ@recipefinder.mdlzb.mongodb.net/?retryWrites=true&w=majority&appName=RecipeFinder"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    db = client["Recipe_DB"]  # replace with your actual database name
    collection = db["recipes"]  # replace with your actual collection name

    # Sample recipe document
    recipe_document = {
        "title": "Spaghetti Carbonara",
        "ingredients": [
            "200g spaghetti",
            "100g pancetta",
            "2 large eggs",
            "50g pecorino cheese",
            "50g parmesan cheese",
            "2 cloves garlic",
            "Salt",
            "Freshly ground black pepper",
            "Fresh parsley (for garnish)"
        ],
        "instructions": "1. Cook spaghetti in salted water until al dente. 2. In a separate pan, cook pancetta until crispy. 3. Beat the eggs and mix with cheeses. 4. Combine hot spaghetti with pancetta and garlic, then remove from heat. 5. Stir in the egg and cheese mixture quickly. 6. Serve with extra cheese and parsley.",
        "cook_time": {
            "prep_time": "10 minutes",
            "cook_time": "15 minutes",
            "total_time": "25 minutes"
        },
        "notes": "Add more cheese for extra creaminess.",
        "nutrition": {
            "calories": 500,
            "protein": "20g",
            "carbohydrates": "60g",
            "fat": "25g"
        },
        "additional": {
            "course": "Main",
            "cuisine": "Italian"
        }
    }

    # Insert the document into the collection
    result = collection.insert_one(recipe_document)
    print(f"Recipe inserted with id: {result.inserted_id}")
    recipes = collection.find()

    for recipe in recipes:
        print(recipe)

except Exception as e:
    print(e)

