import json
from flask import Flask, request, jsonify
from flask_cors import CORS

import auth
import user
import recipe
import ingredient
import admin
import search
import analysis

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def start():
    return 'it is the backend server to the recipe recommendation system'

@app.route('/auth/register', methods=['POST'])
def register():
    payload = request.json
    email = payload['email']
    username = payload['username']
    password = payload['password']
    confirmed_password = payload['confirmed_password']
    result = auth.register(email, username, password, confirmed_password)
    return jsonify(result)

@app.route('/auth/login', methods=['POST'])
def login():
    payload = request.json
    email = payload['email']
    password = payload['password']
    result = auth.login(email, password)
    return jsonify(result)

@app.route('/auth/logout', methods=['POST'])
def logout():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    result = auth.logout(user_id, token)
    return jsonify(result)

@app.route('/recipe/create', methods=['POST'])
def recipe_create():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    name = payload['name']
    image = payload['image']
    category = payload['category']
    ingredients = payload['ingredients']
    description = payload ['description']

    result = recipe.create_recipe(user_id, token, name, image, category, ingredients, description)
    return jsonify(result)

@app.route('/recipe/delete', methods=['DELETE'])
def recipe_delete():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    recipe_id = payload['recipe_id']
    result = recipe.recipe_delete(user_id, token, recipe_id)
    return jsonify(result)

# Return all recipes from database
@app.route('/recipe/show', methods=['GET'])
def recipe_show():
    result = recipe.list_recipes()
    return jsonify(result)

# Return the recipe detail given recipe_id
@app.route('/recipe/detail', methods=['GET'])
def recipe_detail():
    '''
    get values from args
    return recipe details shown in data.json
    '''
    payload = request.args
    recipe_id = payload['recipe_id']
    result = recipe.recipe_detail(recipe_id)
    return jsonify(result)

@app.route('/recipe/like', methods=['POST'])
def recipe_like():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    recipe_id = payload['recipe_id']
    result = recipe.like_recipe(user_id, token, recipe_id)
    return jsonify(result)

@app.route('/recipe/unlike', methods=['POST'])
def recipe_unlike():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    recipe_id = payload['recipe_id']
    result = recipe.unlike_recipe(user_id, token, recipe_id)
    return jsonify(result)

@app.route('/recipe/rating', methods=['POST'])
def recipe_rating():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    recipe_id = payload['recipe_id']
    rating = payload['rating']
    result = recipe.rate_recipe(user_id, token, rating, recipe_id)
    return jsonify(result)

@app.route('/recipe/collect', methods=['POST'])
def recipe_collect():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    recipe_id = payload['recipe_id']
    result = recipe.collect_recipe(user_id, token, recipe_id)
    return jsonify(result)

@app.route('/recipe/own', methods=['GET'])
def user_show_recipes():
    payload = request.args
    user_id = payload['user_id']
    result = recipe.show_own_recipes(user_id)
    return jsonify(result)

@app.route('/recipe/uncollect', methods=['POST'])
def recipe_uncollect():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    recipe_id = payload['recipe_id']
    result = recipe.uncollect_recipe(user_id, token, recipe_id)
    return jsonify(result)

@app.route('/recipe/comment', methods=['POST'])
def recipe_comment():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    recipe_id = payload['recipe_id']
    comment = payload['comment']
    result = recipe.recipe_comment(user_id, token, recipe_id, comment)
    return jsonify(result)

@app.route('/user/profile', methods=['GET'])
def user_profile():
    data = request.args
    user_id = data.get('user_id')
    result = user.show_profile(user_id)
    return jsonify(result)

@app.route('/user/change/email', methods=['PUT'])
def user_change_email():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    old_email = payload['old_email']
    new_email = payload['new_email']
    result = user.change_email(user_id, token, old_email, new_email)
    return jsonify(result)

@app.route('/user/change/password', methods=['PUT'])
def user_change_password():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    old_password = payload['old_password']
    new_password = payload['new_password']
    result = user.change_password(user_id, token, old_password, new_password)
    return jsonify(result)

@app.route('/user/change/icon', methods=['PUT'])
def user_change_icon():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    icon = payload['icon']
    result = user.change_icon(user_id, token, icon)
    return jsonify(result)

@app.route('/user/change/username', methods=['PUT'])
def user_change_username():
    payload = request.json
    user_id = payload['user_id']
    token = payload['token']
    new_name = payload['new_name']
    result = user.change_username(user_id, token, new_name)
    return jsonify(result)

@app.route('/user/follow', methods=['POST'])
def user_follow():
    payload = request.json
    curr_user_id = payload['curr_user_id']
    token = payload['token']
    target_user_id = payload['target_user_id']
    result = user.follow_user(curr_user_id, token, target_user_id)
    return jsonify(result)

@app.route('/user/unfollow', methods=['POST'])
def user_unfollow():
    payload = request.json
    curr_user_id = payload['curr_user_id']
    token = payload['token']
    target_user_id = payload['target_user_id']
    result = user.unfollow_user(curr_user_id, token, target_user_id)
    return jsonify(result)

@app.route('/user/collection', methods=['GET'])
def user_show_collection():
    payload = request.args
    user_id = payload['user_id']
    token = payload['token']
    result = user.show_collection(user_id, token)
    return jsonify(result)

@app.route('/ingredient/select', methods=['GET'])
def ingredient_select():
    name = request.args.get('name')
    result = ingredient.select_ingredient(name)
    return jsonify(result)

@app.route('/ingredient/populate', methods=['POST'])
def ingredient_populate():
    payload = request.json
    name = payload['name']
    category = payload['category']
    result = ingredient.populate_ingredient(name, category)
    return jsonify(result)

@app.route('/ingredient/show', methods=['GET'])
def ingredient_show():
    # data = request.args
    result = ingredient.get_ingredients()
    return jsonify(result)

@app.route('/recipe/search/name', methods=['POST'])
def recipes_by_name():
    payload = request.json
    recipe_name = payload['recipe_name']
    meal_type = payload['meal_type']
    sort_by = payload['sort_by']
    result = search.search_recipe_by_name(recipe_name, meal_type, sort_by)
    return jsonify(result)

@app.route('/recipe/search/ingredients', methods=['POST'])
def recipes_by_ingredients():
    payload = request.json
    ingredients = payload['ingredients'] # Given a list of ingredient names
    meal_type = payload['meal_type']
    sort_by = payload['sort_by']
    result = search.search_recipe_by_ingredients(ingredients, meal_type, sort_by)
    return jsonify(result)

@app.route('/analysis/users', methods=['GET'])
def top_five_users():
    payload = request.args
    user_id = payload['user_id']
    token = payload['token']
    result = analysis.get_five_most_followers_users(user_id, token)
    return jsonify(result)

@app.route('/analysis/recipes', methods=['GET'])
def top_five_recipes():
    payload = request.args
    user_id = payload['user_id']
    token = payload['token']
    result = analysis.get_five_most_collection_recipes(user_id, token)
    return jsonify(result)

@app.route('/analysis/ingredients', methods=['GET'])
def top_five_ingredients():
    payload = request.args
    user_id = payload['user_id']
    token = payload['token']
    result = analysis.get_ten_most_frequently_searched_set_of_ingredients(user_id, token)
    return jsonify(result)

if __name__ == '__main__':
    app.run()