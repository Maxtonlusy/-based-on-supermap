from flask import Blueprint ,jsonify,request
from . import  tool
from . import  health_tool
from . import  point_position
health_page = Blueprint('health_page', __name__ , url_prefix='/health_page')
@health_page.route('/health_record', methods=[ 'POST'])
def show_data():
    condition = request.get_json()
    list_ =condition['list']
    print(condition)
    page = condition['page']
    offset = (page - 1) * 5
    rawdata = tool.get_db_range_data_('health_record','record',offset,5,list_)
    count = tool.get_db_range_data_row('health_record', 'record',list_)
    print('iii')
    print(count)
    data = rawdata + [count]
    print(data)
    return jsonify(data)
def get_db_range_data_for_all(database, chart_name, list_):
    connection = tool.get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    if not list_:
        data = tool.get_db_all_data(database, chart_name)
        return data
    placeholders = ', '.join(['%s'] * len(list_))
    query = f"SELECT * FROM {chart_name} WHERE card IN ({placeholders}) "
    cursor.execute(query, list_)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data
@health_page.route('/card', methods=['GET'])
def create_card():
    data = tool.generate_card_number()
    return jsonify(data)
@health_page.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    position =data["position"]
    card =data['card']
    name = data['name']
    status = data['status']
    area =data['area']
    dict_user ={'card': card, 'name': name, 'status': status,'password':'123456','position':position,"area":area}
    tool.create_user(dict_user, 'health_record', 'record')
    return jsonify('okok')
@health_page.route('/chart_cloud', methods=['GET'])
def create_chart():

    data = health_tool.count_occurrences_in_db('health_record', 'record', 'disease')
    return jsonify(data)

@health_page.route('/chart_health', methods=['GET'])
def create_chart_health():
    data = health_tool.count_occurrences_in_db('health_record', 'record', 'status')
    print(data)
    return jsonify(data)
@health_page.route('/hp_map_health', methods=['GET'])
def hp_point():
    data = tool.get_db_all_data('point', 'hospital')
    return jsonify(data)
@health_page.route('/hp_map_health_rural', methods=['GET'])
def hp_point_rural():
    data = tool.get_db_all_data('point', 'rural_hospital')
    return jsonify(data)
@health_page.route('/dang', methods=['GET'])
def hp_point_dang():
    data = tool.get_db_all_data('point', 'dang')
    print(data)
    return jsonify(data)
@health_page.route('/institution', methods=['GET'])
def hp_point_institution():
    data = tool.get_db_all_data('point', 'institution')
    print(data)
    return jsonify(data)
@health_page.route('/position', methods=['POST'])
def get_position():
    condition = request.get_json()
    point =point_position.get_location(condition,'武汉',api_key="f9d1fcc233de234630dd5f5b3e251d67")
    return jsonify(point)
@health_page.route('/position_name', methods=['POST'])
def get_position_name():
    condition = request.get_json()
    lat =condition['lat']
    lng = condition['lng']
    point =point_position.get_address(lng,lat,api_key="f9d1fcc233de234630dd5f5b3e251d67")
    point['formatted_address'] = point['formatted_address'].replace("湖北省武汉市", "")
    return jsonify(point)


@health_page.route('/all', methods=['POST'])
def get_data():
    condition = request.get_json()
    list_ =condition['list']
    data =get_db_range_data_for_all('health_record', 'record',list_)
    print(data)
    status = {
        '健康': 0,
        '不健康': 0,
        '亚健康': 0,
        '慢性呼吸系统疾病': 0,
        '心脑血管疾病': 0,
        '骨骼与关节疾病': 0,
        '神经系统退行性疾病': 0
    }
    for i in data:
        if i['status'] == '健康':
            status['健康'] += 1
        elif i['status'] == '不健康':
            status['不健康'] += 1
        elif i['status'] == '亚健康':
            status['亚健康'] += 1
        if i['disease'] == '慢性呼吸系统疾病':
            status['慢性呼吸系统疾病'] += 1
        elif i['disease'] == '心脑血管疾病':
            status['心脑血管疾病'] += 1
        elif i['disease'] == '骨骼与关节疾病':
            status['骨骼与关节疾病'] += 1
        elif i['disease'] == '神经系统退行性疾病':
            status['神经系统退行性疾病'] += 1
    print(status)
    return jsonify(status)
@health_page.route('/status', methods=['POST'])
def hp_point_status():
    condition = request.get_json()
    card =condition['card']
    data = tool.get_db_data('health_record','record','card',card)
    print(data)
    return jsonify(data)