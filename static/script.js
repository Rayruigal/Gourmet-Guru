document.getElementById('recipeForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const ingredients = document.getElementById('ingredients').value.split(',').map(item => item.trim());
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
        if (data.recipe) {
            document.getElementById('recipeResult').innerText = data.recipe;
        } else {
            document.getElementById('recipeResult').innerText = 'Error: ' + data.error;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('recipeResult').innerText = 'Error: Could not generate recipe.';
    });
});
