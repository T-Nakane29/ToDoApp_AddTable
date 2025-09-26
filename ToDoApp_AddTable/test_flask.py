from flask import Flask
import mariadb
import settings

app = Flask(__name__)


def get_connection():
    return mariadb.connect(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name
    )


# テスト新規追加
def test_insert():
    conn = get_connection()
    cur = conn.cursor()
    sql = (
        "INSERT INTO " + settings.tbl_name + " "
        "(name, task, due_date, rent_buy, real_estate, real_estate_name, note) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)"
    )
    data = ("山田太郎", "新規追加タスク", "2025-08-31", "賃貸", "戸建て", "新規追加物件", "101号室")
    cur.execute(sql, data)
    conn.commit()

    # 直前にINSERTしたレコードのIDを取得する
    inserted_id = cur.lastrowid
    cur.close()
    conn.close()
    print(f"追加成功: ID={inserted_id}")
    return inserted_id


# テスト編集
def test_update(id):
    conn = get_connection()
    cur = conn.cursor()
    sql = (
        "UPDATE " + settings.tbl_name + " "
        "SET name = ?, task = ?, due_date = ?, rent_buy = ?, real_estate = ?, real_estate_name = ?, note = ? "
        "WHERE id = ?"
    )
    updated_data = ("田中次郎", "新規追加タスク編集済み", "2025-08-25", "管理",
                    "集合住宅", "新規追加物件編集済み", "101号室ではなく102号室", id)
    cur.execute(sql, updated_data)
    conn.commit()
    cur.close()
    conn.close()
    print(f"編集成功: ID={id}")

# テスト削除


def test_delete(id):
    conn = get_connection()
    cur = conn.cursor()
    sql = "DELETE FROM " + settings.tbl_name + " WHERE id = ?"
    cur.execute(sql, (id,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"削除成功: ID={id}")

# テスト後DBデータ確認


def test_select_all():
    conn = get_connection()
    cur = conn.cursor()
    sql = "SELECT * FROM " + settings.tbl_name
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    print("現在のデータ一覧:")
    for row in rows:
        print(row)


if __name__ == "__main__":
    print("テスト開始")
    inserted_id = test_insert()
    test_select_all()
    test_update(inserted_id)
    test_select_all()
    test_delete(inserted_id)
    test_select_all()
