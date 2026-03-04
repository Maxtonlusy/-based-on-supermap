import time
import random
import mysql.connector
import bcrypt
from datetime import datetime, timedelta

user_data_id  = [
    "username",
    "password_hash",
    "realname",
    "age",
    "gender",
    "phonenumber",
    "email",
    "address",
    "role",
    "user_avatar"
]
def create_password_hash(data):
    print(data)
    password = data['password']
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(password_bytes, salt)
    data['password_hash'] = hash_bytes.decode('utf-8')
    del data['password']
    return data






def get_column_total( database, table_name, column_name, condition=None):
        connection = get_db_connection(database)
        cursor = connection.cursor()
        # 构建查询语句
        query = f"SELECT SUM({column_name}) AS total FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"

        # 执行查询
        cursor.execute(query)

        # 获取结果
        result = cursor.fetchone()
        total = result[0] if result[0] is not None else 0

        print(f"{column_name}列的总计值为: {total}")


        cursor.close()
        connection.close()
        return total





def create_user(rawdata, database, chartname):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    data = create_password_hash(rawdata)
    values = list(data.values())
    columns = list(data.keys())

    escaped_table_name = f"`{database}`.`{chartname}`"
    column_names = ", ".join([f"`{col}`" for col in columns])
    placeholders = ", ".join(["%s"] * len(values))
    sql = f"""
        INSERT INTO {escaped_table_name} ({column_names})
        VALUES ({placeholders})
    """
    cursor.execute(sql, tuple(values))
    connection.commit()
    cursor.close()
    connection.close()






def del_user(data, database, chartname):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    key = next(iter(data.keys()))
    value = next(iter(data.values()))
    sql = f'DELETE FROM {chartname} WHERE {key} =%s;'
    cursor.execute(sql, (value,))
    connection.commit()
    cursor.close()
    connection.close()




def add_column(database, chartname,column_name,data_list):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    placeholders = ', '.join(['%s'] * len(data_list))
    query = f"INSERT INTO {chartname} ({column_name}) VALUES ({placeholders})"
    values = [(data,) for data in data_list]
    cursor.executemany(query, values)
    connection.commit()










def get_db_connection(database):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="192206.q",
            database=database
        )
        return connection
    except mysql.connector.Error as e:
        print(f"数据库连接错误: {e}")
        return None

def get_db_data(database,chart_name,column,group):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM {chart_name} WHERE {column} = %s"
    cursor.execute(query, (group,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def get_db_data_for_old_chart(database, chart_name, column, group, field1, field2):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT {field1}, {field2} FROM {chart_name} WHERE {column} = %s"
    cursor.execute(query, (group,))
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def modify_db_data(database,chart_name,target_column,match_column,match_value,new_value):
    if target_column == 'password_hash':
        password = new_value
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash_bytes = bcrypt.hashpw(password_bytes, salt)
        new_value = hash_bytes.decode('utf-8')
        connection = get_db_connection(database)
        cursor = connection.cursor(dictionary=True)
        sql = (f"UPDATE {chart_name} "
               f"SET password_hash = %s "
               f"WHERE {match_column} = %s")
        cursor.execute(sql, (new_value, match_value))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        connection = get_db_connection(database)
        cursor = connection.cursor(dictionary=True)
        sql = (f"UPDATE {chart_name} "
               f"SET {target_column} = %s "
               f"WHERE {match_column} = %s")
        cursor.execute(sql, (new_value, match_value))
        print(f"受影响的行数: {cursor.rowcount}")
        connection.commit()
        cursor.close()
        connection.close()

def modify_db_data_for_dict(database,chart_name,match_column,match_value,new_value):
    for col in new_value.keys():
        if col =='password_hash':
            password = new_value[col]
            password_bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash_bytes = bcrypt.hashpw(password_bytes, salt)
            new_value[col] = hash_bytes.decode('utf-8')
    set_clause = ", ".join([f"{col} = %s" for col in new_value.keys()])

    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)

    # 构建完整 SQL
    sql = (f"UPDATE {chart_name} "
           f"SET {set_clause} "
           f"WHERE {match_column} = %s")

    # 准备参数: 更新值的列表 + 匹配值
    params = list(new_value.values()) + [match_value]

    cursor.execute(sql, params)
    print(f"受影响的行数: {cursor.rowcount}")
    connection.commit()
    cursor.close()
    connection.close()








def get_db_all_data(database,chart_name):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    query = f"SELECT * FROM {chart_name}"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data


def get_db_some_data(database, chart_name,list_data):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    columns = ", ".join(list_data)
    query = f"SELECT {columns} FROM {chart_name}"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    connection.close()
    return data


def get_db_range_data(database, chart_name, offset, count):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)

    query = f"SELECT * FROM {chart_name} LIMIT {offset}, {count}"
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    connection.close()
    return data


def get_db_all_data_row(database, chart_name):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT COUNT(*) FROM {chart_name}")
    count = cursor.fetchone()
    cursor.close()
    connection.close()
    return count






def generate_card_number():

    millis_timestamp = int(round(time.time() * 1000))


    random_num = random.randint(0, 999999)


    card_number = f"WH{millis_timestamp}{random_num:06d}"

    return card_number


def add_feedback(database,card, name, content,title,longitude,latitude, status='pending'):
    if not content or content.strip() == "":
        content='无'
    if not title or title.strip() == "":
        title='无'

    connection = get_db_connection(database)
    cursor = connection.cursor()


    sql = """
    INSERT INTO user_feedback (card, name, content, status,title,longitude,latitude)
    VALUES (%s, %s, %s, %s,%s, %s, %s)
    """


    cursor.execute(sql, (card, name, content, status,title,longitude,latitude))


    connection.commit()
    print(f"反馈数据插入成功，记录ID: {cursor.lastrowid}")
    connection.commit()
    cursor.close()
    connection.close()


def add_task( card, longitude, latitude, url,district,position):
    connection = get_db_connection("task")
    cursor = connection.cursor()

    sql = """
        INSERT INTO task (card, url,longitude,latitude,district,position)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
    cursor.execute(sql, (card, url, longitude, latitude,district,position))
    connection.commit()
    cursor.close()
    connection.close()








def get_data_limit_data(database,chart_name):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    sql = f"""
    SELECT * FROM {chart_name}
    WHERE `time` >= %s 
      AND `time` < %s
    """
    cursor.execute(sql, (today, tomorrow))
    results = cursor.fetchall()
    count = cursor.rowcount
    cursor.close()
    connection.close()
    return results,count


def get_db_range_data_for_date(database, chart_name, offset, count,status,type_,time_range):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    conditions = []
    today_start = datetime.now().strftime('%Y-%m-%d 00:00:00')  # 今天0点
    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
    if time_range!= "all":
        if time_range == "three_days_ago":
            time_condition = f"time < '{three_days_ago}'"
            conditions = [time_condition]
        elif time_range == "within_three_days":
            time_condition = f"time >= '{three_days_ago}' AND time < '{today_start}'"
            conditions = [time_condition]
        elif time_range == "today":
            time_condition = f"time >= '{today_start}'"
            conditions = [time_condition]

    if type_ != "all":
        conditions.append(f"type = '{type_}'")
    if status != "all":
        conditions.append(f"status = '{status}'")
    where_query = " WHERE " + " AND ".join(conditions) if conditions else ""
    query = f"SELECT * FROM {chart_name}{where_query} ORDER BY time DESC LIMIT {offset}, {count}"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    print(conditions)
    return data

def get_db_range_data_for_date_num(database, chart_name,status,type_,time_range):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    conditions = []
    today_start = datetime.now().strftime('%Y-%m-%d 00:00:00')  # 今天0点
    three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
    if time_range != "all":
        if time_range == "three_days_ago":
            time_condition = f"time < '{three_days_ago}'"
            conditions = [time_condition]
        elif time_range == "within_three_days":
            time_condition = f"time >= '{three_days_ago}' AND time < '{today_start}'"
            conditions = [time_condition]
        elif time_range == "today":
            time_condition = f"time >= '{today_start}'"
            conditions = [time_condition]
    if type_ != "all":
        conditions.append(f"status = '{type_}'")
    if status != "all":
        conditions.append(f"status = '{status}'")
    where_query = " WHERE " + " AND ".join(conditions) if conditions else ""
    query = f"SELECT * FROM {chart_name}{where_query} "

    cursor.execute(query)
    data = cursor.fetchall()

    record_count = cursor.rowcount
    return record_count


def get_db_last_cl(database, chart_name,number, order_field='id'):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)

    # 关键逻辑：按指定字段倒序排列，取前10条（即最后10条）
    query = f"SELECT * FROM {chart_name} ORDER BY {order_field} DESC LIMIT {number}"
    cursor.execute(query)
    data = cursor.fetchall()
    print(data)

    data.reverse()

    cursor.close()
    connection.close()
    return data










def quick_modify_db_data(database, table_name, update_columns, match_column, match_value):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    set_clause = ", ".join([f"{col} = %s" for col in update_columns.keys()])
    sql = f"UPDATE {table_name} SET {set_clause} WHERE {match_column} = %s"
    params = list(update_columns.values()) + [match_value]
    cursor.execute(sql, params)
    connection.commit()
    print(f"成功更新了 {cursor.rowcount} 行数据")
    cursor.close()
    connection.close()


def check_value_exists(database, table_name, column_name, target_value):
    try:
        connection = get_db_connection(database)
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT 1 FROM {table_name} WHERE {column_name} = %s LIMIT 1"
        cursor.execute(query, (target_value,))
        return cursor.fetchone() is not None
    finally:
            cursor.close()
            connection.close()

def get_db_range_data_(database, chart_name, offset, count,list_):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    if not list_:
        data = get_db_range_data(database, chart_name, offset, count)
        return data
    placeholders = ', '.join(['%s'] * len(list_))
    query = f"SELECT * FROM {chart_name} WHERE card IN ({placeholders}) LIMIT {offset}, {count}"
    cursor.execute(query,list_)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return data

def get_db_range_data_row(database, chart_name,list_):
    connection = get_db_connection(database)
    cursor = connection.cursor(dictionary=True)
    if not list_:
        data = get_db_all_data_row(database, chart_name)
        return data
    placeholders = ', '.join(['%s'] * len(list_))
    query = f"SELECT * FROM {chart_name} WHERE card IN ({placeholders}) "
    cursor.execute(query, list_)
    data = cursor.fetchall()
    count = {'COUNT(*)': len(data)}
    cursor.close()
    connection.close()
    return count


def get_top5_largest( database, table_name, column_name):
    connection = get_db_connection(database)

    cursor = connection.cursor(dictionary=True)


    query = f"""
    SELECT {column_name} ,name
    FROM {table_name} 
    ORDER BY {column_name} DESC 
    LIMIT 5
    """

    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    result = sorted(data, key=lambda x: int(x['value']), reverse=True)
    return result



# database,chart_name,target_column,match_column,match_value,new_value






















# if __name__ == "__main__":
    # def _add_task(card, longitude, latitude,  district, position, value, url):
    #     connection = get_db_connection("task")
    #     cursor = connection.cursor()
    #
    #     sql = """
    #         INSERT INTO task (card,longitude,latitude,district,position,value,url)
    #         VALUES (%s, %s, %s, %s, %s, %s,%s)
    #         """
    #     cursor.execute(sql, (card, longitude, latitude, district, position, value, url))
    #     connection.commit()
    #     cursor.close()
    #     connection.close()
    #
    #
    # import random
    #
    #
    # test_task_list = []
    # types = ["生活事务类", "健康医疗类", "信息咨询类", "情感社交类", "紧急"]
    # districts = ["武昌区", "洪山区", "江岸区", "江汉区", "青山区", "汉阳区", "硚口区", "东西湖区", "蔡甸区", "江夏区"]
    # locations = [
    #     "商场", "医院", "政务中心", "广场", "公园", "学校", "超市", "银行", "餐馆", "写字楼",
    #     "地铁站", "公交站", "社区服务中心", "体育场馆", "图书馆", "菜市场", "加油站", "酒店", "电影院", "KTV"
    # ]
    #
    #
    # base_longitude = 114.2
    # base_latitude = 30.5
    # longitude_range = 0.2  # 经度范围
    # latitude_range = 0.2  # 纬度范围
    #
    # for i in range(200):
    #
    #     timestamp = random.randint(1717800000000, 1718800000000)
    #     card_number = f"HW{timestamp}"
    #
    #     longitude = round(base_longitude + random.uniform(0, longitude_range), 14)
    #     latitude = round(base_latitude + random.uniform(0, latitude_range), 14)
    #
    #     # 随机选择类型、县区和地点
    #     task_type = random.choice(types)
    #     district = random.choice(districts)
    #     location = f"{district}{random.choice(locations)}"
    #
    #     # 生成100-500之间的随机Value值
    #     value = random.randint(100, 500)
    #
    #     # 生成随机URL
    #     url = f"{random.randint(10000000, 99999999)}.wav"
    #
    #     # 添加到列表
    #     test_task_list.append({
    #         "卡号": card_number,
    #         "经度": longitude,
    #         "纬度": latitude,
    #         "类型": task_type,
    #         "所处地区": "湖北省",
    #         "所处县区": district,
    #         "地点": location,
    #         "Value值": value,
    #         "URL": url
    #     })
    #
    # for i in test_task_list:
    #     card =i['卡号']
    #     type_ ='信息咨询类'
    #     print(f"当前类型值: [{type_}]")
    #     longitude =i['经度']
    #     latitude =i["纬度"]
    #     district= i["所处县区"]
    #     position=i["地点"]
    #     value =i["Value值"]
    #     url ='WH1756469583371554999_16.wav'
    #     _add_task(card,  longitude, latitude, district, position, value, url)
    #     # card, type_, longitude, latitude, district, position, value, url

    # elderly_feedback_data = [
    #     {
    #         "card": "HW1717209600000",
    #         "name": "张桂兰",
    #         "content": "希望系统能增加语音提示功能，年纪大了看文字有点费劲",
    #         "status": "pending",
    #         "tip": "操作体验",
    #         "title": "建议增加语音提示",
    #         "longitude": 114.2189,
    #         "latitude": 30.5928
    #     },
    #     {
    #         "card": "HW1717210000000",
    #         "name": "王建国",
    #         "content": "上次提交的社区活动报名，一直没收到确认消息，想问问进展",
    #         "status": "processing",
    #         "tip": "服务体验",
    #         "title": "社区活动报名确认查询",
    #         "longitude": 114.3055,
    #         "latitude": 30.6086
    #     },
    #     {
    #         "card": "HW1717210500000",
    #         "name": "李芳",
    #         "content": "系统里的健康讲座信息很实用，希望能多更新一些武汉本地医院的讲座",
    #         "status": "resolved",
    #         "tip": "健康关怀",
    #         "title": "增加本地医院健康讲座信息",
    #         "longitude": 114.1733,
    #         "latitude": 30.5444
    #     },
    #     {
    #         "card": "HW1717211000000",
    #         "name": "赵援朝",
    #         "content": "经纬度定位有时候不太准，上次显示我在江汉区，其实我在武昌区",
    #         "status": "processing",
    #         "tip": "系统功能",
    #         "title": "定位准确性问题反馈",
    #         "longitude": 114.3615,
    #         "latitude": 30.5488
    #     },
    #     {
    #         "card": "HW1717211500000",
    #         "name": "孙桂英",
    #         "content": "想通过系统找附近的老年活动室，筛选功能不太好用，希望优化",
    #         "status": "pending",
    #         "tip": "设施查询",
    #         "title": "老年活动室筛选功能优化建议",
    #         "longitude": 114.2700,
    #         "latitude": 30.6250
    #     },
    #     {
    #         "card": "HW1717212000000",
    #         "name": "周明",
    #         "content": "感谢工作人员及时处理了我的用药提醒设置问题，现在用着很方便",
    #         "status": "resolved",
    #         "tip": "服务体验",
    #         "title": "用药提醒设置问题已解决",
    #         "longitude": 114.2000,
    #         "latitude": 30.5800
    #     },
    #     {
    #         "card": "HW1717212500000",
    #         "name": "吴兰",
    #         "content": "系统里的社交板块人太少了，希望能多组织线上交流活动，认识些同龄朋友",
    #         "status": "pending",
    #         "tip": "社交体验",
    #         "title": "增加线上社交交流活动",
    #         "longitude": 114.3333,
    #         "latitude": 30.5667
    #     },
    #     {
    #         "card": "HW1717213000000",
    #         "name": "郑国强",
    #         "content": "提交的免费体检预约申请被拒绝了，想知道具体原因",
    #         "status": "reject",
    #         "tip": "健康服务",
    #         "title": "免费体检预约被拒原因查询",
    #         "longitude": 114.2500,
    #         "latitude": 30.6000
    #     },
    #     {
    #         "card": "HW1717213500000",
    #         "name": "钱淑芬",
    #         "content": "系统界面的字体能不能再调大一点，现在的大小看久了眼睛不舒服",
    #         "status": "processing",
    #         "tip": "操作体验",
    #         "title": "建议调大界面字体",
    #         "longitude": 114.1850,
    #         "latitude": 30.5550
    #     },
    #     {
    #         "card": "HW1717219000000",
    #         "name": "尤利",
    #         "content": "系统推送的广场舞活动很适合我，希望能多推送一些武昌区的活动",
    #         "status": "未开始",
    #         "tip": "活动体验",
    #         "title": "希望多推送武昌区广场舞活动",
    #         "longitude": 114.3400,
    #         "latitude": 30.5800
    #     }
    # ]
    # for i in elderly_feedback_data:
    #     card =i["card"]
    #     longitude =i['longitude']
    #     latitude =i["latitude"]
    #     title= i["title"]
    #     name=i["name"]
    #     content = i["content"]
    #     add_feedback('feedback',card, name, content,title,longitude,latitude, status='pending')




