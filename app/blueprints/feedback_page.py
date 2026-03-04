from flask import Blueprint ,jsonify,request
from datetime import datetime, timedelta
from . import tool

# import jieba
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer

feedback_page = Blueprint('feedback_page', __name__ , url_prefix='/feedback_page')
@feedback_page.route('/feedback_card', methods=['GET'])
def show_data():
    data = tool.get_db_all_data('feedback', 'user_feedback')
    count =tool.get_db_all_data_row('feedback', 'user_feedback')
    num =count['COUNT(*)']
    print(num)

    if num != 0:
        i = 0
        # 未处理
        type_count_pending = 0
        # 已处理
        type_count_resolved = 0
        # 拒绝
        type_count_rejected = 0
        type_count_comment = 0
        while i < num:
            if data[i]['status'] == "pending":
                type_count_pending += 1
            elif data[i]['status'] == "resolved":
                type_count_resolved += 1
            elif data[i]['status'] == "rejected":
                type_count_rejected += 1
            elif data[i]['comment'] == 'bad':
                type_count_comment += 1
            i += 1
        reject_ratio_raw = type_count_rejected / num *100
        reject_ratio = round(reject_ratio_raw,1)
        bad_comment_ratio_raw = type_count_comment / num *100
        bad_comment_ratio = round(bad_comment_ratio_raw,1)
        dict_data_card = {}
        dict_data_card['type_count_resolved'] = type_count_resolved
        dict_data_card['reject_ratio'] =reject_ratio
        dict_data_card['bad_comment_ratio']= bad_comment_ratio
        dict_data_card['type_count_pending'] =type_count_pending
        return jsonify(dict_data_card)
    else:
        dict_data_card = {}
        dict_data_card['type_count_resolved'] = 0
        dict_data_card['reject_ratio'] = 0
        dict_data_card['bad_comment_ratio'] =0
        dict_data_card['type_count_pending'] = 0
        return jsonify(dict_data_card)

@feedback_page.route('/feedback_list', methods=['POST'])
def show_list():
    condition = request.get_json()
    page = condition['page']
    status = condition['status']
    date =condition['date']
    type_ = condition['type']
    offset = (page - 1) * 10
    rawdata = tool.get_db_range_data_for_date('feedback', 'user_feedback',offset,10,status,type_,date)
    feedback_list = rawdata
    for feedback in feedback_list:
        feedback['time'] = feedback['time'].strftime("%m-%d")
    return jsonify(feedback_list)
@feedback_page.route('/feedback_list_all', methods=[ 'POST'])
def show_list_num():
    condition = request.get_json()
    print(condition)
    status = condition['status']
    date = condition['date']
    type_ = condition['type']
    print(status)
    num = tool.get_db_range_data_for_date_num('feedback', 'user_feedback',status,type_,date)
    print(num)
    return jsonify(num)
@feedback_page.route('/feedback_map', methods=['GET'])
def show_map():
    def get_db_all_data(database, chart_name):
        connection = tool.get_db_connection(database)
        cursor = connection.cursor(dictionary=True)

        today_start = datetime.now().strftime('%Y-%m-%d 00:00:00')

        query = f"SELECT * FROM {chart_name} WHERE time >= '{today_start}'"

        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        return data
    rawdata = get_db_all_data('feedback', 'user_feedback')
    feedback_list = rawdata
    for feedback in feedback_list:
        feedback['time'] = feedback['time'].strftime("%m-%d")
    return jsonify(feedback_list)
@feedback_page.route('/feedback_mimicry', methods=[ 'POST'])
def show_task_mimicry():
    condition = request.get_json()
    card = condition['card']
    data =tool.get_db_data('feedback', 'user_feedback','card',card)
    return jsonify(data)
@feedback_page.route('/adjust_feedback', methods=[ 'POST'])
def adjust_feedback():
    data = request.get_json()
    card =data['card']
    print(card)
    print(data)
    print('qqq')
    tool.quick_modify_db_data('feedback', 'user_feedback',data,'card',card)
    return jsonify('ok')

@feedback_page.route('/add_feedback', methods=[ 'POST'])
def add_feedback():
    condition = request.get_json()
    print(condition)
    card = condition['card']
    name = condition['name']
    content= condition['content']
    title =condition['title']
    position = condition['position']
    longitude = position['longitude']
    latitude = position['latitude']
    tool.add_feedback('feedback', card,name,content,title, longitude,latitude, 'pending')
    return jsonify('ok')




