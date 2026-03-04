
from flask import Blueprint ,jsonify,request

from . import tool
home_page = Blueprint('home_page', __name__  ,url_prefix='/home_page')
@home_page.route('/chart_show', methods=['POST'])
def show_data():
    condition = request.get_json()
    area = condition.get('area')
    rawdata = tool.get_db_data('chart_data','wuhan','area',area)
    print(rawdata)
    return jsonify(rawdata)

@home_page.route('/chart_demand', methods=['GET'])
def chart_data():
    list_data= ["volunteer", "medical", "comfort", "live"]
    rawdata =tool.get_db_some_data('chart_data', 'chartdata_demand',list_data)
    return jsonify(rawdata)
@home_page.route('/header', methods=['POST'])
def avatar_data():
    condition = request.get_json()
    card = condition.get('card')
    rawdata = tool.get_db_data('health_record', 'record', 'card', card)
    del rawdata[0]["password_hash"]
    return jsonify(rawdata)
@home_page.route('/bus', methods=['GET'])
def bus_data():
    data=tool.get_db_all_data('point','bus')
    return jsonify(data)