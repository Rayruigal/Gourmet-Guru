document.getElementById('recipeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const ingredientsInput = document.getElementById('ingredients').value;
    const ingredients = ingredientsInput.split(',').map(item => item.trim());
    const cuisine = document.getElementById('cuisine').value;

    fetch('/generate_recipe', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            ingredients: ingredients,
            cuisine: cuisine
        })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('recipeResult');
        if (data.recipe) {
            resultDiv.innerText = data.recipe;
        } else {
            resultDiv.innerText = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('recipeResult').innerText = 'Error: Could not generate recipe.';
    });
});
