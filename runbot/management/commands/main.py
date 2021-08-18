from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler
from Buttons import *
from Rooms import *
from Users import *

state_phone = 1
state_main = 2
state_add_room = 3
state_room_name = 4
state_room_eni = 5
state_room_buyi = 6
state_room_h = 7
state_room_edit = 8
state_xonalar = 9
state_update_room = 10
state_update_eni = 11
state_update_buyi = 12
state_update_color = 13
state_update_h = 14
state_add_furniture = 15
state_furniture = 14


def start(update: Update, context: CallbackContext) -> None:
    users = get_date()
    if update.effective_user.id not in users:
        update.message.reply_text(
            f'Assalomu Alaykum {update.effective_user.first_name}\nBotimizga xush kelibsiz ushbu bot orqali siz Uyingiz uchun chiroyli Dizayndagi mebellarni tanlashingiz va sotib olishingiz mumkin!!!\n Botdan to\'liq  foydalanish uchun Telefon raqamingizni yuboring👇👇',
            reply_markup=phone_button)
        return state_phone
    else:
        update.message.reply_text(
            f'Assalomu alaykum {update.effective_user.first_name}\nO\'zingiz uchun kerakli buyruqlardan birini tanlang👇👇',
            reply_markup=main_buttons)
        return state_main


def command_phone(update, context):
    contact = update.effective_message.contact
    phone = contact.phone_number
    add(update.effective_user.first_name, update.effective_user.id, phone)
    update.message.reply_text(f'O\'zingiz uchun kerakli buyruqlardan birini tanlang👇👇', reply_markup=main_buttons)
    return state_main


def my_rooms(update, context):
    rooms = get_rooms()
    my_room = []
    for i in rooms:
        if i[1] == update.effective_user.id:
            my_room.append(i)
    if my_room:
        update.message.reply_text('MY ROOM', reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Xonalaringizdan birini tanlang:', reply_markup=button_room(update.effective_user.id))
        return state_xonalar
    else:
        update.message.reply_text(f'Siz hali Xona qo\'shmagansiz ADD ROOM bo\'limiga borib xona qo\'shing',
                                  reply_markup=main_buttons)
        return state_main


def my_orders(update, context):
    update.message.reply_text('Mening Zakazlarim tanlandi')


def add_room(update, context):
    update.message.reply_text('Xona nomini kiriting:', reply_markup=ReplyKeyboardRemove())
    return state_room_name


def room_eni(update, context):
    update.message.reply_text('Xona enini kiriting:')
    xona_nomi = update.message.text
    add_rooms(update.effective_user.id, xona_nomi)
    print(f'xona nomi: {xona_nomi}')
    return state_room_eni


def room_buyi(update, context):
    update.message.reply_text('Xona buyini kiriting:')
    xona_eni = int(update.message.text)
    set_eni(update.effective_user.id, eni=xona_eni)
    print(f'xona eni', xona_eni)
    return state_room_buyi


def room_h(update, context):
    update.message.reply_text('Xona balandligini kiriting:')
    xona_buyi = int(update.message.text)
    set_buyi(update.effective_user.id, buyi=xona_buyi)
    print(f'xona buyi {xona_buyi}')
    return state_room_h


def room_main(update, context):
    xona_balandligi = int(update.message.text)
    set_h(update.effective_user.id, room_h=xona_balandligi)
    print(f'Xona balandligi {xona_balandligi}')
    update.message.reply_text("Xona muaffaqiyatli qo'shildi", reply_markup=main_buttons)
    return state_main


def inline_add_room(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    print(user_id, query.data)
    query.message.delete()
    try:
        add_rooms(user_id=user_id, name=query.data)
        query.message.reply_html(
            f'Xonalar ro\'yxatiga {query.data} muaffaqiyatli qo\'shildi', reply_markup=main_buttons
        )
    except:
        query.message.reply_html(
            f'Siz allaqachon {query.data} xonani qo\'shib bo\'lgansiz MY ROOMS bo\'limiga o\'ting',
            reply_markup=main_buttons
        )

    return state_main


def command_room_edit(update, context):
    query = update.callback_query
    A = query.data
    aa = A.split('_')
    print('aa', aa[1])
    query.message.delete()
    if aa[0] == 'editroom':
        query.message.reply_html(f'O\'zgartirmoqchi bo\'lgan qismingizni tanlang',
                                 reply_markup=edit_room_button(int(aa[1])))
        update_user_current(update.effective_user.id, int(aa[1]))
        return state_update_room
    elif aa[0] == 'addfurniture':
        update_user_current(update.effective_user.id, int(aa[1]))
        query.message.reply_html(f'Mebel uchun kerakli kategoriyani tanlang ', reply_markup=Button_furnitures())
        return state_add_furniture
    elif aa[0] == 'deleteroom':
        delete_room(int(aa[1]))
        query.message.reply_html(f'xona muaffaqiyatli olib tashlandi  {aa[1]}', reply_markup=main_buttons)
    elif aa[0] == 'back':
        query.message.reply_text('Bosh sahifa', reply_markup=main_buttons)
    return state_main


def command_update_room(update, context):
    query = update.callback_query
    A = query.data
    aa = A.split('_')
    print('aa', aa)
    query.message.delete()
    if aa[0] == 'editcolor':
        query.message.reply_text('Xona uchun yangi rangni tanlang: ')
        return state_update_color
    elif aa[0] == 'editeni':
        query.message.reply_text('Xonaning yangi enini kiriting: ')
        return state_update_eni
    elif aa[0] == 'editbuyi':
        query.message.reply_text('Xonaning yangi buyini kiriting: ')
        return state_room_buyi
    elif aa[0] == 'edith':
        query.message.reply_text('Xonaning yangi balandligini kiriting: ')
        return state_room_h
    elif aa[0] == 'main':
        query.message.reply_text('Siz asosiy menyudasiz\nKerakli buyruqlardan birini tanlang',
                                 reply_markup=main_buttons)
        return state_main


def command_update_color(update, context):
    xona_color = update.message.text
    set_color(update.effective_user.id, xona_color)
    update.message.reply_text(f'Xona rangi {xona_color} ga muaffaqiyatli o\'zgartirildi', reply_markup=main_buttons)
    return state_main


def command_update_eni(update, context):
    xona_eni = int(update.message.text)
    set_eni(update.effective_user.id, xona_eni)
    update.message.reply_text(f'Xona eni {xona_eni}m ga muaffaqiyatli o\'zgartirildi', reply_markup=main_buttons)
    return state_main


def command_update_buyi(update, context):
    xona_buyi = int(update.message.text)
    set_buyi(update.effective_user.id, xona_buyi)
    update.message.reply_text(f'Xona bo\'yi {xona_buyi}m ga muaffaqiyatli o\'zgartirildi', reply_markup=main_buttons)
    return state_main


def command_update_h(update, context):
    xona_h = int(update.message.text)
    set_buyi(update.effective_user.id, xona_h)
    update.message.reply_text(f'Xona balandligi {xona_h}m ga muaffaqiyatli o\'zgartirildi', reply_markup=main_buttons)
    return state_main


def command_xona(update, context):
    query = update.callback_query
    A = query.data
    print('Xona id: ', A)
    query.message.delete()
    rooms = get_rooms()
    my_room = []
    for i in rooms:
        if i[0] == int(A):
            my_room.append(i)
    for i in my_room:
        ph = int(i[0]) % 10 + 1
        xabar = f'Xona Nomi: {i[2]}\n' \
                f'xona rangi: {i[3]}\n' \
                f'Xona eni {i[4]}m\n' \
                f'Xona buyi {i[5]}m\n' \
                f'Xona balandligi {i[6]}m'
        context.bot.send_photo(chat_id=i[1], photo=open(f'rasmlar/room{ph}.png', 'rb'), caption=xabar,
                               reply_markup=Room_button(i[0]))
    return state_room_edit


def command_furniture_category(update, context):
    query = update.callback_query
    A = query.data
    query.message.delete()
    query.message.reply_text('Qaysi turdagi mebel olmoqchisiz', reply_markup=Button_furniture_by_id(int(A)))
    return state_furniture


def command_furniture(update, context):
    query = update.callback_query
    A = query.data
    query.message.delete()
    query.message.reply_text('O\'zingiz uchun kerakli mebelni tanlang ')


updater = Updater('1945109840:AAE_hLSDKMXPhzUn1Lt1t9MeYRykvcbhlSg')

con_hand = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        state_phone: [
            MessageHandler(Filters.contact, command_phone)],
        state_main: [
            MessageHandler(Filters.regex('^(' + 'Mening xonalarim' + ')$'), my_rooms),
            MessageHandler(Filters.regex('^(' + 'Mening buyurtmalarim' + ')$'), my_orders),
            MessageHandler(Filters.regex('^(' + 'Xona qo\'shish' + ')$'), add_room),
        ],
        state_add_room: [
            CallbackQueryHandler(inline_add_room)
        ],
        state_room_name: [
            MessageHandler(Filters.text, room_eni)
        ],
        state_room_eni: [
            MessageHandler(Filters.text, room_buyi)
        ],
        state_room_buyi: [
            MessageHandler(Filters.text, room_h)
        ],
        state_room_h: [
            MessageHandler(Filters.text, room_main)
        ],
        state_room_edit: [
            CallbackQueryHandler(command_room_edit)
        ],
        state_xonalar: [
            CallbackQueryHandler(command_xona)
        ],
        state_update_room: [
            CallbackQueryHandler(command_update_room)
        ],
        state_update_color: [
            MessageHandler(Filters.text, command_update_color)
        ],

        state_update_eni: [
            MessageHandler(Filters.text, command_update_eni)
        ],

        state_update_buyi: [
            MessageHandler(Filters.text, command_update_buyi)
        ],

        state_update_h: [
            MessageHandler(Filters.text, command_update_h)
        ],

        state_add_furniture: [
            CallbackQueryHandler(command_furniture_category)
        ],
        state_furniture: [
            CallbackQueryHandler(command_furniture)
        ]
    },
    fallbacks=[CommandHandler('start', start)]
)

updater.dispatcher.add_handler(con_hand)
updater.start_polling()
updater.idle()
