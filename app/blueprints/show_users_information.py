
from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import tool


app = Flask(
    __name__,
    template_folder=r'D:\made_map\wuhan_map\web_project\my_templates',
    static_folder=r'D:\made_map\wuhan_map\web_project\static'
)
app.secret_key = 'jsdajhdlialkjdl'

@app.route('/', methods=['GET'])
def user_information_show ():
    session['username'] = "1"
    username = session['username']
    tool.get_db_connection('users-information')
    data_list = tool.get_db_data('users-information','users','username',username)
    data = json.dumps(data_list)
    return render_template('user.html', data=data)

@app.route('/', methods=['POST'])
def upload_file():
    username = session['username']
    content_type = request.headers.get('Content-Type')
    if content_type.startswith('multipart/form-data'):
        file = request.files['user_avatar_file']
        extension = file.filename.rsplit(".", 1)[1].lower()
        new_filename = f"{username}."+extension
        file.filename = new_filename
        print(file.filename)
        file_path = '../static/images/user_avatar/' + file.filename
        file.save(file_path)
        tool.modify_db_data('users-information', 'users', 'user_avatar', 'username', username, file_path)
        data_list = tool.get_db_data('users-information', 'users', 'username', username)
        data = json.dumps(data_list)
        return render_template('user.html', data=data)
    if content_type == 'application/json':
        data = request.json
        for key in data.keys():
            if key != 'password':
                tool.modify_db_data('users-information', 'users', key, 'username', username, data[key])
            else:
                tool.create_password_hash(data)
                tool.modify_db_data('users-information', 'users', 'password_hash', 'username', username, data['password_hash'])
        data_list = tool.get_db_data('users-information', 'users', 'username', username)
        data = json.dumps(data_list)
        return render_template('user.html', data=data)
    return render_template('user.html')
@app.route('/add_user', methods=['POST'])
def add_user ():
    rawdata = request.form
    print(rawdata)
    data =  rawdata.to_dict()
    tool.create_user(data,'users-information','users')
    return 'okok'
@app.route('/del_user', methods=['POST'])
def del_user ():
    # 应加判断是否为admin
    rawdata = request.form

    data =  rawdata.to_dict()
    tool.del_user(data,'users-information','users')
    return 'okok'


@app.route('/adjust_user', methods=['POST'])
def adjust_user ():
    # 应加判断是否为admin
    rawdata = request.form
    data =  rawdata.to_dict()
    values = list(data.values())
    keys = list(data.keys())
    tool.modify_db_data('users-information','users','password_hash',keys[0],values[0],values[1])
    return 'okok'

@app.route('/query_user', methods=['GET'])
def query_user ():
    username = request.args.get('username')
    tool.get_db_connection('users-information')
    data_list = tool.get_db_data('users-information','users','username',username)
    data = json.dumps(data_list)

    return data






if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=True ,port =3348)

