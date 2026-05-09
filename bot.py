import telebot
from telebot import types
from flask import Flask
import threading
import os
import requests

# ==========================================
# 1. TUS TOKENS
# ==========================================
TOKEN = "8281697686:AAEBf29VABSA1BH6D7-jX8WEas4xXndGJic" 
CRYPTO_TOKEN = "578542:AA8vQa975AdFGA0d6A5J9CaY6p4tKMyAmCv" 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

user_langs = {} # Memoria de idiomas

# ==========================================
# 2. BASE DE DATOS DE LINKS
# ==========================================
# 🎁 LINKS GRATIS (10 carpetas x 5 espacios)
PACK_GRATIS = {
    "g1": {"nombre": "📁 Sophie Rain", "imgs": ["https://postimg.cc/PvWWZ53N", "https://postimg.cc/fV2xYFKh", "https://postimg.cc/RJBfMzS4", "https://postimg.cc/756zP9kC", "https://postimg.cc/CBjBr6jX"]},
    "g2": {"nombre": "📁 Lexi Marvel", "imgs": ["https://i.postimg.cc/fy36SQKT/1.jpg", "https://postimg.cc/xX469qWr", "https://postimg.cc/zyV9wmrp", "https://postimg.cc/9zCK8w2z", "https://postimg.cc/hJVZMc3C"]},
    "g3": {"nombre": "📁 EmaraB", "imgs": ["https://postimg.cc/9Dfjx830", "https://postimg.cc/TLn8yBby", "https://postimg.cc/n916270F", "https://postimg.cc/svjXrJFW", "https://postimg.cc/Xrh79Srg"]},
    "g4": {"nombre": "📁 Tana Rein", "imgs": ["https://postimg.cc/bdj014bd", "https://postimg.cc/RWqwMm5z", "https://postimg.cc/sQCW9ZM4", "https://postimg.cc/4nZtYVkZ", "https://postimg.cc/PP5w4Hqq"]},
    "g5": {"nombre": "📁 Vega Thompson", "imgs": ["https://postimg.cc/p9Tcb4Cw", "https://postimg.cc/BPxMB0ZY", "https://postimg.cc/bZ6LTL8X", "https://postimg.cc/XBckykxc", "https://postimg.cc/rKj9VgDS"]},
    "g6": {"nombre": "📁 Mikaela Testa", "imgs": ["https://postimg.cc/YGjSFrRk", "https://postimg.cc/6yCpn1dk", "https://postimg.cc/mz0TFQhb", "https://postimg.cc/kBPnJF0J", "https://postimg.cc/9DJVB3rm"]},
    "g7": {"nombre": "📁 Corinna Kopf", "imgs": ["https://postimg.cc/K1XQs43P", "https://postimg.cc/Jyxqnq62", "https://postimg.cc/5QYqsMxg", "https://postimg.cc/dDp9LDBn", "https://postimg.cc/Z9b81NbF"]},
    "g8": {"nombre": "📁 Breckie Hill", "imgs": ["https://postimg.cc/2qwhzScz", "https://postimg.cc/WDTBC5q9", "https://postimg.cc/BPLkHyRs", "https://postimg.cc/dDpzwsTs", "https://postimg.cc/JsWvHpqd"]},
    "g9": {"nombre": "📁 Hannah Palmer", "imgs": ["https://postimg.cc/MMjmDSKw", "https://postimg.cc/kByFww9M", "https://postimg.cc/QK31JKyH", "https://postimg.cc/jD5NcbZz", "https://postimg.cc/34gDNJxK"]},
    "g10": {"nombre": "📁 Kirstentoosweet", "imgs": ["https://postimg.cc/sQkd6sYg", "https://postimg.cc/ZCFtHkCt", "https://postimg.cc/G4X00kP2", "https://postimg.cc/DJbRbHtN", "https://postimg.cc/dZ2X5dtc"]}
}

# 💎 LINKS VIP (10 carpetas individuales + 1 Todo en Uno)
PACKS_VIP = {
    "v1": {"nombre": "💎 Sophie Raein 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/cnha2a6qji2ysep/SophieRain.zip/file"},
    "v2": {"nombre": "💎 Lexi Marvel 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/6igmvzfxxjypg62/Lexi+Marvel.zip/file"},
    "v3": {"nombre": "💎 EmaraB 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/9939prl9lrb7zvm/EmaraB.zip/file"},
    "v4": {"nombre": "💎 Tana Rein 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/s8mo3quupi2arcg/Tana+Rein.zip/file"},
    "v5": {"nombre": "💎 Vega Thompson 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/0tjl2n4wyy5dnw4/Vega+Thompson.zip/file"},
    "v6": {"nombre": "💎 Mikaela Testa 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/lpd76dlz1h4984e/Mikaela+Testa.zip/file"},
    "v7": {"nombre": "💎 Corina Kopf 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/sp5met6tkm0z53r/Corinna+Kopf.zip/file"},
    "v8": {"nombre": "💎 Breckie Hill 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/tpu2xcpwyu771qx/Breckie+Hill.zip/file"},
    "v9": {"nombre": "💎 Hanna Palmer 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/ta9krljkn20vt9p/Hanna+Palmer.zip/file"},
    "v10": {"nombre": "💎 Kirstentoosweet 10 📹 + 10 📸", "precio": "5.00", "link": "https://www.mediafire.com/file/bf2u4lja9htkshn/Kirstentoosweet.zip/file"},
    "v11": {"nombre": "💎 MEGA PACK ALL IN ONE", "precio": "30.00", "link": "https://www.mediafire.com/file/ubhl92ic9alix8v/All+in+one.zip/file"}
}

# ==========================================
# 3. TEXTOS (INGLÉS / ESPAÑOL)
# ==========================================
T = {
    "en": {
        "main_menu": "🔥 **MAIN MENU** 🔥\nChoose an option:",
        "btn_free": "🎁 Free Content",
        "btn_vip": "💎 VIP Content",
        "menu_free": "🎁 **FREE VAULT**\nSelect a folder:",
        "menu_vip": "💎 **VIP VAULT**\nSelect a premium folder:",
        "btn_back": "⬅️ Back to Menu",
        "pay_title": "Select payment method for",
        "btn_stars": "⭐️ Pay with Stars",
        "btn_usdt": "💵 Pay with USDT",
        "pay_crypto": "🔗 Click below to pay with USDT. After paying, click 'Verify Payment'.",
        "btn_pay_url": "💳 Pay Here",
        "btn_verify": "✅ Verify Payment",
        "success": "✅ **PAYMENT SUCCESSFUL!**\n\nHere is your VIP access:\n",
        "wait": "⏳ Payment not detected yet. Try again in a few seconds.",
        "free_msg": "Enjoy your free preview! 🎁\n"
    },
    "es": {
        "main_menu": "🔥 **MENÚ PRINCIPAL** 🔥\nElige una opción:",
        "btn_free": "🎁 Contenido Gratis",
        "btn_vip": "💎 Contenido VIP",
        "menu_free": "🎁 **BÓVEDA GRATIS**\nSelecciona una carpeta:",
        "menu_vip": "💎 **BÓVEDA VIP**\nSelecciona una carpeta premium:",
        "btn_back": "⬅️ Volver al Menú",
        "pay_title": "Selecciona método de pago para",
        "btn_stars": "⭐️ Pagar con Estrellas",
        "btn_usdt": "💵 Pagar con USDT",
        "pay_crypto": "🔗 Haz clic abajo para pagar con USDT. Luego haz clic en 'Verificar Pago'.",
        "btn_pay_url": "💳 Pagar Aquí",
        "btn_verify": "✅ Verificar Pago",
        "success": "✅ **¡PAGO EXITOSO!**\n\nAquí tienes tu acceso VIP:\n",
        "wait": "⏳ Aún no detectamos el pago. Espera unos segundos y vuelve a verificar.",
        "free_msg": "¡Disfruta tu contenido gratis! 🎁\n"
    }
}

# ==========================================
# 4. FUNCIONES DE CRYPTOBOT API
# ==========================================
def create_crypto_invoice(amount, item_id):
    headers = {"Crypto-Pay-API-Token": CRYPTO_TOKEN}
    payload = {"asset": "USDT", "amount": str(amount), "description": f"VIP Access"}
    try:
        res = requests.post("https://pay.crypt.bot/api/createInvoice", headers=headers, json=payload).json()
        if res.get("ok"):
            return res["result"]["pay_url"], res["result"]["invoice_id"]
    except:
        pass
    return None, None

def check_crypto_payment(invoice_id):
    headers = {"Crypto-Pay-API-Token": CRYPTO_TOKEN}
    try:
        res = requests.get(f"https://pay.crypt.bot/api/getInvoices?invoice_ids={invoice_id}", headers=headers).json()
        if res.get("ok") and len(res["result"]["items"]) > 0:
            return res["result"]["items"][0]["status"] == "paid"
    except:
        pass
    return False

# ==========================================
# 5. LÓGICA DEL BOT
# ==========================================
@app.route('/')
def index():
    return "Máquina VIP 100% Automática (Estrellas + Crypto) Online 🚀"

# Comando /start - Idiomas
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"),
        types.InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")
    )
    bot.send_message(message.chat.id, "Select your language / Selecciona tu idioma:", reply_markup=markup)

def show_main_menu(chat_id, message_id, lang):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(T[lang]["btn_free"], callback_data="menu_free"),
        types.InlineKeyboardButton(T[lang]["btn_vip"], callback_data="menu_vip")
    )
    bot.edit_message_text(T[lang]["main_menu"], chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data
    lang = user_langs.get(chat_id, "en") # Por defecto inglés

    # 1. Configurar Idioma
    if data in ["lang_en", "lang_es"]:
        user_langs[chat_id] = "en" if data == "lang_en" else "es"
        show_main_menu(chat_id, msg_id, user_langs[chat_id])
    
    # 2. Volver al Menú
    elif data == "back_main":
        show_main_menu(chat_id, msg_id, lang)

    # 3. Menú Gratis (Lee los botones automáticamente)
    elif data == "menu_free":
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = [types.InlineKeyboardButton(pack["nombre"], callback_data=f"getfree_{key}") for key, pack in PACK_GRATIS.items()]
        markup.add(*buttons)
        markup.add(types.InlineKeyboardButton(T[lang]["btn_back"], callback_data="back_main"))
        bot.edit_message_text(T[lang]["menu_free"], chat_id, msg_id, parse_mode="Markdown", reply_markup=markup)

    # 4. Entregar Gratis (COMO ÁLBUM DE FOTOS)
    elif data.startswith("getfree_"):
        key = data.replace("getfree_", "")
        pack = PACK_GRATIS[key]
        
        # Le avisamos al usuario que se está cargando para que no se desespere
        bot.send_message(chat_id, "⏳...")
        
        try:
            # Preparamos el álbum
            media_group = []
            for i, url in enumerate(pack['imgs']):
                # Ponemos el texto de saludo solo en la primera foto
                caption = f"🎁 **{pack['nombre']}**\n{T[lang]['free_msg']}" if i == 0 else None
                media_group.append(types.InputMediaPhoto(media=url, caption=caption, parse_mode="Markdown"))
            
            # Enviamos el álbum
            bot.send_media_group(chat_id, media=media_group)
        
        except Exception as e:
            # Si falla (porque no son links .jpg o .png directos), mandamos como texto
            mensaje_error = f"⚠️ Nota: Para ver estas imágenes como un álbum, asegúrate de configurar los **Enlaces Directos** en tu código.\n\n🎁 **{pack['nombre']}**\n" + "\n".join([f"{i+1}. {l}" for i, l in enumerate(pack['imgs'])])
            bot.send_message(chat_id, mensaje_error, parse_mode="Markdown")

    # 5. Menú VIP (Lee los botones automáticamente)
    elif data == "menu_vip":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, pack in PACKS_VIP.items():
            markup.add(types.InlineKeyboardButton(f"{pack['nombre']} - ${pack['precio']}", callback_data=f"paymenu_{key}"))
        markup.add(types.InlineKeyboardButton(T[lang]["btn_back"], callback_data="back_main"))
        bot.edit_message_text(T[lang]["menu_vip"], chat_id, msg_id, parse_mode="Markdown", reply_markup=markup)

    # 6. Selección de Método de Pago
    elif data.startswith("paymenu_"):
        item_id = data.replace("paymenu_", "")
        pack = PACKS_VIP[item_id]
        
        precio_usd = float(pack["precio"])
        stars_p = int(precio_usd * 50)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(f"{T[lang]['btn_stars']} ({stars_p} ⭐️)", callback_data=f"stars_{item_id}"),
            types.InlineKeyboardButton(f"{T[lang]['btn_usdt']} (${precio_usd:.2f})", callback_data=f"crypto_{item_id}"),
            types.InlineKeyboardButton(T[lang]["btn_back"], callback_data="menu_vip")
        )
        bot.edit_message_text(f"💳 {T[lang]['pay_title']} **{pack['nombre']}**:", chat_id, msg_id, parse_mode="Markdown", reply_markup=markup)

    # 7. Factura de Estrellas
    elif data.startswith("stars_"):
        item_id = data.replace("stars_", "")
        pack = PACKS_VIP[item_id]
        stars_p = int(float(pack["precio"]) * 50)
        
        titulo_limpio = pack['nombre'].replace("💎", "").strip()[:32] 
        
        bot.send_invoice(chat_id, title=titulo_limpio, description="VIP Access 🔓", provider_token="", currency="XTR", 
                         prices=[types.LabeledPrice(label="VIP", amount=stars_p)], invoice_payload=f"check_{item_id}")

    # 8. Factura de USDT
    elif data.startswith("crypto_"):
        item_id = data.replace("crypto_", "")
        pack = PACKS_VIP[item_id]
        usdt_p = pack["precio"]
        
        bot.edit_message_text("⏳ Generating secure invoice...", chat_id, msg_id)
        pay_url, invoice_id = create_crypto_invoice(usdt_p, item_id)
        
        if pay_url:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton(T[lang]["btn_pay_url"], url=pay_url),
                types.InlineKeyboardButton(T[lang]["btn_verify"], callback_data=f"verify_{invoice_id}_{item_id}"),
                types.InlineKeyboardButton(T[lang]["btn_back"], callback_data="menu_vip")
            )
            bot.edit_message_text(T[lang]["pay_crypto"], chat_id, msg_id, reply_markup=markup)

    # 9. Verificar Pago USDT
    elif data.startswith("verify_"):
        partes = data.split("_")
        invoice_id = partes[1]
        item_id = partes[2]
        
        if check_crypto_payment(invoice_id):
            link = PACKS_VIP[item_id]['link']
            bot.send_message(chat_id, f"{T[lang]['success']}{link}", parse_mode="Markdown")
            bot.edit_message_text("✅ Access Granted.", chat_id, msg_id) 
        else:
            bot.answer_callback_query(call.id, T[lang]["wait"], show_alert=True)

# ==========================================
# 6. VERIFICAR PAGO ESTRELLAS
# ==========================================
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    chat_id = message.chat.id
    lang = user_langs.get(chat_id, "en")
    item_id = message.successful_payment.invoice_payload.replace("check_", "")
    link = PACKS_VIP[item_id]['link']
    
    bot.send_message(chat_id, f"{T[lang]['success']}{link}", parse_mode="Markdown")

# Ejecución
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
