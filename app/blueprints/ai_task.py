from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
import os
from . import tool
from . import point_position
import random
import json
import os
from volcenginesdkarkruntime import Ark
from datetime import datetime, timedelta
def add_value( value, volunteer):
    connection = tool.get_db_connection('users-information')
    cursor = connection.cursor(dictionary=True)
    # 明确指定列名，而不是使用url变量拼接
    sql = """
           UPDATE `volunteer` 
           SET `value` = `value` + %s  
           WHERE `card` = %s 
       """
    cursor.execute(sql, (value, volunteer))
    print(f"受影响的行数: {cursor.rowcount}")
    connection.commit()
    cursor.close()
    connection.close()
def add_task(card, longitude, latitude, type_, district, position,value,url):
    connection = tool.get_db_connection("task")
    cursor = connection.cursor()

    sql = """
        INSERT INTO task (card, type,longitude,latitude,district,position,value,url)
        VALUES (%s, %s, %s, %s, %s, %s,%s,%s)
        """
    cursor.execute(sql, (card, type_, longitude, latitude, district, position,value,url))
    connection.commit()
    cursor.close()
    connection.close()
def get_db_range_data(database, chart_name, offset, count):
    connection = tool.get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM {chart_name} WHERE status = '未开始' LIMIT {offset}, {count}"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def get_db_range_data_row(database, chart_name):
    connection = tool.get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT COUNT(*) FROM {chart_name} WHERE status = '未开始' ")
    count = cursor.fetchone()
    cursor.close()
    connection.close()
    return count






# 创建蓝图
task = Blueprint('task', __name__, url_prefix='/task')

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'webm', 'ogg'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@task.route('/data_task', methods=['POST'])
def upload_audio():
    try:

        upload_folder = os.path.join(current_app.config.get('STATIC_FOLDER', 'assets'), 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            current_app.config['UPLOAD_FOLDER'] = upload_folder


        current_app.config.setdefault('MAX_CONTENT_LENGTH', 10 * 1024 * 1024)


        if 'audioFile' not in request.files:
            return jsonify({'error': '请求中没有文件部分'}), 400

        file = request.files['audioFile']


        if file.filename == '':
            return jsonify({'error': '未选择文件'}), 400


        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)

            while os.path.exists(filepath):
                name, ext = os.path.splitext(filename)
                import re
                match = re.search(r'_(\d+)$', name)

                if match:
                    counter = int(match.group(1)) + 1
                    new_name = re.sub(r'_(\d+)$', f'_{counter}', name)
                else:
                    counter = 1
                    new_name = f"{name}_{counter}"

                filename = f"{new_name}{ext}"
                filepath = os.path.join(upload_folder, filename)


            file.save(filepath)

            return jsonify({
                'success': True,
                'message': '文件上传成功',
                'filename': filename,
                'size': os.path.getsize(filepath),  # 返回文件大小（字节）
                'path': filepath
            }), 200
        else:
            return jsonify({
                'error': f'不支持的文件类型，允许的类型：{ALLOWED_EXTENSIONS}'
            }), 400

    except Exception as e:
        current_app.logger.error(f"文件上传错误: {str(e)}")
        return jsonify({'error': '服务器处理文件时发生错误'}), 500
@task.route('/upload_task', methods=['POST'])
def upload_task():
    condition = request.get_json()
    card =condition['card']
    position =condition['position']
    longitude = position['longitude']
    latitude = position['latitude']
    point = point_position.get_address(longitude,latitude,api_key="f9d1fcc233de234630dd5f5b3e251d67")
    district =point['district']
    position =point['formatted_address']
    url = condition['url']
    tool.add_task(card, longitude, latitude, url,district,position )
    return 'ok'
@task.route('/task_list', methods=['POST'])
def show_list():
    condition = request.get_json()
    print(condition)
    page = condition['page']
    status = condition['status']
    date =condition['date']
    type_ = condition['type']
    offset = (page - 1) * 10
    rawdata = tool.get_db_range_data_for_date('task', 'task',offset,10,status,type_,date)
    feedback_list = rawdata
    for feedback in feedback_list:
        feedback['time'] = feedback['time'].strftime("%m-%d")
    return jsonify(feedback_list)
@task.route('/task_list_all', methods=[ 'POST'])
def show_list_num():
    condition = request.get_json()

    status = condition['status']
    date = condition['date']
    type_ = condition['type']

    num = tool.get_db_range_data_for_date_num('task', 'task',status,type_,date)

    return jsonify(num)

@task.route('/task_map', methods=[ 'POST'])
def show_task_map():
    condition = request.get_json()
    volunteer = condition['volunteer']
    data =tool.get_db_data('task', 'task','volunteer',volunteer)
    return jsonify(data)


@task.route('/task_mimicry', methods=[ 'POST'])
def show_task_mimicry():
    condition = request.get_json()
    print(condition)
    url = condition['url']
    data =tool.get_db_data('task', 'task','url',url)
    return jsonify(data)
@task.route('/adjust_task', methods=[ 'POST'])
def adjust_task():
    data = request.get_json()
    url =data['url']
    del data['card']
    tool.quick_modify_db_data('task', 'task',data,'url',url)
    return jsonify('ok')
@task.route('/task_volunteer', methods=[ 'POST'])
def show_volunteer():
    condition = request.get_json()
    volunteer = condition['volunteer']
    check = tool.check_value_exists('task', 'task', 'volunteer', volunteer)
    data = tool.get_db_data('task', 'task', 'volunteer', volunteer)
    time = data[0]['time']
    adjust_time = f"{time.year}年{time.month}月{time.day}日 {time.hour}时{time.minute}分{time.second}秒"
    data[0]['time'] = adjust_time
    return jsonify(data)

@task.route('/task_check', methods=[ 'POST'])
def check_volunteer():
    condition = request.get_json()
    volunteer = condition['volunteer']

    check = tool.check_value_exists('task', 'task', 'volunteer', volunteer)

    return jsonify({"status": check})
@task.route('/task_volunteer_list', methods=['GET'])
def show_volunteer_list():
    count =get_db_range_data_row('task', 'task')
    num =count['COUNT(*)']
    if num>4:
        num_round =random.randint(1, num-4)
        data =get_db_range_data('task', 'task',num_round,4)
        for i in range(0,4):
            time = data[i]['time']
            adjust_time = f"{time.year}年{time.month}月{time.day}日 {time.hour}时{time.minute}分{time.second}秒"
            data[i]['time'] = adjust_time
        return jsonify(data)
    else:
        data = get_db_range_data('task', 'task',0, num)
        for i in range(0, num):
            time = data[i]['time']
            adjust_time = f"{time.year}年{time.month}月{time.day}日 {time.hour}时{time.minute}分{time.second}秒"
            data[i]['time'] = adjust_time
        return jsonify(data)
@task.route('/task_accept', methods=['POST'])
def task_accept():
    condition = request.get_json()
    print(condition)
    url =condition['url']
    volunteer = condition['volunteer']
    check =tool.check_value_exists('task', 'task', 'volunteer', volunteer)
    print(check)
    if check:
        return 'no'
    else:
        tool.modify_db_data('task', 'task', 'volunteer', 'url', url, volunteer)
        return 'ok'

@task.route('/task_status', methods=['POST'])
def task_status():
    condition = request.get_json()
    status = condition['status']
    url  = condition['url']
    volunteer = condition['volunteer']
    print(condition)
    if status =='finish':
        param ={"url":url,'volunteer':f"{volunteer}服务",'status':'已完成'}
        tool.modify_db_data_for_dict('task', 'task','url',url,param)
        url=param['url']
        value =condition['value']
        if value is not None:
            value=float(value)
            add_value( value, volunteer)
    if status =='reject':
        param ={"url":url,'volunteer':"",'status':'未开始'}
        print(param)
        print('ok')
        tool.modify_db_data_for_dict('task', 'task','url',url,param)
    return 'ok'
@task.route('/task_map_show', methods=['GET'])
def show_map():
    rawdata = tool.get_data_limit_data('task', 'task')

    return jsonify(rawdata)
@task.route('/task_chart', methods=['GET'])
def show_chart():
    data = tool.get_db_all_data('task', 'task')
    count = tool.get_db_all_data_row('task', 'task')
    num = count['COUNT(*)']
    if num != 0:
        i = 0
        # 未处理
        type_count_pending = 0
        # 已处理
        type_count_resolved = 0
        # 拒绝
        type_count_rejected = 0
        type_count_doing = 0
        type_count_life =0
        type_count_medical = 0
        type_count_information = 0
        type_count_mood = 0
        # enum('未开始', '进行中', '已完成', '已暂停', '已取消')
        while i < num:
            if data[i]['status'] == "未开始":
                type_count_pending += 1
            elif data[i]['status'] == "已完成":
                type_count_resolved += 1
            elif data[i]['status'] == "已取消":
                type_count_rejected += 1
            elif data[i]['status'] == '进行中':
                type_count_doing += 1
            # //enum('生活事务类','健康医疗类','信息咨询类','情感社交类')
            if data[i]['type'] == "生活事务类":
                type_count_life += 1
            elif data[i]['type']  == "健康医疗类":
                type_count_medical += 1
            elif data[i]['type'] == "信息咨询类":
                type_count_information += 1
            elif data[i]['type'] == '情感社交类':
                type_count_mood += 1
            i += 1
        dict_data_card = {
            'type_count_resolved': type_count_resolved,
            'type_count_rejected': type_count_rejected,
            'type_count_doing': type_count_doing,
            'type_count_pending': type_count_pending,
            'type_count_life': type_count_life,
            'type_count_medical': type_count_medical,
            'type_count_information': type_count_information,
            'type_count_mood': type_count_mood,

        }
        return jsonify(dict_data_card)
@task.route('/task_chart_value', methods=['GET'])
def show_chart_value():
    data = tool.get_top5_largest('users-information', 'volunteer', 'value')
    return jsonify(data)
@task.route('/sos', methods=['POST'])
def sos():
    condition = request.get_json()
    print(condition)
    card = condition['card']
    position = condition['position']
    longitude = position['longitude']
    latitude = position['latitude']
    url = condition['url']
    point = point_position.get_address(longitude, latitude, api_key="f9d1fcc233de234630dd5f5b3e251d67")
    district = point['district']
    address_position = str(point['formatted_address'])
    type_ = "紧急"
    district_str = str(district)
    print(district)
    add_task(card, longitude, latitude, type_, district_str, address_position,500,url)
    return 'ok'
@task.route('/sos_show', methods=['POST'])
def sos_show():
    condition = request.get_json()
    card = condition['card']
    url = condition['url']
    position = condition['position']
    longitude = position['longitude']
    latitude = position['latitude']
    point = point_position.get_address(longitude, latitude, api_key="f9d1fcc233de234630dd5f5b3e251d67")
    district = str(point['district'])
    position = str(point['formatted_address'])
    type_ = "紧急"

    add_task(card, longitude, latitude, type_, district, position,500,url)
    return 'ok'
@task.route('/my_task', methods=['POST'])
def my_task():
    condition = request.get_json()
    card = condition['card']

    def get_db_data(database, chart_name, column, group):
        connection = tool.get_db_connection(database)
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT * FROM {chart_name} WHERE {column} = %s ORDER BY time DESC"
        cursor.execute(query, (group,))
        data = cursor.fetchall()

        for item in data:
            if 'time' in item and item['time'] is not None:
                if isinstance(item['time'], str):
                    time_obj = datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S')
                else:
                    time_obj = item['time']
                item['time'] = time_obj.strftime('%Y年%m月%d日 %H时%M分%S秒')
        cursor.close()
        connection.close()
        return data
    task_data =get_db_data('task', 'task',"card",card)
    feedback_data=get_db_data('feedback', 'user_feedback',"card",card)
    data =task_data+feedback_data
    return jsonify(data)
@task.route('/ai', methods=['POST'])
def ai():
    condition = request.get_json()
    client = Ark(api_key=os.environ.get("ARK_API_KEY"))

    print(condition)
    completion = client.chat.completions.create(
        model="doubao-seed-1-6-250615",
        messages=[

            {"role": "system", "content": "你是一个武汉gis数据分析师，你要出一个分析建议，净量和老年人有关用不超过300个字回答问题。"},
            # 用户的实际问题
            {"role": "user","content": condition }
        ]
    )

    print(completion.choices[0].message.content)
    return jsonify(completion.choices[0].message.content)

