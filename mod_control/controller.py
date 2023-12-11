from flask import Blueprint,request,jsonify,abort
from flask_jwt_extended import jwt_required,get_jwt_identity

mod_controller = Blueprint('control',__name__)

@mod_controller.route('/get_unlabelled_foods', methods=['POST'])
@jwt_required()
def getUnlabelledFoods():
    if request.method == "POST":
        from mod_user_foods.model import  get_unlabelled_foods_by_user_id
        from mod_food_ingredients.model import get_food_ingredient_by_food_id, get_ingredients_by_food_ids
        from mod_food_nutrients.model import get_nutrients_by_food_id, get_nutrients_by_food_ids
        import json
        from mod_user.controller import protected
        current_user = protected(get_jwt_identity())
        user_id=current_user[0].json["user_id"]

        foods=get_unlabelled_foods_by_user_id(user_id)
#        food_ids= [food.foodId for food in foods]
        from flask import jsonify

        # Create dictionaries to organize the data
        food_dict = {}
        nutrients_dict = {}
        ingredients_dict = {}

        for food_id, food_name, preference, nutrient_name, nutrient_quantity, ingredient_name, ingredient_quantity, unit_name in foods:
            if food_id not in food_dict:
                food_dict[food_id] = {
                    'id': food_id,
                    'name': food_name,
                    'preference': preference,
                    'nutrients': [],
                    'ingredients': []
                }

            # Add nutrient information
            nutrient_key = (food_id, nutrient_name, unit_name)
            if nutrient_key not in nutrients_dict:
                nutrients_dict[nutrient_key] = {
                    'name': nutrient_name,
                    'quantity': nutrient_quantity,
                    'unit': unit_name
                }
                food_dict[food_id]['nutrients'].append(nutrients_dict[nutrient_key])

            # Add ingredient information
            ingredient_key = (food_id, ingredient_name)
            if ingredient_key not in ingredients_dict:
                ingredients_dict[ingredient_key] = {
                    'name': ingredient_name,
                    'quantity': ingredient_quantity
                }
                food_dict[food_id]['ingredients'].append(ingredients_dict[ingredient_key])

        # Convert the dictionary to a list to get the final JSON object
        food_list = list(food_dict.values())

        # Convert the list to a JSON object
        import json
        food_json = json.dumps(food_list, indent=2, ensure_ascii=False)

        return food_json#jsonify(json.loads(json.dumps({'Data':dict_['Data']},default=str)))


@mod_controller.route('/get_foods', methods=['POST'])
@jwt_required()
def getFoods():
    if request.method == "POST":
        from mod_foods.model import get_foods_by_category
        import json
        req_json = request.json
        foodGroupId = req_json['foodGroupId']
        dict_ = {'Data': []}
        for i in get_foods_by_category(foodGroupId):
            foods_dict = {'id':'',
                            'name':'',
                            'foodGroupId':'',
                            'caseStudy':'',
                            'portion':'',
                            'cost':'',
                            'preference':'',
                            'preference2':'',
                            'preparingTime':'',
                            'cookingTime':'',
                            'rating':'',
                            'co2':'',
                            'availability':'',
                            'picUrl':'',
                            'nameRoots':'',
                         }

            foods_dict['id']= i.id
            foods_dict['name']  = i.name
            foods_dict['foodGroupId'] = i.foodGroupId
            foods_dict['caseStudy'] = i.caseStudy
            foods_dict['portion'] = i.portion
            foods_dict['cost'] = i.cost
            foods_dict['preference'] = i.preference
            foods_dict['preference2'] = i.preference2
            foods_dict['preparingTime'] = i.preparingTime
            foods_dict['cookingTime'] = i.cookingTime
            foods_dict['rating'] = i.rating
            foods_dict['co2']  = i.co2
            foods_dict['availability'] = i.availability
            foods_dict['picUrl'] = i.picUrl
            foods_dict['nameRoots']     = i.nameRoots

            dict_['Data'].append(foods_dict)
        return jsonify(json.loads(json.dumps({'Data':dict_['Data']},default=str)))


@mod_controller.route('/set_food_preference', methods=['POST'])
@jwt_required()
def set_food_preference():
    if request.method == "POST":
        from mod_user_foods.model import  set_food_preference
        import json
        req_json = request.json
        from mod_user.controller import protected
        current_user = protected(get_jwt_identity())
        user_id=current_user[0].json["user_id"]
        foodId = req_json['foodId']
        preference = req_json['preference']
        insert=set_food_preference(user_id,foodId,preference)
        if insert:
            return jsonify({'Status': 'Success',
                            'Message': 'The preference has been set for the food.'})
        else:
            return jsonify({'Status' : 'Fail',
                            'Message': 'The preference couldn\'t be set.'})

@mod_controller.route('/set_menu_preference', methods=['POST'])
@jwt_required()
def set_menu_preference():
    if request.method == "POST":
        from mod_chosen_menu.model import  set_menu_preference
        import json
        req_json = request.json
        from mod_user.controller import protected
        current_user = protected(get_jwt_identity())
        user_id=current_user[0].json["user_id"]
        menuId = req_json['menuId']
        preference = req_json['preference']
        insert=set_menu_preference(user_id,menuId,preference)
        if insert:
            return jsonify({'Status': 'Success',
                            'Message': 'The preference has been set for the Menu.'})
        else:
            return jsonify({'Status' : 'Fail',
                            'Message': 'The preference couldn\'t be set.'})



@mod_controller.route('/reset_food_preference', methods=['POST'])
@jwt_required()
def reset_food_preference():
    if request.method == "POST":
        from mod_user_foods.model import  reset_food_preference
        import json
        req_json = request.json
        from mod_user.controller import protected
        current_user = protected(get_jwt_identity())
        user_id=current_user[0].json["user_id"]
        foodId = req_json['foodId']
        remove=reset_food_preference(user_id,foodId)
        if remove:
            return jsonify({'Status': 'Success',
                            'Message': 'The preference has been deleted for the food.'})
        else:
            return jsonify({'Status' : 'Fail',
                            'Message': 'The preference couldn\'t be deleted.'})

@mod_controller.route('/reset_menu_preference', methods=['POST'])
@jwt_required()
def reset_menu_preference():
    if request.method == "POST":
        from mod_chosen_menu.model import  reset_menu_preference
        import json
        req_json = request.json
        from mod_user.controller import protected
        current_user = protected(get_jwt_identity())
        user_id=current_user[0].json["user_id"]
        menuId = req_json['menuId']
        remove=reset_menu_preference(user_id,menuId)
        if remove:
            return jsonify({'Status': 'Success',
                            'Message': 'The preference has been deleted for the Menu.'})
        else:
            return jsonify({'Status' : 'Fail',
                            'Message': 'The preference couldn\'t be deleted.'})

