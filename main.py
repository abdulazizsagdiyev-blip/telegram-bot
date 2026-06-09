# -*- coding: utf-8 -*-
import telebot
from telebot import types
import json
import os
from datetime import datetime

bot = telebot.TeleBot("8965235108:AAFOvnpgR3C9VXRBkG0M2_X87xDiMdDK5QM")

ADMIN_ID = 5331260247

WORK_START = 9
WORK_END = 18

user_data = {}
requests_db = {}
request_counter = [0]

REGIONS = {
    "Toshkent shahri": ["Bektemir", "Chilonzor", "Hamza", "Mirzo Ulugbek", "Mirobod", "Sergeli", "Shayxontohur", "Olmazar", "Uchtepa", "Yakkasaroy", "Yashnobod", "Yunusobod"],
    "Toshkent viloyati": ["Angren", "Bekobod", "Bo'stonliq", "Chinoz", "Qibray", "Oqqo'rg'on", "Ohangaron", "Parkent", "Piskent", "Yangiyo'l", "Yuqorichirchiq", "Zangiota"],
    "Samarqand viloyati": ["Samarqand", "Kattaqo'rg'on", "Ishtixon", "Jomboy", "Qo'shrabot", "Narpay", "Nurobod", "Oqdaryo", "Pastdarg'om", "Payariq", "Toyloq", "Urgut"],
    "Farg'ona viloyati": ["Farg'ona", "Qo'qon", "Marg'ilon", "Oltiariq", "Bag'dod", "Beshariq", "Buvayda", "Dang'ara", "Furqat", "Quva", "Rishton", "Toshloq", "O'zbekiston", "Yozyovon"],
    "Andijon viloyati": ["Andijon", "Asaka", "Baliqchi", "Bo'z", "Buloqboshi", "Izboskan", "Jalolquduq", "Xo'jaobod", "Marhamat", "Oltinkol", "Paxtaobod", "Qo'rg'ontepa", "Shahrixon", "Ulug'nor"],
    "Namangan viloyati": ["Namangan", "Chortoq", "Chust", "Kosonsoy", "Mingbuloq", "Norin", "Pop", "To'raqo'rg'on", "Uychi", "Yangiqo'rg'on"],
    "Qashqadaryo viloyati": ["Qarshi", "Shahrisabz", "Chiroqchi", "G'uzor", "Kasbi", "Kitob", "Koson", "Mirishkor", "Muborak", "Nishon", "Qamashi", "Yakkabog'"],
    "Surxondaryo viloyati": ["Termiz", "Angor", "Bandixon", "Boysun", "Denov", "Jarqo'rg'on", "Qiziriq", "Qumqo'rg'on", "Muzrabot", "Oltinsoy", "Sariosiyo", "Sherobod", "Sho'rchi", "Uzun"],
    "Buxoro viloyati": ["Buxoro", "G'ijduvon", "Jondor", "Kogon", "Qorakol", "Qorovulbozor", "Peshku", "Romitan", "Shofirkon", "Vobkent"],
    "Xorazm viloyati": ["Urganch", "Bog'ot", "Gurlan", "Xiva", "Xazorasp", "Qo'shko'pir", "Shovot", "Tuproqqal'a", "Yangiariq", "Yangibozor"],
    "Navoiy viloyati": ["Navoiy", "Karmana", "Konimex", "Navbahor", "Nurota", "Qiziltepa", "Tomdi", "Uchquduq", "Xatirchi"],
    "Jizzax viloyati": ["Jizzax", "Arnasoy", "Baxmal", "Do'stlik", "Forish", "G'allaorol", "Sharof Rashidov", "Mirzacho'l", "Paxtakor", "Yangiobod", "Zarbdor", "Zafarobod"],
    "Sirdaryo viloyati": ["Guliston", "Boyovut", "Havos", "Mirzaobod", "Oqoltin", "Sardoba", "Sayxunobod", "Shirin", "Xovos"],
    "Qoraqalpog'iston": ["Nukus", "Amudaryo", "Beruniy", "Chimboy", "Ellikkala", "Kegeyli", "Mo'ynoq", "Qanliko'l", "Qo'ng'irot", "Qorao'zak", "Shumanay", "Taxtako'pir", "To'rtko'l", "Xo'jayli"]
}


def is_work_time():
    now = datetime.now()
    return WORK_START <= now.hour < WORK_END


def main_menu(lang="uz"):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    if lang == "uz":
        markup.add(
            types.KeyboardButton("📝 Murojaat yuborish"),
            types.KeyboardButton("📋 Murojaatlarim")
        )
        markup.add(
            types.KeyboardButton("📞 Bog'lanish"),
            types.KeyboardButton("ℹ️ Ma'lumot")
        )
        markup.add(types.KeyboardButton("🌐 Tilni o'zgartirish"))
    elif lang == "ru":
        markup.add(
            types.KeyboardButton("📝 Отправить обращение"),
            types.KeyboardButton("📋 Мои обращения")
        )
        markup.add(
            types.KeyboardButton("📞 Связаться"),
            types.KeyboardButton("ℹ️ Информация")
        )
        markup.add(types.KeyboardButton("🌐 Сменить язык"))
    else:
        markup.add(
            types.KeyboardButton("📝 Send request"),
            types.KeyboardButton("📋 My requests")
        )
        markup.add(
            types.KeyboardButton("📞 Contact"),
            types.KeyboardButton("ℹ️ Information")
        )
        markup.add(types.KeyboardButton("🌐 Change language"))
    return markup


def region_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for region in REGIONS.keys():
        markup.add(types.KeyboardButton(region))
    return markup


def district_markup(region):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for district in REGIONS.get(region, []):
        markup.add(types.KeyboardButton(district))
    return markup


def rating_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    markup.add("⭐1", "⭐⭐2", "⭐⭐⭐3", "⭐⭐⭐⭐4", "⭐⭐⭐⭐⭐5")
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add("🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English")
    bot.send_message(message.chat.id,
        "👋 Salom!\n\n🌐 Tilni tanlang / Выберите язык / Choose language:",
        reply_markup=markup)


@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != ADMIN_ID:
        return
    total = len(requests_db)
    new = sum(1 for r in requests_db.values() if r['status'] == 'new')
    process = sum(1 for r in requests_db.values() if r['status'] == 'process')
    done = sum(1 for r in requests_db.values() if r['status'] == 'done')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("📊 Statistika", "📢 Hammaga xabar")
    markup.add("📋 Barcha murojaatlar")
    bot.send_message(message.chat.id,
        "👨‍💼 ADMIN PANEL\n\n"
        "📊 Statistika:\n"
        "📌 Jami: " + str(total) + "\n"
        "🆕 Yangi: " + str(new) + "\n"
        "⏳ Jarayonda: " + str(process) + "\n"
        "✅ Hal qilindi: " + str(done),
        reply_markup=markup)


@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.text == "📊 Statistika")
def admin_stats(message):
    admin_panel(message)


@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.text == "📢 Hammaga xabar")
def broadcast_start(message):
    user_data[message.chat.id] = {'admin_action': 'broadcast'}
    bot.send_message(message.chat.id, "📢 Yubormoqchi bo'lgan xabaringizni yozing:")
    bot.register_next_step_handler(message, do_broadcast)


def do_broadcast(message):
    if user_data.get(message.chat.id, {}).get('admin_action') != 'broadcast':
        return
    sent = 0
    for uid in set(r['user_id'] for r in requests_db.values()):
        try:
            bot.send_message(uid, "📢 Xabar:\n\n" + message.text)
            sent += 1
        except:
            pass
    bot.send_message(message.chat.id, "✅ " + str(sent) + " ta foydalanuvchiga yuborildi!")
    user_data[message.chat.id] = {}


@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.text == "📋 Barcha murojaatlar")
def all_requests(message):
    if not requests_db:
        bot.send_message(message.chat.id, "📋 Hozircha murojaat yo'q.")
        return
    for rid, r in list(requests_db.items())[-10:]:
        status_icon = "🆕" if r['status'] == 'new' else "⏳" if r['status'] == 'process' else "✅"
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("⏳ Jarayonda", callback_data="status_process_" + str(rid)),
            types.InlineKeyboardButton("✅ Hal qilindi", callback_data="status_done_" + str(rid))
        )
        markup.add(types.InlineKeyboardButton("💬 Javob berish", callback_data="reply_" + str(rid)))
        bot.send_message(message.chat.id,
            status_icon + " Murojaat #" + str(rid) + "\n"
            "👤 @" + str(r.get('username', 'noma\'lum')) + "\n"
            "📱 " + str(r.get('phone', '')) + "\n"
            "📍 " + str(r.get('region', '')) + ", " + str(r.get('district', '')) + "\n"
            "💼 " + str(r.get('job', '')) + "\n"
            "📝 " + str(r.get('request', '')) + "\n"
            "🕐 " + str(r.get('time', '')),
            reply_markup=markup)


@bot.callback_query_handler(func=lambda c: c.data.startswith("status_"))
def change_status(call):
    parts = call.data.split("_")
    new_status = parts[1]
    rid = int(parts[2])
    if rid in requests_db:
        requests_db[rid]['status'] = new_status
        uid = requests_db[rid]['user_id']
        lang = requests_db[rid].get('lang', 'uz')
        if new_status == 'process':
            icon = "⏳"
            if lang == 'uz':
                user_msg = "⏳ #" + str(rid) + " murojaatingiz ko'rib chiqilmoqda!"
            elif lang == 'ru':
                user_msg = "⏳ Ваше обращение #" + str(rid) + " рассматривается!"
            else:
                user_msg = "⏳ Your request #" + str(rid) + " is being reviewed!"
        else:
            icon = "✅"
            if lang == 'uz':
                user_msg = "✅ #" + str(rid) + " murojaatingiz hal qilindi!"
            elif lang == 'ru':
                user_msg = "✅ Ваше обращение #" + str(rid) + " решено!"
            else:
                user_msg = "✅ Your request #" + str(rid) + " has been resolved!"
        try:
            bot.send_message(uid, user_msg)
        except:
            pass
        bot.answer_callback_query(call.id, icon + " Status yangilandi!")


@bot.callback_query_handler(func=lambda c: c.data.startswith("reply_"))
def admin_reply(call):
    rid = int(call.data.split("_")[1])
    user_data[call.message.chat.id] = {'admin_action': 'reply', 'reply_to': rid}
    bot.send_message(call.message.chat.id, "💬 #" + str(rid) + " murojaatga javobingizni yozing:")
    bot.register_next_step_handler(call.message, send_reply)


def send_reply(message):
    if user_data.get(message.chat.id, {}).get('admin_action') != 'reply':
        return
    rid = user_data[message.chat.id].get('reply_to')
    if rid and rid in requests_db:
        uid = requests_db[rid]['user_id']
        lang = requests_db[rid].get('lang', 'uz')
        if lang == 'uz':
            prefix = "📩 #" + str(rid) + " murojaatingizga javob:\n\n"
        elif lang == 'ru':
            prefix = "📩 Ответ на ваше обращение #" + str(rid) + ":\n\n"
        else:
            prefix = "📩 Reply to your request #" + str(rid) + ":\n\n"
        try:
            bot.send_message(uid, prefix + message.text)
            bot.send_message(message.chat.id, "✅ Javob yuborildi!")
        except:
            bot.send_message(message.chat.id, "❌ Xatolik!")
    user_data[message.chat.id] = {}


@bot.message_handler(func=lambda m: m.text in ["🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English"])
def choose_lang(message):
    if "O'zbek" in message.text:
        lang = "uz"
        text = "✅ Til tanlandi! Quyidagi menyudan birini tanlang:"
    elif "Русский" in message.text:
        lang = "ru"
        text = "✅ Язык выбран! Выберите один из следующих:"
    else:
        lang = "en"
        text = "✅ Language selected! Choose one of the following:"
    user_data[message.chat.id] = {'lang': lang}
    bot.send_message(message.chat.id, text, reply_markup=main_menu(lang))


@bot.message_handler(func=lambda m: m.text in [
    "🌐 Tilni o'zgartirish", "🌐 Сменить язык", "🌐 Change language"])
def change_lang(message):
    start(message)


@bot.message_handler(func=lambda m: m.text in ["📞 Bog'lanish", "📞 Связаться", "📞 Contact"])
def contact(message):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')
    if lang == "uz":
        text = "📞 Biz bilan bog'laning:\n\n📱 Telefon: +998901234567\n📧 Email: info@example.uz\n🕐 Ish vaqti: 9:00 - 18:00"
    elif lang == "ru":
        text = "📞 Свяжитесь с нами:\n\n📱 Телефон: +998901234567\n📧 Email: info@example.uz\n🕐 Рабочее время: 9:00 - 18:00"
    else:
        text = "📞 Contact us:\n\n📱 Phone: +998901234567\n📧 Email: info@example.uz\n🕐 Working hours: 9:00 - 18:00"
    bot.send_message(message.chat.id, text, reply_markup=main_menu(lang))


@bot.message_handler(func=lambda m: m.text in ["ℹ️ Ma'lumot", "ℹ️ Информация", "ℹ️ Information"])
def info(message):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')
    if lang == "uz":
        text = "ℹ️ Bu bot orqali:\n✅ Murojaat yuborishingiz\n📋 Murojaat tarixini ko'rishingiz\n📩 Admin javobini olishingiz\n⭐ Baholashingiz mumkin!"
    elif lang == "ru":
        text = "ℹ️ Через этот бот:\n✅ Отправить обращение\n📋 История обращений\n📩 Получить ответ\n⭐ Оценить работу!"
    else:
        text = "ℹ️ Through this bot:\n✅ Send a request\n📋 Request history\n📩 Get a reply\n⭐ Rate our work!"
    bot.send_message(message.chat.id, text, reply_markup=main_menu(lang))


@bot.message_handler(func=lambda m: m.text in ["📋 Murojaatlarim", "📋 Мои обращения", "📋 My requests"])
def my_requests(message):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')
    user_reqs = [(rid, r) for rid, r in requests_db.items() if r['user_id'] == message.chat.id]
    if not user_reqs:
        if lang == 'uz':
            text = "📋 Sizda hali murojaat yo'q."
        elif lang == 'ru':
            text = "📋 У вас пока нет обращений."
        else:
            text = "📋 You have no requests yet."
        bot.send_message(message.chat.id, text, reply_markup=main_menu(lang))
        return
    text = "📋 Murojaatlaringiz:\n\n"
    for rid, r in user_reqs[-5:]:
        status = "🆕 Yangi" if r['status'] == 'new' else "⏳ Jarayonda" if r['status'] == 'process' else "✅ Hal qilindi"
        text += "#" + str(rid) + " - " + status + "\n📝 " + str(r.get('request', ''))[:30] + "...\n🕐 " + str(r.get('time', '')) + "\n\n"
    bot.send_message(message.chat.id, text, reply_markup=main_menu(lang))


@bot.message_handler(func=lambda m: m.text in [
    "📝 Murojaat yuborish", "📝 Отправить обращение", "📝 Send request"])
def start_request(message):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')

    if not is_work_time():
        if lang == 'uz':
            text = "🕐 Hozir ish vaqtimiz emas!\n\nIsh vaqti: 9:00 - 18:00\n\nLekin murojaatingizni yuborishingiz mumkin, ish vaqtida javob beramiz! ✅"
        elif lang == 'ru':
            text = "🕐 Сейчас не рабочее время!\n\nРабочее время: 9:00 - 18:00\n\nНо вы можете отправить обращение, мы ответим в рабочее время! ✅"
        else:
            text = "🕐 It's not working hours!\n\nWorking hours: 9:00 - 18:00\n\nBut you can send a request, we'll reply during working hours! ✅"
        bot.send_message(message.chat.id, text)

    user_data[message.chat.id]['step'] = 'phone'

    if lang == "uz":
        text = "📱 Telefon raqamingizni yuboring:"
        btn_text = "📱 Raqamimni yuborish"
    elif lang == "ru":
        text = "📱 Отправьте ваш номер телефона:"
        btn_text = "📱 Отправить мой номер"
    else:
        text = "📱 Send your phone number:"
        btn_text = "📱 Send my number"

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(btn_text, request_contact=True))
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')
    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text
    user_data[message.chat.id]['phone'] = phone

    if lang == "uz":
        text = "📍 Viloyatingizni tanlang:"
    elif lang == "ru":
        text = "📍 Выберите область:"
    else:
        text = "📍 Select your region:"
    bot.send_message(message.chat.id, text, reply_markup=region_markup())
    bot.register_next_step_handler(message, get_region)


def get_region(message):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')
    if message.text not in REGIONS:
        if lang == 'uz':
            bot.send_message(message.chat.id, "❗ Iltimos, viloyatni tanlang:", reply_markup=region_markup())
        else:
            bot.send_message(message.chat.id, "❗ Please select a region:", reply_markup=region_markup())
        bot.register_next_step_handler(message, get_region)
        return
    user_data[message.chat.id]['region'] = message.text

    if lang == "uz":
        text = "📍 Tumaningizni tanlang:"
    elif lang == "ru":
        text = "📍 Выберите район:"
    else:
        text = "📍 Select your district:"
    bot.send_message(message.chat.id, text, reply_markup=district_markup(message.text))
    bot.register_next_step_handler(message, get_district)


def get_district(message):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')
    region = user_data[message.chat.id].get('region', '')
    if message.text not in REGIONS.get(region, []):
        bot.send_message(message.chat.id, "❗ Iltimos, tumanni tanlang:", reply_markup=district_markup(region))
        bot.register_next_step_handler(message, get_district)
        return
    user_data[message.chat.id]['district'] = message.text

    if lang == "uz":
        text = "💼 Kasbingiz nima?\n\nMasalan: O'qituvchi, Shifokor..."
    elif lang == "ru":
        text = "💼 Ваша профессия?\n\nНапример: Учитель, Врач..."
    else:
        text = "💼 What is your profession?\n\nExample: Teacher, Doctor..."
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(message, get_job)


def get_job(message):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')
    user_data[message.chat.id]['job'] = message.text

    if lang == "uz":
        text = "📝 Murojaatingizni yozing:\n\n📎 Rasm yoki fayl ham yuborishingiz mumkin!"
    elif lang == "ru":
        text = "📝 Напишите ваше обращение:\n\n📎 Можно также отправить фото или файл!"
    else:
        text = "📝 Write your request:\n\n📎 You can also send a photo or file!"
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, get_request)


def get_request(message):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')
    data = user_data[message.chat.id]

    if message.photo:
        data['request'] = message.caption or "Rasm yuborildi"
        data['photo_id'] = message.photo[-1].file_id
    elif message.document:
        data['request'] = message.caption or "Fayl yuborildi"
        data['doc_id'] = message.document.file_id
    else:
        data['request'] = message.text

    request_counter[0] += 1
    rid = request_counter[0]
    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    requests_db[rid] = {
        'user_id': message.chat.id,
        'username': message.from_user.username or "noma'lum",
        'lang': lang,
        'phone': data.get('phone', ''),
        'region': data.get('region', ''),
        'district': data.get('district', ''),
        'job': data.get('job', ''),
        'request': data.get('request', ''),
        'photo_id': data.get('photo_id', None),
        'doc_id': data.get('doc_id', None),
        'status': 'new',
        'time': now
    }

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("⏳ Jarayonda", callback_data="status_process_" + str(rid)),
        types.InlineKeyboardButton("✅ Hal qilindi", callback_data="status_done_" + str(rid))
    )
    markup.add(types.InlineKeyboardButton("💬 Javob berish", callback_data="reply_" + str(rid)))

    admin_msg = (
        "🔔 YANGI MUROJAAT #" + str(rid) + "\n"
        "==================\n"
        "👤 @" + str(data.get('username', requests_db[rid]['username'])) + "\n"
        "🆔 ID: " + str(message.chat.id) + "\n"
        "🌐 Til: " + str(lang.upper()) + "\n"
        "==================\n"
        "📱 Telefon: " + str(data.get('phone', '')) + "\n"
        "📍 " + str(data.get('region', '')) + ", " + str(data.get('district', '')) + "\n"
        "💼 Kasb: " + str(data.get('job', '')) + "\n"
        "==================\n"
        "📝 Murojaat: " + str(data.get('request', '')) + "\n"
        "🕐 Vaqt: " + now + "\n"
        "=================="
    )

    if data.get('photo_id'):
        bot.send_photo(ADMIN_ID, data['photo_id'], caption=admin_msg, reply_markup=markup)
    elif data.get('doc_id'):
        bot.send_document(ADMIN_ID, data['doc_id'], caption=admin_msg, reply_markup=markup)
    else:
        bot.send_message(ADMIN_ID, admin_msg, reply_markup=markup)

    if lang == "uz":
        done_text = "✅ Murojaatingiz qabul qilindi! (#" + str(rid) + ")\n\n⚡ Tez orada javob beramiz!\n\nRahmat! 🙏"
        rate_text = "⭐ Xizmatimizni baholang:"
    elif lang == "ru":
        done_text = "✅ Ваше обращение принято! (#" + str(rid) + ")\n\n⚡ Мы скоро ответим!\n\nСпасибо! 🙏"
        rate_text = "⭐ Оцените наш сервис:"
    else:
        done_text = "✅ Your request received! (#" + str(rid) + ")\n\n⚡ We will respond soon!\n\nThank you! 🙏"
        rate_text = "⭐ Rate our service:"

    bot.send_message(message.chat.id, done_text, reply_markup=main_menu(lang))
    bot.send_message(message.chat.id, rate_text, reply_markup=rating_markup())
    bot.register_next_step_handler(message, get_rating, rid)


def get_rating(message, rid):
    lang = user_data.get(message.chat.id, {}).get('lang', 'uz')
    rating = message.text
    if rid in requests_db:
        requests_db[rid]['rating'] = rating
    bot.send_message(ADMIN_ID, "⭐ #" + str(rid) + " murojaatga baho: " + rating)
    if lang == 'uz':
        text = "🙏 Bahoingiz uchun rahmat!"
    elif lang == 'ru':
        text = "🙏 Спасибо за оценку!"
    else:
        text = "🙏 Thank you for rating!"
    bot.send_message(message.chat.id, text, reply_markup=main_menu(lang))
bot.polling()

