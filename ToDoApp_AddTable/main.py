from flask import Flask, render_template, request, redirect, session
import mariadb
import settings
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
# ユーザーログイン状態をsessionという辞書型オブジェクトが保持し、それはクッキーに保存される。
# 改ざんされて任意の名前以外でも入られないように暗号化するために必要なガキが secret_key


def get_connection():
    return mariadb.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name
    )

# 25/8/21 新規追加、編集などに複数回繰り返し出ているのでMariaDB接続を関数でまとめる


# userリストを取得する
def get_all_users():
    sql = "SELECT id, name FROM users"
    return execute_query(sql, fetch=True)


def execute_query(sql, params=None, fetch=False):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, params or ())
    result = cur.fetchall() if fetch else None
    if not fetch:
        conn.commit()
    cur.close()
    conn.close()
    return result


def get_user_id(name):
    sql = "SELECT id FROM users WHERE name = ?"
    result = execute_query(sql, (name,), fetch=True)
    return result[0][0] if result else None


@app.route('/')
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    name = request.form['username']
    user_id = get_user_id(name)
    if user_id:
        session['user_id'] = user_id
        session['username'] = name
        session['is_admin'] = (name == '中根 貴仁')  # 管理者判定

        return redirect('/tasks')
    else:
        return "名前が見つかりませんでした。"


# ユーザー追加処理
@app.route('/add_user', methods=["POST"])
def add_user():
    if not session.get('is_admin'):
        return "権限がありません"

    new_name = request.form.get("new_username")
    if not new_name:
        return "名前が空です"

    # 重複チェック
    sql_check = "SELECT id FROM users WHERE name = ?"
    existing = execute_query(sql_check, (new_name,), fetch=True)
    if existing:
        return "その名前はすでに登録されています"

    # 登録処理
    sql_insert = "INSERT INTO users (name) VALUES (?)"
    execute_query(sql_insert, (new_name,))
    return redirect('/tasks')


# ユーザー削除処理
@app.route('/delete_user', methods=["POST"])
def delete_user():
    if not session.get('is_admin'):
        return "権限がありません"

    user_id = request.form.get("delete_user_id")
    if not user_id:
        return "ユーザーが選択されていません"

    # 存在確認（任意）
    sql_check = "SELECT id FROM users WHERE id = ?"
    existing = execute_query(sql_check, (user_id,), fetch=True)
    if not existing:
        return "そのユーザーは存在しません"

    # 削除処理（ON DELETE CASCADEが有効ならtasksも削除される）
    sql_delete = "DELETE FROM users WHERE id = ?"
    execute_query(sql_delete, (user_id,))
    return redirect('/tasks')


@app.route('/tasks')
def tasks():
    if 'user_id' not in session:
        return redirect('/')
    # id名が表示されてしまうのでsqlを変更 25/9/23
    sql = """
    SELECT tasks.id, users.name, tasks.task, tasks.due_date, tasks.rent_buy,
    tasks.real_estate, tasks.real_estate_name, tasks.note
    FROM tasks
    JOIN users ON tasks.user_id = users.id
    WHERE tasks.user_id = ?
    """
    todo_data = execute_query(sql, (session['user_id'],), fetch=True)
    user_list = get_all_users() if session.get('is_admin') else []
    return render_template("index.html", todo_data=todo_data, username=session['username'], user_list=user_list)


# ログアウト処理
@app.route('/logout')
def logout():
    session.clear()  # セッション情報をすべて削除
    return redirect('/')


# 可読性・安全性UPのため新規追加～DBからのデータ取得(全件)までをルート分け
# URLの先頭('/')にアクセスした際に表示
# 新規追加処理
@app.route('/add', methods=["POST"])
def add():
    form_data = {
        "user_id": session['user_id'],
        "task": request.form.get("task"),
        "due_date": request.form.get("due_date"),
        "rent_buy": request.form.get("rent_buy"),
        "real_estate": request.form.get("real_estate"),
        "real_estate_name": request.form.get("real_estate_name"),
        "note": request.form.get("note")
    }

    # SQLインジェクションリスク回避のためf-string(f""")から変更
    # 新規追加と同様に編集、削除、DBからのデータ取得の部分を変更する
    sql = (
        "INSERT INTO tasks "
        # 25/8/21 スペース抜け注意
        "(user_id, task, due_date, rent_buy, real_estate, real_estate_name, note) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    )

    # 25/8/21 上部で設定したMariaDBの接続関数
    execute_query(sql, tuple(form_data.values()))
    return redirect('/tasks')


# 編集処理
@app.route('/update', methods=["POST"])
def update():
    form_data = {
        "task": request.form.get("task"),
        "due_date": request.form.get("due_date"),
        "rent_buy": request.form.get("rent_buy"),
        "real_estate": request.form.get("real_estate"),
        "real_estate_name": request.form.get("real_estate_name"),
        "note": request.form.get("note"),
        "id": request.form.get("update_id")
    }
    sql = (
        "UPDATE tasks SET task = ?, due_date = ?, rent_buy = ?, real_estate = ?, real_estate_name = ?, note = ? "
        "WHERE id = ? AND user_id = ?"
    )

    # 25/8/21 上部で設定したMariaDBの接続関数
    execute_query(sql, tuple(form_data.values()) + (session['user_id'],))
    return redirect('/tasks')


# 削除処理
@app.route('/delete', methods=["POST"])
def delete():
    target_id = request.form.get("delete_id")
    sql = "DELETE FROM tasks WHERE id = ? AND user_id = ?"

    # 25/8/21 上部で設定したMariaDBの接続関数を一部変更
    execute_query(sql, (target_id, session['user_id']))
    return redirect('/tasks')


# DBからのデータ取得(全件)
@app.route('/')
def index():
    sql = "SELECT * FROM " + settings.tbl_name

    # 25/8/21 上部で設定したMariaDBの接続関数を一部変更
    todo_data = execute_query(sql, fetch=True)
    return render_template("index.html", todo_data=todo_data)


# 25/8/21 MariaDB接続は不要
if __name__ == '__main__':
    app.run(debug=True, port=2000)
