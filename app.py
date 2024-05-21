from flask import Flask, request, jsonify, render_template
# from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import AutoTokenizer, AutoModelWithLMHead
import torch

app = Flask(__name__)

# Load the LLaMA3 model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained('EleutherAI/gpt-neo-2.7B')
# model = AutoModelForCausalLM.from_pretrained('EleutherAI/gpt-neo-2.7B')
tokenizer = AutoTokenizer.from_pretrained('gpt2')
model = AutoModelWithLMHead.from_pretrained('gpt2')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()

    ingredients = data.get('ingredients', [])
    cuisine = data.get('cuisine', 'Italian')  # Default cuisine is Italian

    # # Here you would fetch the recipe based on the ingredients and cuisine
    # # For now, let's just return a dummy recipe
    # recipe = generate_dummy_recipe(ingredients, cuisine)


    # json_recipe = dict()
    # json_recipe['recipe'] = recipe['instructions']


    # return json_recipe
    print('Running....')

    if not ingredients or not cuisine:
        return jsonify({'error': 'Ingredients and cuisine type are required.'}), 400

    prompt = f"Create a {cuisine} recipe using the following ingredients: {', '.join(ingredients)}."

    try:
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
        outputs = model.generate(inputs['input_ids'], max_length=200, num_return_sequences=1)

        recipe = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        return jsonify({'recipe': recipe})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
