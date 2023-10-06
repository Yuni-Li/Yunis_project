import admin
import recipe
import auth
from bson.objectid import ObjectId
from mongoconfig import CLIENT, DBNAME

def test_create_recipe():
    admin.clear_data()
    # Create a user
    user = auth.register('sample.user@gmail.com', 'sampleuser', 'sampleuser123', 'sampleuser123')
    user_id = user['user_id']
    token = user['token']
    # user creates a recipe
    recipe_detail = recipe.create_recipe(user_id, token, 'recipeA', '', 'A', [], '')
    recipe_id = recipe_detail['recipe_id']
    # Check recipe details
    recipes_col = CLIENT[DBNAME]['recipes']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    assert target_recipe != None

def test_list_recipes():
    admin.clear_data()
    # Create a user
    user = auth.register('sample.user@gmail.com', 'sampleuser', 'sampleuser123', 'sampleuser123')
    user_id = user['user_id']
    token = user['token']
    # user creates multiple recipes
    recipeA = recipe.create_recipe(user_id, token, 'recipeA', '', 'A', [], '')
    recipeB = recipe.create_recipe(user_id, token, 'recipeB', '', 'B', [], '')
    recipeC = recipe.create_recipe(user_id, token, 'recipeC', '', 'C', [], '')
    recipeD = recipe.create_recipe(user_id, token, 'recipeD', '', 'D', [], '')
    # Check recipes details
    recipes_col = CLIENT[DBNAME]['recipes']
    recipes_details = list(recipes_col.find())
    assert recipes_details[0]['_id'] == ObjectId(recipeA['recipe_id'])
    assert recipes_details[1]['_id'] == ObjectId(recipeB['recipe_id'])
    assert recipes_details[2]['_id'] == ObjectId(recipeC['recipe_id'])
    assert recipes_details[3]['_id'] == ObjectId(recipeD['recipe_id'])

def test_like_recipe():
    admin.clear_data()
    # Create a user
    user = auth.register('sample.user@gmail.com', 'sampleuser', 'sampleuser123', 'sampleuser123')
    user_id = user['user_id']
    token = user['token']
    # user creates a recipe
    recipe_detail = recipe.create_recipe(user_id, token, 'recipeA', '', 'A', [], '')
    recipe_id = recipe_detail['recipe_id']
    # Check recipe details
    recipes_col = CLIENT[DBNAME]['recipes']
    # User likes the recipe
    status = recipe.like_recipe(user_id, token, recipe_id)
    assert status['success']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    assert ObjectId(user_id) in target_recipe['liked_by']

def test_unlike_recipe():
    admin.clear_data()
    # Create a user
    user = auth.register('sample.user@gmail.com', 'sampleuser', 'sampleuser123', 'sampleuser123')
    user_id = user['user_id']
    token = user['token']
    # user creates a recipe
    recipe_detail = recipe.create_recipe(user_id, token, 'recipeA', '', 'A', [], '')
    recipe_id = recipe_detail['recipe_id']
    # Check recipe details
    recipes_col = CLIENT[DBNAME]['recipes']
    # User likes the recipe
    status = recipe.like_recipe(user_id, token, recipe_id)
    assert status['success']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    assert ObjectId(user_id) in target_recipe['liked_by']
    # User unlikes the recipe
    status = recipe.unlike_recipe(user_id, token, recipe_id)
    assert status['success']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    assert ObjectId(user_id) not in target_recipe['liked_by']

def test_rate_recipe():
    admin.clear_data()
    # Create two users
    user1 = auth.register('sample.user1@gmail.com', 'sampleuser1', 'sampleuser123', 'sampleuser123')
    user1_id = user1['user_id']
    token1 = user1['token']
    user2 = auth.register('sample.user2@gmail.com', 'sampleuser2', 'sampleuser223', 'sampleuser223')
    user2_id = user2['user_id']
    token2 = user2['token']
    # user creates a recipe
    recipe_detail = recipe.create_recipe(user1_id, token1, 'recipeA', '', 'A', [], '')
    recipe_id = recipe_detail['recipe_id']
    # User1 rate the recipe
    status = recipe.rate_recipe(user1_id, token1, 5, recipe_id)
    assert status['success']
    # User2 rate the recipe
    status = recipe.rate_recipe(user2_id, token2, 3, recipe_id)
    # Check recipe details
    recipes_col = CLIENT[DBNAME]['recipes']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    rating_score = target_recipe['rating']
    number_of_rating = target_recipe['number_of_rating']
    assert rating_score == 4
    assert number_of_rating == 2

def test_collect_recipe():
    admin.clear_data()
    # Create a user
    user = auth.register('sample.user@gmail.com', 'sampleuser', 'sampleuser123', 'sampleuser123')
    user_id = user['user_id']
    token = user['token']
    # user creates a recipe
    recipe_detail = recipe.create_recipe(user_id, token, 'recipeA', '', 'A', [], '')
    recipe_id = recipe_detail['recipe_id']
    # User collects recipe
    status = recipe.collect_recipe(user_id, token, recipe_id)
    assert status['success']
    # Check user and recipe details
    users_col = CLIENT[DBNAME]['users']
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })
    assert ObjectId(recipe_id) in target_user['collections']

    recipes_col = CLIENT[DBNAME]['recipes']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    assert ObjectId(user_id) in target_recipe['collected_by']
    assert target_recipe['number_of_collections'] == 1


def test_uncollect_recipe():
    admin.clear_data()
    # Create a user
    user = auth.register('sample.user@gmail.com', 'sampleuser', 'sampleuser123', 'sampleuser123')
    user_id = user['user_id']
    token = user['token']
    # user creates a recipe
    recipe_detail = recipe.create_recipe(user_id, token, 'recipeA', '', 'A', [], '')
    recipe_id = recipe_detail['recipe_id']
    # User collects recipe
    status = recipe.collect_recipe(user_id, token, recipe_id)
    assert status['success']
    # Check user and recipe details
    users_col = CLIENT[DBNAME]['users']
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })
    assert ObjectId(recipe_id) in target_user['collections']

    recipes_col = CLIENT[DBNAME]['recipes']
    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    assert ObjectId(user_id) in target_recipe['collected_by']
    assert target_recipe['number_of_collections'] == 1
    # User uncollects recipe
    status = recipe.uncollect_recipe(user_id, token, recipe_id)
    assert status['success']
    # Check user and recipe details
    target_user = users_col.find_one({
        '_id': ObjectId(user_id)
    })
    assert ObjectId(recipe_id) not in target_user['collections']

    target_recipe = recipes_col.find_one({
        '_id': ObjectId(recipe_id)
    })
    assert ObjectId(user_id) not in target_recipe['collected_by']
    assert target_recipe['number_of_collections'] == 0