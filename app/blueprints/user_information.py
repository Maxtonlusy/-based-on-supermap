from flask import Blueprint ,jsonify,request

from . import tool
user_information = Blueprint('user_information', __name__  ,url_prefix='/user')

@user_information.route('/user_health', methods=['POST'])
def get_user():
        condition = request.get_json()
        card =condition['card']
        print(card)
        data =tool.get_db_data('health_record','record','card',card)
        del data[0]["password_hash"]

        return jsonify(data)













@user_information.route('/information_user', methods=['POST'])
def user_information_show ():
        condition = request.get_json()
        print(condition)
        card = condition['card']
        data = tool.get_db_data('users-information', 'users', 'card', card)
        return jsonify(data)
@user_information.route('/volunteer_information', methods=['POST'])
def volunteer_information_show ():
        condition = request.get_json()
        print(condition)
        card = condition['card']
        print(card)
        data = tool.get_db_data('users-information', 'volunteer', 'card', card)
        return jsonify(data)

@user_information.route('/adjust_volunteer', methods=['POST'])
def adjust_volunteer ():
        condition = request.get_json()
        card =condition['card']
        password_hash = condition['password_hash']
        if password_hash==None:
                condition['password_hash']="123456"
        tool.modify_db_data_for_dict('users-information','volunteer','card',card,condition)
        return jsonify('ok')
@user_information.route('/adjust_user', methods=['POST'])
def adjust ():
        condition = request.get_json()
        card =condition['card']
        password_hash =condition['password_hash']
        if password_hash==None:
                condition['password_hash']="123456"
        print(condition)
        tool.modify_db_data_for_dict('health_record','record','card',card,condition)
        return jsonify('ok')
@user_information.route('/adjust_admin', methods=['POST'])
def adjust_admin ():
        condition = request.get_json()
        print(condition)
        card =condition['card']
        check = tool.check_value_exists('users-information', 'users', 'card', card)
        if check==False:
                return jsonify('no')
        else:
                tool.modify_db_data_for_dict('users-information','users','card',card,condition)
                return jsonify('yes')



@user_information.route('/add_admin', methods=['POST'])
def add_admin ():
        condition = request.get_json()
        card =condition['card']
        check = tool.check_value_exists('users-information','users', 'card' ,card)
        if check==False:
                tool.create_user(condition, 'users-information', 'users')
                return jsonify('ok')
        else:
                return jsonify('no')

@user_information.route('/del_admin', methods=['POST'])
def del_admin ():
        condition = request.get_json()
        card =condition['card']
        print(condition)
        check = tool.check_value_exists('users-information','users', 'card' ,card)
        if check==False:
                return jsonify('no')
        else:
                tool.del_user(condition,'users-information','users')
                return jsonify('yes')
