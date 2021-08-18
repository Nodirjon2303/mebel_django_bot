from django.core.management.base import BaseCommand
from telegram.utils.request import Request
from telegram import Bot
from django.conf import settings
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler
from runbot.models import *
from .Buttons import *
from .Rooms import *
from .Users import *

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
state_furniture = 16
state_furniture_zakaz = 17
state_savatcha = 18


def start(update: Update, context: CallbackContext) -> None:
    profile, boolen = Profile.objects.get_or_create(telegram_id=update.effective_user.id,
                                                    first_name=update.effective_user.first_name)
    print('a=', profile.first_name, 'b=', boolen)
    print(not profile.phone_number)
    if not profile.phone_number:
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
    print(contact)
    phone = contact.phone_number
    print("phone:", phone)
    profile = Profile.objects.get(telegram_id=contact.user_id)
    profile.phone_number = phone
    profile.save()
    update.message.reply_text(f'O\'zingiz uchun kerakli buyruqlardan birini tanlang👇👇', reply_markup=main_buttons)
    return state_main


def my_rooms(update, context):
    profile = Profile.objects.get(telegram_id=update.effective_user.id)

    try:
        rooms = Rooms.objects.filter(profile=profile)
    except Exception as e:
        print(e)
        rooms = []
    print("ROOMS", rooms)
    if rooms:
        update.message.reply_text('MY ROOM', reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Xonalaringizdan birini tanlang:', reply_markup=button_room(update.effective_user.id))
        return state_xonalar
    else:
        update.message.reply_text(f'Siz hali Xona qo\'shmagansiz ADD ROOM bo\'limiga borib xona qo\'shing',
                                  reply_markup=main_buttons)
        return state_main


def my_orders(update, context):
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    orders = Order.objects.filter(profile=profile)
    if orders:
        for order in orders:
            t = 1
            fur = order.furniture
            context.bot.send_photo(chat_id=update.effective_user.id,
                                   photo=open(f"D:/PYTHON/MY PROJECTS/mebel_django_bot/media/{fur.image}",
                                              'rb'),
                                   caption=f"{t}- zakaz \n"
                                           f"Mebel nomi: {fur.name}\n"
                                           f"Mebel Narxi: {fur.price} so\'m\n"
                                           f"Mebel zakaz berilgan sanasi: {order.order_date}\n"
                                           f"Zakaz berilgan soni: {order.quantity}\n"
                                           f"Zakaz holati: {order.status}")
            t += 1
    else:
        update.message.reply_text(
            'Siz hali mahsulot zakaz bermagansiz Mahsulotlar bo\'limiga borib mahsulot zakaz qilishingiz mumkin')
    return state_main


def add_room(update, context):
    update.message.reply_text('Xona nomini kiriting:', reply_markup=ReplyKeyboardRemove())
    return state_room_name


def room_eni(update, context):
    update.message.reply_text('Xona enini kiriting:')
    xona_nomi = update.message.text
    profile = Profile.objects.get(telegram_id=update.message.chat_id)
    room = Rooms.objects.create(name=xona_nomi, profile=profile)
    profile.current_room = room.id
    profile.save()
    print(f'xona nomi: {xona_nomi}')
    return state_room_eni


def room_buyi(update, context):
    update.message.reply_text('Xona buyini kiriting:')
    xona_eni = float(update.message.text)
    print(f'xona eni', xona_eni)
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    room = Rooms.objects.get(id=profile.current_room)
    room.eni = xona_eni
    room.save()
    print(room.name)
    return state_room_buyi


def room_h(update, context):
    update.message.reply_text('Xona balandligini kiriting:')
    xona_buyi = float(update.message.text)
    print(f'xona buyi {xona_buyi}')
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    room = Rooms.objects.get(id=profile.current_room)
    room.buyi = xona_buyi
    room.save()
    return state_room_h


def room_main(update, context):
    xona_balandligi = float(update.message.text)
    print(f'Xona balandligi {xona_balandligi}')
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    room = Rooms.objects.get(id=profile.current_room)
    room.balandligi = xona_balandligi
    room.save()
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


def command_fur_zakaz(update, context):
    query = update.callback_query
    query.message.delete()
    print("QUERY:", type(query.message))
    A = query.data
    aa = A.split('_')
    print('aa', aa[1])
    furniture = Furnitures.objects.get(id=int(aa[1]))
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    if aa[0] == 'zakaz':
        query.message.reply_html(
            f'Zakaz muaffaqiyatli qabul qilindi\n Tez orada siz bilan bog\'lanamiz\nZakazlarni MY ORDERS bo\'limida ko\'rishingiz mumkin',
            reply_markup=main_buttons)

        Order.objects.create(furniture=furniture, profile=profile)
        return state_main
    if aa[0] == 'savat':
        query.message.reply_html(
            f'Mahsulot savatchaga muaffaqiyatli qo\'shildi\nMahsulotni Savatcha bo\'limida ko\'rishingiz mumkin',
            reply_markup=main_buttons)
        Savatcha.objects.create(profile=profile, furniture=furniture)
        return state_main
    if aa[0] == 'back':
        rooms = Rooms.objects.filter(profile=profile)
        if rooms:
            query.message.reply_text('Xonalaringizdan birini tanlang:',
                                     reply_markup=button_room(update.effective_user.id))
            return state_xonalar
        else:
            update.message.reply_text(f'MAIN MENU',
                                      reply_markup=main_buttons)
            return state_main


def command_room_edit(update, context):
    query = update.callback_query
    A = query.data
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    aa = A.split('_')
    print('aa', aa[1])
    query.message.delete()
    if aa[0] == 'editroom':
        query.message.reply_html(f'O\'zgartirmoqchi bo\'lgan qismingizni tanlang',
                                 reply_markup=edit_room_button(int(aa[1])))
        profile.current_room = int(aa[1])
        profile.save()
        return state_update_room
    elif aa[0] == 'addfurniture':
        profile = Profile.objects.get(telegram_id=update.effective_user.id)
        profile.current_room = int(aa[1])
        profile.save()
        query.message.reply_html(f'Mebel uchun kerakli kategoriyani tanlang ', reply_markup=Button_furnitures())
        return state_add_furniture
    elif aa[0] == 'deleteroom':
        room = Rooms.objects.get(id=int(aa[1]))
        room.delete()
        query.message.reply_html(f'xona muaffaqiyatli olib tashlandi ', reply_markup=main_buttons)
        return state_main
    elif aa[0] == 'back':
        rooms = Rooms.objects.filter(profile=profile)
        if rooms:
            query.message.reply_text('Xonalaringizdan birini tanlang:',
                                     reply_markup=button_room(update.effective_user.id))
            return state_xonalar
        else:
            query.message.reply_text(f'MAIN MENU',
                                     reply_markup=main_buttons)
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
        profile = Profile.objects.get(telegram_id=update.effective_user.id)
        room = Rooms.objects.get(id=profile.current_room)
        ph = int(room.id) % 10 + 1
        xabar = f'Xona Nomi: {room.name}\n' \
                f'xona rangi: {room.color}\n' \
                f'Xona eni {room.eni}m\n' \
                f'Xona buyi {room.buyi}m\n' \
                f'Xona balandligi {room.balandligi}m'
        context.bot.send_photo(chat_id=profile.telegram_id,
                               photo=open(f'D:/PYTHON/MY PROJECTS/Mebel_bot/rasmlar/room{ph}.png', 'rb'), caption=xabar,
                               reply_markup=Room_button(room.id))

        return state_room_edit


def command_update_color(update, context):
    xona_color = update.message.text
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    room = Rooms.objects.get(id=profile.current_room)
    room.color = xona_color
    room.save()
    update.message.reply_text(f'Xona rangi {xona_color} ga muaffaqiyatli o\'zgartirildi')
    ph = int(room.id) % 10 + 1
    xabar = f'Xona Nomi: {room.name}\n' \
            f'xona rangi: {room.color}\n' \
            f'Xona eni {room.eni}m\n' \
            f'Xona buyi {room.buyi}m\n' \
            f'Xona balandligi {room.balandligi}m'
    context.bot.send_photo(chat_id=profile.telegram_id,
                           photo=open(f'D:/PYTHON/MY PROJECTS/Mebel_bot/rasmlar/room{ph}.png', 'rb'), caption=xabar,
                           reply_markup=Room_button(room.id))
    return state_room_edit


def command_update_eni(update, context):
    xona_eni = float(update.message.text)
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    room = Rooms.objects.get(id=profile.current_room)
    room.eni = xona_eni
    room.save()
    update.message.reply_text(f'Xona eni {xona_eni}m ga muaffaqiyatli o\'zgartirildi')
    ph = int(room.id) % 10 + 1
    xabar = f'Xona Nomi: {room.name}\n' \
            f'xona rangi: {room.color}\n' \
            f'Xona eni {room.eni}m\n' \
            f'Xona buyi {room.buyi}m\n' \
            f'Xona balandligi {room.balandligi}m'
    context.bot.send_photo(chat_id=profile.telegram_id,
                           photo=open(f'D:/PYTHON/MY PROJECTS/Mebel_bot/rasmlar/room{ph}.png', 'rb'), caption=xabar,
                           reply_markup=Room_button(room.id))
    return state_room_edit


def command_update_buyi(update, context):
    xona_buyi = float(update.message.text)
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    room = Rooms.objects.get(id=profile.current_room)
    room.buyi = xona_buyi
    room.save()
    update.message.reply_text(f'Xona bo\'yi {xona_buyi}m ga muaffaqiyatli o\'zgartirildi')
    ph = int(room.id) % 10 + 1
    xabar = f'Xona Nomi: {room.name}\n' \
            f'xona rangi: {room.color}\n' \
            f'Xona eni {room.eni}m\n' \
            f'Xona buyi {room.buyi}m\n' \
            f'Xona balandligi {room.balandligi}m'
    context.bot.send_photo(chat_id=profile.telegram_id,
                           photo=open(f'D:/PYTHON/MY PROJECTS/Mebel_bot/rasmlar/room{ph}.png', 'rb'), caption=xabar,
                           reply_markup=Room_button(room.id))
    return state_room_edit


def command_update_h(update, context):
    xona_h = float(update.message.text)
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    room = Rooms.objects.get(id=profile.current_room)
    room.h = xona_h
    room.save()
    update.message.reply_text(f'Xona balandligi {xona_h}m ga muaffaqiyatli o\'zgartirildi')
    ph = int(room.id) % 10 + 1
    xabar = f'Xona Nomi: {room.name}\n' \
            f'xona rangi: {room.color}\n' \
            f'Xona eni {room.eni}m\n' \
            f'Xona buyi {room.buyi}m\n' \
            f'Xona balandligi {room.balandligi}m'
    context.bot.send_photo(chat_id=profile.telegram_id,
                           photo=open(f'D:/PYTHON/MY PROJECTS/Mebel_bot/rasmlar/room{ph}.png', 'rb'), caption=xabar,
                           reply_markup=Room_button(room.id))
    return state_room_edit


def command_xona(update, context):
    query = update.callback_query
    query.message.delete()
    A = query.data
    if query.data == 'main':
        query.message.reply_text('Main menu', reply_markup=main_buttons)
        return state_main
    else:
        profile = Profile.objects.get(telegram_id=update.effective_user.id)
        room = Rooms.objects.get(id=int(A))
        profile.current_room = room.id
        profile.save()
        ph = int(room.id) % 10 + 1
        xabar = f'Xona Nomi: {room.name}\n' \
                f'xona rangi: {room.color}\n' \
                f'Xona eni {room.eni}m\n' \
                f'Xona buyi {room.buyi}m\n' \
                f'Xona balandligi {room.balandligi}m'
        context.bot.send_photo(chat_id=profile.telegram_id,
                               photo=open(f'D:/PYTHON/MY PROJECTS/Mebel_bot/rasmlar/room{ph}.png', 'rb'), caption=xabar,
                               reply_markup=Room_button(room.id))

        return state_room_edit


def command_furniture_category(update, context):
    query = update.callback_query
    A = query.data
    query.message.delete()
    if A == 'back':
        profile = Profile.objects.get(telegram_id=update.effective_user.id)
        room = Rooms.objects.get(id=profile.current_room)
        ph = int(room.id) % 10 + 1
        xabar = f'Xona Nomi: {room.name}\n' \
                f'xona rangi: {room.color}\n' \
                f'Xona eni {room.eni}m\n' \
                f'Xona buyi {room.buyi}m\n' \
                f'Xona balandligi {room.balandligi}m'
        context.bot.send_photo(chat_id=profile.telegram_id,
                               photo=open(f'D:/PYTHON/MY PROJECTS/Mebel_bot/rasmlar/room{ph}.png', 'rb'), caption=xabar,
                               reply_markup=Room_button(room.id))

        return state_room_edit
    else:
        query.message.reply_text('Qaysi turdagi mebel olmoqchisiz', reply_markup=Button_furniture_by_id(int(A)))
        return state_furniture


def command_furniture(update, context):
    query = update.callback_query
    A = query.data
    query.message.delete()
    if A == 'back':
        query.message.reply_html(f'Mebel uchun kerakli kategoriyani tanlang ', reply_markup=Button_furnitures())
        return state_add_furniture
    else:
        fur_cat = Furniture_bycat.objects.get(id=int(A))
        furniture = Furnitures.objects.filter(category=fur_cat)
        if len(furniture) != 0:
            query.message.reply_text("O\'zingiz uchun quyidagi mebellardan birini tanlang",
                                     reply_markup=ReplyKeyboardRemove())
            for fur in furniture:
                try:
                    context.bot.send_photo(chat_id=update.effective_user.id,
                                           photo=open(f"D:/PYTHON/MY PROJECTS/mebel_django_bot/media/{fur.image}",
                                                      'rb'),
                                           caption=f"Mebel nomi: {fur.name}\n"
                                                   f"Mebel Narxi: {fur.price} so\'m",
                                           reply_markup=button_furniture(fur.id))
                except Exception as e:
                    print(e)
            return state_furniture_zakaz

        else:
            query.message.reply_text(
                'Hozircha ushbu katigoriyada mebel mavjud emas\n Iltimos boshqa kategoriyalardan birini tanlang',
                reply_markup=Button_furnitures())
            return state_add_furniture


def log_errors(f):
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'xatolik: {e}'
            print(error_message)
            raise e

    return inner


@log_errors
def do_echo(update, context):
    chat_id = update.message.chat_id
    text = update.message.text

    reply_text = f"Sizning ID raqamingiz: {chat_id}\n{text}"
    update.message.reply_text(
        text=reply_text
    )


def savatcha(update, context):
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    savat = Savatcha.objects.filter(profile=profile)
    if savat:
        xabar = ''
        Jami = 0
        for i in savat:
            k = 1
            xabar += f"{k}.  Mebel Nomi: {i.furniture.name} \n      Mebel narxi: {i.furniture.price}\n      Zakazlar soni:{i.quantity}\n"
            Jami += i.furniture.price
        xabar += f"Jami: {Jami} so\'m"
        update.message.reply_text(xabar, reply_markup=buttons_savatcha())

        return state_savatcha

    else:
        update.message.reply_text(
        'Siz hali savatchaga mebel qo\'shmagansiz\nMebellar bo\'limiga borib savatchaga mahsulot qo\'shing',
        reply_markup=main_buttons)
        return state_main


def command_savatcha(update, context):
    query = update.callback_query
    A = query.data
    profile = Profile.objects.get(telegram_id=update.effective_user.id)
    if A == 'savat':
        Savatcha.objects.filter(profile=profile).delete()
        query.message.reply_text('Savatcha muaffaqiyatli tozalandi:', reply_markup=main_buttons)
        return state_main
    elif A == 'zakaz':
        savat = Savatcha.objects.filter(profile=profile)
        try:
            for i in savat:
                Order.objects.create(profile=profile, furniture=i.furniture)
            update.message.reply_text(
                "Zakaz muaffaqiyatli qabul qilindi\nTez orada siz bilan bo\'g\'lanamiz\nZakazlaringizni Mening zakazlarim bo\'limidan ko\'rishingiz mumkin",
                reply_markup=main_buttons)
            return state_main
        except:
            update.message.reply_text('main manu', reply_markup=main_buttons)


def contact(update, context):
    update.message.reply_html(
        f'Aссалому алайкум ва роҳматуллоҳи ва барокатуҳ!\nБот юзасидан фикр ва таклифларингизни юборишингиз мумкин👇👇\n👨‍💻  @ruzimurodov_nodir\n☎️📞 +998900036563',
        reply_markup=main_buttons)
    return state_main


class Command(BaseCommand):
    help = 'Telegram-bot'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0
        )
        bot = Bot(
            request=request,
            token=settings.TOKEN,
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True
        )

        con_hand = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                state_phone: [
                    MessageHandler(Filters.contact, command_phone)],
                state_main: [
                    MessageHandler(Filters.regex('^(' + '🏘Mening xonalarim' + ')$'), my_rooms),
                    MessageHandler(Filters.regex('^(' + '📤Mening zakazlarim' + ')$'), my_orders),
                    MessageHandler(Filters.regex('^(' + '🏡Xona qo\'shish' + ')$'), add_room),
                    MessageHandler(Filters.regex('^(' + '🛍 Savatcha' + ')$'), savatcha),
                    MessageHandler(Filters.regex('^(' + '☎️📞Biz bilan aloqa' + ')$'), contact)
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
                ],
                state_furniture_zakaz: [
                    CallbackQueryHandler(command_fur_zakaz)
                ],
                state_savatcha: [
                    CallbackQueryHandler(command_savatcha)
                ]
            },
            fallbacks=[CommandHandler('start', start)]
        )

        updater.dispatcher.add_handler(con_hand)

        updater.start_polling()
        updater.idle()
