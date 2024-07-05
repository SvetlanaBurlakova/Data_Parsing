import requests
import pandas as pd

endpoint = "https://api.spoonacular.com/recipes/findByIngredients"
ingredients = input('Введите название ингредиентов через запятую: ')
params = {
    'ingredients' : ingredients,
    "apiKey": "46fdf8ffced74305802df0db1eedb146"
}

response = requests.get(endpoint, params=params)
if response.status_code == 200:
    print('Успешный запрос')
    recipes = response.json()
    for recipe in recipes[:1]:
        title = recipe["title"]
        usedIngredientCount = recipe["usedIngredientCount"]
        missedIngredientCount = recipe["missedIngredientCount"]
        missedIngredients = recipe["missedIngredients"]
        usedIngredients = recipe["usedIngredients"]

        print(f'Название блюда: {title}')
        print(f'Количество ингредиентов: {usedIngredientCount}')
        print(f'Количество доп.ингредиентов: {missedIngredientCount}')
        for ingredient in missedIngredients:
            print(f'Ингредиента: {ingredient["original"]}')
        for ingredient in usedIngredients:
            print(f'Ингредиента: {ingredient["original"]}')
else:
    print(f'Запрос не удался, код ошибки {response.status_code}')