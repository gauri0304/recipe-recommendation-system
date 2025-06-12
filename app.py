from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load recipes from external CSV file
def load_recipes():
    return pd.read_csv("recipes.csv")

# Function to recommend recipes based on user ingredients
def recommend_recipes(ingredients, recipes):
    available_recipes = []
    for _, row in recipes.iterrows():
        recipe_ingredients = set(row["Ingredients"].split(", "))
        user_ingredients = set(ingredients)

        if recipe_ingredients.issubset(user_ingredients):
            available_recipes.append(row)
    return pd.DataFrame(available_recipes)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_ingredients = request.form["ingredients"].strip().lower()
        user_ingredients = [i.strip() for i in user_ingredients.split(",")]
        recipes = load_recipes()
        results = recommend_recipes(user_ingredients, recipes)
        return render_template("index.html", results=results.to_dict("records"))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
