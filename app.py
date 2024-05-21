from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()

    ingredients = data.get('ingredients', [])
    cuisine = data.get('cuisine', 'Italian')  # Default cuisine is Italian

    # Here you would fetch the recipe based on the ingredients and cuisine
    # For now, let's just return a dummy recipe
    recipe = generate_dummy_recipe(ingredients, cuisine)

    return jsonify(recipe)

def generate_dummy_recipe(ingredients, cuisine):
    # Dummy function to generate a recipe
    if cuisine == 'Italian':
        recipe = {
            'name': 'Spaghetti Carbonara',
            'ingredients': ['spaghetti', 'eggs', 'pancetta', 'parmesan cheese'],
            'instructions': 'Cook spaghetti; mix eggs, pancetta, and cheese; combine and serve.'
        }
    elif cuisine == 'Indian':
        recipe = {
            'name': 'Chicken Tikka Masala',
            'ingredients': ['chicken', 'tomato sauce', 'spices', 'cream'],
            'instructions': 'Marinate chicken; grill; simmer in sauce with spices and cream.'
        }
    elif cuisine == 'Chinese':
        recipe = {
            'name': 'Kung Pao Chicken',
            'ingredients': ['chicken', 'peanuts', 'vegetables', 'soy sauce'],
            'instructions': 'Stir-fry chicken and vegetables; add soy sauce and peanuts; serve.'
        }
    else:
        recipe = {
            'name': 'Recipe Not Found',
            'ingredients': [],
            'instructions': 'No recipe found for the selected cuisine.'
        }

    return recipe

if __name__ == '__main__':
    app.run(debug=True)
