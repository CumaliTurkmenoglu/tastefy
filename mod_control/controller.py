from flask import Blueprint,request,jsonify,abort
from flask_jwt_extended import jwt_required,get_jwt_identity


mod_controller = Blueprint('control',__name__)



@mod_controller.route('/get_unlabelled_foods', methods=['POST'])
@jwt_required()
def getUnlabelledFoods():
    if request.method == "POST":
        from mod_user_foods.model import  getUnlabelledFoodsByUserId
        import json
        req_json = request.json
        current_user = get_jwt_identity()
#        current_user = current_user.split("*")
        userId = req_json['userId']

        dict_ = {'Data': []}
        for i in getUnlabelledFoodsByUserId(userId):
            foods_dict = {'id':'',
                            'userId':'',
                            'userName':'',
                            'foodId':'',
                            'foodName':'',
                            'preference':''
                         }

            foods_dict['id']= i.id
            foods_dict['userId']= i.userId
            foods_dict['userName']= i.userName
            foods_dict['foodId']= i.foodId
            foods_dict['foodName']= i.foodName
            foods_dict['preference'] = i.preference

            dict_['Data'].append(foods_dict)
        return jsonify(json.loads(json.dumps({'Data':dict_['Data']},default=str)))


@mod_controller.route('/get_foods', methods=['POST'])
@jwt_required()
def getFoods():
    if request.method == "POST":
        from mod_foods.model import get_foods_by_category
        import json
        req_json = request.json
        current_user = get_jwt_identity()
        current_user = current_user.split("*")
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
        current_user = get_jwt_identity()
#        current_user = current_user.split("*")
        userId = req_json['userId']
        foodId = req_json['foodId']
        preference = req_json['preference']
        insert=set_food_preference(userId,foodId,preference)
        if insert:
            return jsonify({'Status': 'Success',
                            'Message': 'The preference has been set for the food.'})
        else:
            return jsonify({'Status' : 'Fail',
                            'Message': 'The preference couldn\'t be set.'})


