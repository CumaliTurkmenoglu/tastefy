import random

from flask import Blueprint,request,jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

mod_menu = Blueprint('menu',__name__)


@mod_menu.route('/get_unlabelled_menus', methods=['POST'])
@jwt_required()
def getUnlabelledMenus():
    if request.method == "POST":
        from mod_menu.model import  getUnlabelledMenusByUserId,extractFoodNamesAndObjValues, extractObjectives, extractNutrientValues
        from mod_user.controller import protected
        current_user = protected(get_jwt_identity())
        user_id=current_user[0].json["user_id"]

        dict_ = {"Menus": []}
        menus=getUnlabelledMenusByUserId(user_id)
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
            breakfast, lunchdinner= extractFoodNamesAndObjValues(i)
            menu_dict["breakfast"] = breakfast
            menu_dict["lunchdinner"] = lunchdinner
            menu_dict["nutrients"] = extractNutrientValues(i)

            dict_["Menus"].append(menu_dict)
        return jsonify({'Menus': dict_['Menus']})







