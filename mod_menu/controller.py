import random

from flask import Blueprint,request,jsonify
from flask_jwt_extended import get_jwt_identity

mod_menu = Blueprint('menu',__name__)


@mod_menu.route('/get_unlabelled_menus', methods=['POST'])
def getUnlabelledMenus():
    if request.method == "POST":
        from sqlalchemy import func
        from mod_menu.model import  getUnlabelledMenusByUserId,extractFoodNamesAndObjValues, extractObjectives, extractNutrientValues
        import json
        req_json = request.json
        #        current_user = get_jwt_identity()
        #        current_user = current_user.split("*")
        userId = req_json['userId']

        dict_ = {"Menus": []}
        menus=getUnlabelledMenusByUserId(userId)
        random.shuffle(menus)
        for i in menus:
            menu_dict = {"id":"",
                         "experiment":"",
                         "foodNumber":"",
                         "userId":"",
                         "violated": "",
                         "objectives": "",
                         "foods":"",
                         "nutrients":"",
                         }
            menu_dict["id"] = i.id
            menu_dict["experiment"] = i.experiment
            menu_dict["foodNumber"] = i.foodNumber
            menu_dict["userId"] = i.userId
            menu_dict["violated"] = i.violated
            menu_dict["objectives"] = extractObjectives(i.objectives) #as list
            menu_dict["foods"] = extractFoodNamesAndObjValues(i)
            menu_dict["nutrients"] = extractNutrientValues(i)

            dict_["Menus"].append(menu_dict)
        return jsonify({'Menus': dict_['Menus']})







