from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import Blueprint, request


socketio_all = Blueprint('socketio', __name__)


socketio = SocketIO(cors_allowed_origins="*")

clients = {}



@socketio.on('register')
def handle_register(data):

    client_id = request.sid
    room = data['room']
    clients[client_id] = room
    join_room(room)
    print(f"客户端 {client_id} 注册到房间: {room}")


@socketio.on('connect')
def handle_connect():
    client_id = request.sid  # 获取客户端唯一标识
    print(f"客户端 {client_id} 已连接")
    emit('connected', {'message': '连接成功', 'client_id': client_id})


@socketio.on('name')
def handle_name_event(data):

    sender_room = clients.get(request.sid)
    emit('forwarded_name', data, room='chart_overview')  # 只发给clientB房间




@socketio.on('order')
def handle_order_event_card_overview(data):
    emit('charge_data', data, room='card_overview')


@socketio.on('charge_list_record')
def charge_list_record(data):
    emit('charge_data', data, room='record_list')

@socketio.on('record_data')
def charge_list_record(data):
    print(data)
    emit('record_data', data, room='map_record')

@socketio.on('task_point')
def charge_list_record(data):
    print(data)
    print('test')
    emit('task_point', data, room='task_map')
@socketio.on('record')
def charge_record(data):
    print(data)
    print('test')
    emit('record', data, room='record_page')
@socketio.on('source')
def charge_source(data):
    print(data)
    print('source')
    emit('source', data, room='map_source')
@socketio.on('sos')
def sos(data):
    print(data)
    emit('sos', data, room='task_list')