from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton, InlineKeyboardMarkup
from .Rooms import *
from runbot.models import *

con_keyboard = KeyboardButton(text='Send Contact', request_contact=True)
phone_button = ReplyKeyboardMarkup(
    [
        [con_keyboard]
    ], resize_keyboard=True
)

main_buttons = ReplyKeyboardMarkup(
    [
         ['🏘Mening xonalarim',
          '🏡Xona qo\'shish'
          ],
        ['📤Mening zakazlarim',
         '🛍 Savatcha'
         ],
        ['☎️📞Biz bilan aloqa']
    ],
    resize_keyboard=True
)


def Room_button(xona_id):
    ROOM_Buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton('Xonani tahrirlash', callback_data=f'editroom_{xona_id}')],
        [InlineKeyboardButton('Xonani mebellash', callback_data=f'addfurniture_{xona_id}')],
        [InlineKeyboardButton('xonani o\'chirish', callback_data=f'deleteroom_{xona_id}')],
        [InlineKeyboardButton('Ortga', callback_data='back_1')]
    ])

    return ROOM_Buttons


def button_room(user_id):
    profile = Profile.objects.get(telegram_id=user_id)
    rooms = Rooms.objects.filter(profile=profile)
    buttons = []
    temp_b = []
    for i in rooms:
        pass
        print(i)
        temp_b.append(InlineKeyboardButton(i.name, callback_data=i.id))
        buttons.append(temp_b)
        temp_b = []
    temp_b.append(InlineKeyboardButton('Main menu', callback_data='main'))
    buttons.append(temp_b)
    return InlineKeyboardMarkup(buttons)


def edit_room_button(room_id):
    room = Rooms.objects.get(id=int(room_id))

    buttons = []
    temp = []
    temp.append(InlineKeyboardButton(f"Rangi: {room.color}", callback_data=f'editcolor_{room_id}'))
    buttons.append(temp)
    temp = []
    temp.append(InlineKeyboardButton(f"Eni: {room.eni}", callback_data=f'editeni_{room_id}'))
    buttons.append(temp)
    temp = []
    temp.append(InlineKeyboardButton(f"Bo'yi: {room.buyi}", callback_data=f'editbuyi_{room_id}'))
    buttons.append(temp)
    temp = []
    temp.append(InlineKeyboardButton(f"Balanlagi: {room.balandligi}", callback_data=f'edith_{room_id}'))
    buttons.append(temp)
    temp = []
    temp.append(InlineKeyboardButton(f"Ortga", callback_data=f'main_{room_id}'))
    buttons.append(temp)
    return InlineKeyboardMarkup(buttons)


def Button_furnitures():
    furniture_category = Furniture_category.objects.all()
    print(furniture_category)
    temp_b = []
    buttons = []
    for i in furniture_category:
        temp_b.append(InlineKeyboardButton(i.category_name, callback_data=i.id))
        if len(temp_b) == 2:
            buttons.append(temp_b)
            temp_b = []
    if len(temp_b) == 1:
        buttons.append(temp_b)
        temp_b = []
    temp_b.append(InlineKeyboardButton('Ortga', callback_data='back'))
    buttons.append(temp_b)
    return InlineKeyboardMarkup(buttons)


def Button_furniture_by_id(cat_id):
    furniture_category = Furniture_category.objects.get(id=cat_id)
    fur_cat = Furniture_bycat.objects.filter(category=furniture_category)
    print(furniture_category)
    temp_b = []
    buttons = []
    for i in fur_cat:
        temp_b.append(InlineKeyboardButton(i.name, callback_data=i.id))
        if len(temp_b) == 2:
            buttons.append(temp_b)
            temp_b = []
    if len(temp_b) == 1:
        buttons.append(temp_b)
        temp_b = []
    temp_b.append(InlineKeyboardButton('Ortga', callback_data='back'))
    buttons.append(temp_b)
    return InlineKeyboardMarkup(buttons)
def button_furniture(fur_id):
    buttons = [
        [
            InlineKeyboardButton("Zakaz berish", callback_data=f'zakaz_{fur_id}'),
            InlineKeyboardButton("Savatga qo'shish", callback_data=f'savat_{fur_id}')
        ],
        [
            InlineKeyboardButton("Back", callback_data=f'back_{fur_id}')
        ]
    ]
    return InlineKeyboardMarkup(buttons)

def buttons_savatcha():
    buttons = [
        [
            InlineKeyboardButton('Zakaz berish', callback_data='zakaz')
        ],
        [
            InlineKeyboardButton('Savatchani tozalash', callback_data='savat')
        ]
    ]
    return InlineKeyboardMarkup(buttons)
