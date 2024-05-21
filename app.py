from flask import Flask, request, jsonify, render_template, send_from_directory
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from transformers import AutoTokenizer, AutoModelWithLMHead
# import torch
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the LLaMA3 model and tokenizer
# tokenizer = AutoTokenizer.from_pretrained('EleutherAI/gpt-neo-2.7B')
# model = AutoModelForCausalLM.from_pretrained('EleutherAI/gpt-neo-2.7B')
# # tokenizer = AutoTokenizer.from_pretrained('gpt2')
# # model = AutoModelWithLMHead.from_pretrained('gpt2')

@app.route('/')
def index():
    # return render_template('index_1.html') # input ingredients, select Cuisine Type
    # return render_template('index_2.html') # input ingredients, and Cuisine Type as a free choice
    # return render_template('index_3.html') # input ingredients, and Cuisine Type as a free choice, centerlize the box
    # return render_template('index_4.html') # enable upload a photo in the end
    # return render_template('index_5.html') # display the uploaded photo on the URL
    return render_template('index.html') # display the uploaded photo on the URL


@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()

    ingredients = data.get('ingredients', [])
    cuisine = data.get('cuisine', 'Italian')  # Default cuisine is Italian

    # Here you would fetch the recipe based on the ingredients and cuisine
    # For now, let's just return a dummy recipe
    recipe = generate_dummy_recipe(ingredients, cuisine)


    json_recipe = dict()
    json_recipe['recipe'] = recipe['instructions']

    return json_recipe



    # print('Running....')

    # if not ingredients or not cuisine:
    #     return jsonify({'error': 'Ingredients and cuisine type are required.'}), 400

    # prompt = f"Create a {cuisine} recipe using the following ingredients: {', '.join(ingredients)}."
    # print(prompt)

    # try:
    #     inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    #     outputs = model.generate(inputs['input_ids'], max_length=200, num_return_sequences=1)

    #     recipe = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    #     print(recipe)
    #     return jsonify({'recipe': recipe})

    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No photo part in the request'}), 400
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        photo_url = f"/uploads/{file.filename}"
        return jsonify({'photo_url': photo_url})
    return jsonify({'error': 'File upload failed'}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/rate_recipe', methods=['POST'])
def rate_recipe():
    data = request.get_json()
    rating = data.get('rating')
    
    if rating not in [1, 2, 3, 4, 5]:
        return jsonify({'error': 'Invalid rating. Must be between 1 and 5.'}), 400
    
    # Here, you could save the rating to a database or perform other actions
    print(f'Received rating: {rating}')
    
    return jsonify({'message': 'Rating received successfully!'})


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
