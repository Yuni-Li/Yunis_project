# Helper functions
def is_valid_email(email):
    return True

def is_valid_password(password):
    return True

def is_valid_image(image):
    return True

def stringify_recipe(recipe):
    '''
    Convert all the parameters in recipe to string
    '''

    # Convert _id and created_by
    recipe['_id'] = str(recipe['_id'])
    recipe['created_by'] = str(recipe['created_by'])

    # Convert all the data(user id) in liked_by and collected_by
    liked_by = recipe['liked_by']
    collected_by = recipe['collected_by']
    for i in range(len(liked_by)):
        liked_by[i] = str(liked_by[i])
    for i in range(len(collected_by)):
        collected_by[i] = str(collected_by[i])

    # Convert rating to integer
    # If 1 > decimal > 0.75, count it as 1,
    # If 0.75 >= decimal > 0.25, count it as 0.5,
    # if 0.25 >= decimal > 0, count it as 0
    rating = recipe['rating']
    rating_int = int(rating)
    rating_decimal = rating - rating_int
    if rating_decimal > 0.75:
        rating = rating_int + 1
    elif rating_decimal > 0.25:
        rating = rating_int + 0.5
    else:
        rating = rating_int
    recipe['rating'] = round(rating, 1)

    return recipe

def ingredients_to_key(ingredients):
    pass