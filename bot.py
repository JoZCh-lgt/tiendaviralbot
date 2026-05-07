import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
import requests

# 1. Pega tu Token de Telegram
TOKEN_TELEGRAM = '8281697686:AAEBf29VABSA1BH6D7-jX8WEas4xXndGJic'
bot = telebot.TeleBot(TOKEN_TELEGRAM)

# 2. Pega tu API Token de CryptoBot
TOKEN_CRYPTO = '578542:AA8vQa975AdFGA0d6A5J9CaY6p4tKMyAmCv'
URL_CRYPTO = "https://pay.crypt.bot/api/"

# Memoria para autolimpieza
historial_imagenes = {}

# ==========================================
# 🛠️ DICCIONARIO MAESTRO DE TEXTOS (ES/EN)
# ==========================================
textos = {
    "es": {
        "saludo": "¡Hola! Bienvenido a la Tienda Viral 🚀. Elige una opción:",
        "btn_descargas": "📥 Descargas Gratis",
        "btn_exclusivo": "💎 Contenido VIP",
        "volver": "🔙 Volver",
        "titulo_gratis": "📥 ZONA DE MUESTRAS GRATUITAS\n\nSelecciona la galería que deseas ver:",
        "titulo_vip": "🔒 ZONA VIP EXCLUSIVA\n\nAdquiere el paquete completo en ZIP:",
        "msj_volver": "Has vuelto al menú principal 🏠. Elige una opción:",
        "generando": "⏳ Conectando con la blockchain para generar tu factura...",
        "factura_lista": "✅ Factura de **{} USDT** lista.\n\n1️⃣ Haz clic en 'Pagar'.\n2️⃣ Paga en CryptoBot.\n3️⃣ Presiona 'Ya pagué'.",
        "btn_pagar": "💳 Pagar con CryptoBot",
        "btn_verificar": "✅ Ya pagué (Verificar)",
        "abriendo": "✅ Abriendo galería de {}...",
        "caption_gratis": "🎁 Muestra gratuita: {}\n\n👉 *Si te gusta, compra el ZIP en la Zona VIP.*",
        "pago_ok": "✅ ¡PAGO APROBADO! 🎉\n\nEnlace de descarga ZIP:\n👉 {}",
        "espera_pago": "⏳ Aún no detectamos el pago. Espera unos segundos e intenta de nuevo.",
        "error_factura": "❌ Error al crear la factura.",
        "no_links": "⚠️ Esta carpeta aún no tiene links configurados."
    },
    "en": {
        "saludo": "Hello! Welcome to the Viral Store 🚀. Choose an option:",
        "btn_descargas": "📥 Free Downloads",
        "btn_exclusivo": "💎 VIP Content",
        "volver": "🔙 Back",
        "titulo_gratis": "📥 FREE SAMPLES ZONE\n\nSelect the gallery you want to view:",
        "titulo_vip": "🔒 EXCLUSIVE VIP ZONE\n\nGet the full ZIP pack instantly:",
        "msj_volver": "Back to main menu 🏠. Choose an option:",
        "generando": "⏳ Connecting to blockchain to generate your invoice...",
        "factura_lista": "✅ **{} USDT** Invoice ready.\n\n1️⃣ Click 'Pay Now'.\n2️⃣ Pay in CryptoBot.\n3️⃣ Press 'I paid'.",
        "btn_pagar": "💳 Pay with CryptoBot",
        "btn_verificar": "✅ I paid (Verify)",
        "abriendo": "✅ Opening {} gallery...",
        "caption_gratis": "🎁 Free sample: {}\n\n👉 *If you like it, get the full ZIP in the VIP Zone.*",
        "pago_ok": "✅ PAYMENT APPROVED! 🎉\n\nZIP download link:\n👉 {}",
        "espera_pago": "⏳ Payment not detected yet. Please wait a few seconds and try again.",
        "error_factura": "❌ Error creating invoice.",
        "no_links": "⚠️ No links configured for this folder."
    }
}

# ==========================================
# 📁 CONFIGURACIÓN DE CARPETAS (10 GRATIS / 10 VIP)
# ==========================================
PACKS_GRATIS = {
    "g1": {"nombre": "📁 Sophie Rain", "imgs": ["https://postimg.cc/PvWWZ53N", "https://postimg.cc/fV2xYFKh", "https://postimg.cc/RJBfMzS4", "https://postimg.cc/756zP9kC", "https://postimg.cc/CBjBr6jX"]},
    "g2": {"nombre": "📁 Lexi Marvel", "imgs": ["https://i.postimg.cc/fy36SQKT/1.jpg", "https://postimg.cc/xX469qWr", "https://postimg.cc/zyV9wmrp", "https://postimg.cc/9zCK8w2z", "https://postimg.cc/hJVZMc3C"]},
    "g3": {"nombre": "📁 EmaraB", "imgs": ["https://postimg.cc/9Dfjx830", "https://postimg.cc/TLn8yBby", "https://postimg.cc/n916270F", "https://postimg.cc/svjXrJFW", "https://postimg.cc/Xrh79Srg",]},
    "g4": {"nombre": "📁 Tana Rein", "imgs": ["https://postimg.cc/bdj014bd", "https://postimg.cc/RWqwMm5z", "https://postimg.cc/sQCW9ZM4", "https://postimg.cc/4nZtYVkZ", "https://postimg.cc/PP5w4Hqq",]},
    "g5": {"nombre": "📁 Vega Thompson", "imgs": ["https://postimg.cc/p9Tcb4Cw", "https://postimg.cc/BPxMB0ZY", "https://postimg.cc/bZ6LTL8X", "https://postimg.cc/XBckykxc", "https://postimg.cc/rKj9VgDS",]},
    "g6": {"nombre": "📁 Mikaela Testa", "imgs": ["https://postimg.cc/YGjSFrRk", "https://postimg.cc/6yCpn1dk", "https://postimg.cc/mz0TFQhb", "https://postimg.cc/kBPnJF0J", "https://postimg.cc/9DJVB3rm",]},
    "g7": {"nombre": "📁 Corinna Kopf", "imgs": ["https://postimg.cc/K1XQs43P", "https://postimg.cc/Jyxqnq62", "https://postimg.cc/5QYqsMxg", "https://postimg.cc/dDp9LDBn", "https://postimg.cc/Z9b81NbF",]},
    "g8": {"nombre": "📁 Breckie Hill", "imgs": ["https://postimg.cc/2qwhzScz", "https://postimg.cc/WDTBC5q9", "https://postimg.cc/BPLkHyRs", "https://postimg.cc/dDpzwsTs", "https://postimg.cc/JsWvHpqd",]},
    "g9": {"nombre": "📁 Hannah Palmer", "imgs": ["https://postimg.cc/MMjmDSKw", "https://postimg.cc/kByFww9M", "https://postimg.cc/QK31JKyH", "https://postimg.cc/jD5NcbZz", "https://postimg.cc/34gDNJxK",]},
    "g10": {"nombre": "📁 Kirstentoosweet", "imgs": ["https://postimg.cc/sQkd6sYg", "https://postimg.cc/ZCFtHkCt", "https://postimg.cc/G4X00kP2", "https://postimg.cc/DJbRbHtN", "https://postimg.cc/dZ2X5dtc",]}
}

PACKS_VIP = {
    "v1": {"nombre": "💎 Sophie Raein 10 📹 + 10 📸", "precio": "0.50", "link": "https://www.mediafire.com/file/cnha2a6qji2ysep/SophieRain.zip/file"},
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
# --- FUNCIONES DE INTERFAZ ---
def crear_menu_principal(lang):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(textos[lang]["btn_descargas"], callback_data=f"menu_gratis_{lang}"))
    markup.add(InlineKeyboardButton(textos[lang]["btn_exclusivo"], callback_data=f"menu_vip_{lang}"))
    return markup

@bot.message_handler(commands=['start'])
def enviar_idiomas(message):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"), InlineKeyboardButton("🇺🇸 English", callback_data="lang_en"))
    bot.reply_to(message, "🌍 Choose language / Elige idioma:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def responder_botones(call):
    chat_id = call.message.chat.id
    msg_id = call.message.message_id
    data = call.data.split("_")
    
    # 1. Selección inicial de idioma
    if data[0] == "lang":
        lang = data[1]
        bot.delete_message(chat_id, msg_id)
        bot.send_message(chat_id, textos[lang]["saludo"], reply_markup=crear_menu_principal(lang))

    # 2. Volver al inicio (manteniendo el idioma)
    elif data[0] == "volver":
        lang = data[1]
        bot.edit_message_text(textos[lang]["msj_volver"], chat_id, msg_id, reply_markup=crear_menu_principal(lang))

    # 3. Menú de Descargas Gratis
    elif data[0] == "menu" and data[1] == "gratis":
        lang = data[2]
        markup = InlineKeyboardMarkup(row_width=1)
        for id_p, p in PACKS_GRATIS.items():
            markup.add(InlineKeyboardButton(p["nombre"], callback_data=f"show_{id_p}_{lang}"))
        markup.add(InlineKeyboardButton(textos[lang]["volver"], callback_data=f"volver_{lang}"))
        bot.edit_message_text(textos[lang]["titulo_gratis"], chat_id, msg_id, reply_markup=markup)

    # 4. Menú VIP
    elif data[0] == "menu" and data[1] == "vip":
        lang = data[2]
        markup = InlineKeyboardMarkup(row_width=1)
        for id_p, p in PACKS_VIP.items():
            markup.add(InlineKeyboardButton(f"{p['nombre']} - ${p['precio']} USDT", callback_data=f"buy_{id_p}_{lang}"))
        markup.add(InlineKeyboardButton(textos[lang]["volver"], callback_data=f"volver_{lang}"))
        bot.edit_message_text(textos[lang]["titulo_vip"], chat_id, msg_id, reply_markup=markup)

    # 5. Mostrar Álbum (Media Group) + Autolimpieza
    elif data[0] == "show":
        id_p, lang = data[1], data[2]
        pack = PACKS_GRATIS[id_p]
        
        if "LINK_" in pack['imgs'][0]:
            bot.answer_callback_query(call.id, textos[lang]["no_links"], show_alert=True)
            return

        # Limpiar mensajes anteriores
        if chat_id in historial_imagenes:
            for m_id in historial_imagenes[chat_id]:
                try: bot.delete_message(chat_id, m_id)
                except: pass
        historial_imagenes[chat_id] = []

        m_aviso = bot.send_message(chat_id, textos[lang]["abriendo"].format(pack['nombre']))
        album = [InputMediaPhoto(link) for link in pack['imgs']]
        album[0].caption = textos[lang]["caption_gratis"].format(pack['nombre'])
        album[0].parse_mode = "Markdown"
        
        m_album = bot.send_media_group(chat_id, album)
        historial_imagenes[chat_id].append(m_aviso.message_id)
        for m in m_album: historial_imagenes[chat_id].append(m.message_id)

    # 6. Generar Factura Crypto
    elif data[0] == "buy":
        id_p, lang = data[1], data[2]
        pack = PACKS_VIP[id_p]
        bot.send_message(chat_id, textos[lang]["generando"])
        
        headers = {"Crypto-Pay-API-Token": TOKEN_CRYPTO}
        payload = {"asset": "USDT", "amount": pack['precio'], "description": pack['nombre']}
        
        try:
            res = requests.post(URL_CRYPTO + "createInvoice", headers=headers, data=payload).json()
            if res.get("ok"):
                inv_id = res["result"]["invoice_id"]
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton(textos[lang]["btn_pagar"], url=res["result"]["pay_url"]))
                markup.add(InlineKeyboardButton(textos[lang]["btn_verificar"], callback_data=f"check_{inv_id}_{id_p}_{lang}"))
                bot.send_message(chat_id, textos[lang]["factura_lista"].format(pack['precio']), parse_mode="Markdown", reply_markup=markup)
        except: bot.send_message(chat_id, textos[lang]["error_factura"])

    # 7. Verificar Pago
    elif data[0] == "check":
        inv_id, id_p, lang = data[1], data[2], data[3]
        headers = {"Crypto-Pay-API-Token": TOKEN_CRYPTO}
        try:
            res = requests.get(URL_CRYPTO + "getInvoices", headers=headers, params={"invoice_ids": inv_id}).json()
            if res.get("ok") and res["result"]["items"][0]["status"] == "paid":
                bot.edit_message_text(textos[lang]["pago_ok"].format(PACKS_VIP[id_p]["link"]), chat_id, msg_id)
            else:
                bot.answer_callback_query(call.id, textos[lang]["espera_pago"], show_alert=True)
        except: pass

# --- EL CORAZÓN PARA LA NUBE (FLASK) ---
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "¡Mi Tienda Viral está viva y trabajando 24/7!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

threading.Thread(target=run_flask).start()

print("¡La Tienda Cripto está lista para la Nube!")
bot.infinity_polling()
