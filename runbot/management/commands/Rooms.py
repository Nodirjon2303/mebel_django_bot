from sqlite3 import connect



def get_rooms_by_id(room_id):
    con = connect('users.db')
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT * FROM rooms WHERE room_id = {room_id}")
        res = cursor.fetchall()
    except Exception as e:
        print(e)
    con.close()
    return res[0]


def add_rooms(user_id, name):
    con = connect('users.db')
    cursor = con.cursor()
    rooms = get_rooms()
    user_rooms = []
    for i in rooms:
        if i[1] == user_id:
            user_rooms.append(i[2])
    if name not in user_rooms:
        try:
            cursor.execute(
                "INSERT INTO rooms (user_id , name ) VALUES (:user_id , :name )",
                {'user_id': user_id, 'name': name})
            con.commit()
        except:
            print("There is something wrong with your code")
    try:
        cursor.execute(f"SELECT * FROM rooms WHERE user_id = {user_id}")
        res = cursor.fetchall()
        cursor.execute(f"UPDATE users SET current_room ={res[-1][0]} where user_id = {user_id} ")
        con.commit()
    except Exception as e:
        print(e)

    con.close()


def set_eni(user_id, eni):
    con = connect('users.db')
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    res = cursor.fetchall()
    print(res[0][-1])

    try:
        cursor.execute(f"UPDATE rooms SET eni = {eni}  where room_id = {res[0][-1]} ")
        con.commit()
    except Exception as e:
        print(e)

    con.close()


def set_buyi(user_id, buyi):
    con = connect('users.db')
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    res = cursor.fetchall()
    print(type(res[0][-1]))

    try:
        cursor.execute(f"UPDATE rooms SET buyi = {buyi}  WHERE room_id = {res[0][-1]} ")
        con.commit()
    except Exception as e:
        print(e)
    con.close()


def set_color(user_id, color):
    con = connect('users.db')
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    res = cursor.fetchall()
    print(type(res[0][-1]))

    try:
        cursor.execute(f"UPDATE rooms SET color = '{color}'  where room_id = {res[0][-1]} ")
        con.commit()
    except Exception as e:
        print(e)

    con.close()


def set_h(user_id, room_h):
    con = connect('users.db')
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    res = cursor.fetchall()
    print(res[0][-1])

    try:
        cursor.execute(f"UPDATE rooms  SET balandlik = {room_h} where room_id = {res[0][-1]} ")
        con.commit()
    except Exception as e:
        print(e)

    con.close()


def delete_room(xona_id):
    con = connect('users.db')
    cursor = con.cursor()
    cursor.execute(f"DELETE FROM rooms WHERE room_id = '{xona_id}'")
    con.commit()
    con.close()

def get_furniture():
    con = connect('users.db')
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT * FROM furniture_category")
        res = cursor.fetchall()
    except Exception as e:
        print(e)
    con.close()
    return res

def get_fur_by_id(cat_id):
    con = connect('users.db')
    cursor = con.cursor()
    try:
        cursor.execute(f"SELECT * FROM furniture_catbycat where category_id = {cat_id} ")
        res = cursor.fetchall()
    except Exception as e:
        print(e)
    con.close()
    return res
def get_fur_detail(cat_id):
    pass