from sqlite3 import connect


def get_date():
    con = connect('users.db')
    cursor = con.cursor()
    all_users = []
    try:
        cursor.execute(f"SELECT * FROM users")
        res = cursor.fetchall()
        print(res)
    except Exception as e:
        print(e)
    con.close()
    try:
        for i in res:
            all_users.append(i[2])
        return all_users
    except Exception as e:
        return 1


def add(first_name, id, phone_number):
    con = connect('users.db')
    users = get_date()
    cursor = con.cursor()
    if id not in users:
        try:
            cursor.execute(
                "INSERT INTO users (first_name ,user_id, phone_number ) VALUES (:first_name , :id, :phone_number)",
                {'first_name': first_name, 'id': id, 'phone_number': phone_number})
            con.commit()
        except:
            print("There is something wrong with your code")
    con.close()


def update_user_current(user_id, room_id):
    con = connect('users.db')
    cursor = con.cursor()
    try:
        cursor.execute(f"UPDATE users SET current_room = {room_id}  where user_id = {user_id} ")
        con.commit()
    except Exception as e:
        print(e)
    con.close()

