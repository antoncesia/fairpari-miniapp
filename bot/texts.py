"""Тексты бота по языкам.

Источник — русские тексты из брифа (таблица «FairPari (339) — TG bot brief» и новый бриф).
EN / ES / PT / UZ — ЧЕРНОВОЙ перевод для прототипа: по договорённости (С-05) финальные
переводы делают переводчики разработки, FairPari вычитывает.
"""

LANGS = ("en", "pt", "uz", "es")          # С-04: английский, португальский, узбекский, испанский
DEFAULT_LANG = "en"                       # «основной язык» брифа для экрана выбора языка

LANG_NAMES = {"en": "English", "pt": "Português", "uz": "O‘zbekcha", "es": "Español"}

# С-09 / В-05: суммы бонуса по языку. Для ES взято решение FairPari из документа с вопросами
# (Аргентина → ARS); в новом брифе для ES стоит €. Для PT — € (язык под вопросом, В-04).
BONUS = {
    "en": ("€100", "€1,500"),
    "pt": ("€100", "€1,500"),
    "uz": ("1,300,000 UZS", "20,500,000 UZS"),
    "es": ("170,000 ARS", "2,500,000 ARS"),
}

# С-10: каналы по языку и поддержка
CHANNELS = {
    "uz": "https://t.me/fairpari_uzb",
    "en": "https://t.me/fairpari24",
    "es": "https://t.me/fairpari_arg",
    "pt": "https://t.me/fairpari_portu",
}
SUPPORT_URL = "https://t.me/fairpariadmin"

# С-13: кнопка приветственной рассылки. Ссылки для других языков не даны (В-16) — везде /en/.
WELCOME_BONUS_URL = "https://fairpari.com/en/bonus/casino/promotions/slot_first_deposit"

# ---------- профиль бота ----------
ABOUT = {  # setMyShortDescription, до 120 символов (С-07)
    "ru": "FairPari — популярные игры, спортивные события и другие развлечения от нашей надёжной букмекерской компании 🏆",
    "en": "FairPari — popular games, sports events and more from our trusted betting company 🏆",
    "es": "FairPari: juegos populares, eventos deportivos y más de nuestra casa de apuestas de confianza 🏆",
    "pt": "FairPari — jogos populares, eventos esportivos e mais da nossa casa de apostas de confiança 🏆",
    "uz": "FairPari — ishonchli bukmeker kompaniyamizdan mashhur o‘yinlar va sport tadbirlari 🏆",
}

DESCRIPTION = {  # setMyDescription, до 512 символов: видно до нажатия «Старт» (С-07)
    "ru": ("Добро пожаловать в FairPari — ваше новое любимое онлайн-казино и дом для ставок на спорт!\n\n"
           "Погружайтесь в самые популярные игры, делайте ставки на более чем 1000 захватывающих спортивных событий, "
           "крутите слоты недели и получайте бонус за бонусом! 🔥🎰⚽\n\n"
           "Пополнение счёта — проще простого: мы с радостью принимаем все основные криптовалюты. "
           "Для начала мы дарим вам огромный приветственный бонус до €1,500 и 150 бесплатных вращений! 🎁\n\n"
           "Готовы играть? Просто нажмите «Старт» ниже, и пусть веселье начнётся! 👇"),
    "en": ("Welcome to FairPari — your new favourite online casino and home of sports betting!\n\n"
           "Dive into the most popular games, bet on 1,000+ exciting sports events, spin the slot of the week "
           "and collect bonus after bonus! 🔥🎰⚽\n\n"
           "Depositing is easy: we accept all major cryptocurrencies. To get you started, we give you a huge "
           "welcome bonus of up to €1,500 and 150 free spins! 🎁\n\n"
           "Ready to play? Just tap “Start” below and let the fun begin! 👇"),
    "es": ("¡Bienvenido a FairPari, tu nuevo casino online favorito y tu casa de apuestas deportivas!\n\n"
           "Sumérgete en los juegos más populares, apuesta en más de 1000 eventos deportivos, gira la tragamonedas "
           "de la semana y consigue bono tras bono. 🔥🎰⚽\n\n"
           "Depositar es muy fácil: aceptamos las principales criptomonedas. Para empezar, te regalamos un gran "
           "bono de bienvenida de hasta €1,500 y 150 giros gratis. 🎁\n\n"
           "¿Listo para jugar? Pulsa «Iniciar» abajo y que empiece la diversión. 👇"),
    "pt": ("Bem-vindo à FairPari — o seu novo cassino online favorito e a casa das apostas esportivas!\n\n"
           "Mergulhe nos jogos mais populares, aposte em mais de 1000 eventos esportivos, gire o slot da semana "
           "e ganhe bônus atrás de bônus! 🔥🎰⚽\n\n"
           "Depositar é muito fácil: aceitamos as principais criptomoedas. Para começar, damos a você um grande "
           "bônus de boas-vindas de até €1,500 e 150 rodadas grátis! 🎁\n\n"
           "Pronto para jogar? Toque em “Começar” abaixo e que a diversão comece! 👇"),
    "uz": ("FairPari’ga xush kelibsiz — sevimli onlayn kazinongiz va sport tikishlari uyi!\n\n"
           "Eng mashhur o‘yinlarni o‘ynang, 1000 dan ortiq sport tadbirlariga tiking, haftaning slotini aylantiring "
           "va bonusdan keyin bonus oling! 🔥🎰⚽\n\n"
           "Hisobni to‘ldirish juda oson: barcha asosiy kriptovalyutalarni qabul qilamiz. Boshlash uchun sizga "
           "€1,500 gacha katta xush kelibsiz bonusi va 150 ta bepul aylantirish sovg‘a qilamiz! 🎁\n\n"
           "O‘ynashga tayyormisiz? Pastdagi «Boshlash» tugmasini bosing! 👇"),
}

# ---------- выбор языка ----------
CHOOSE_LANG = {"en": "👇 Choose a language:", "es": "👇 Elige un idioma:", "pt": "👇 Escolha um idioma:", "uz": "👇 Tilni tanlang:"}

COMMANDS = {
    "en": {"start": "Main menu", "language": "Change language"},
    "es": {"start": "Menú principal", "language": "Cambiar idioma"},
    "pt": {"start": "Menu principal", "language": "Mudar idioma"},
    "uz": {"start": "Asosiy menyu", "language": "Tilni o‘zgartirish"},
}

# ---------- главное меню (С-08, С-10) ----------
BUTTONS = {
    "en": {"register": "Register 🔥", "play": "Play ▶️", "channel": "FairPari Channel 📢", "support": "Support 🆘", "bonus": "Get bonus"},
    "es": {"register": "Registrarse 🔥", "play": "Jugar ▶️", "channel": "Canal FairPari 📢", "support": "Soporte 🆘", "bonus": "Obtener bono"},
    "pt": {"register": "Cadastrar 🔥", "play": "Jogar ▶️", "channel": "Canal FairPari 📢", "support": "Suporte 🆘", "bonus": "Pegar bônus"},
    "uz": {"register": "Ro‘yxatdan o‘tish 🔥", "play": "O‘ynash ▶️", "channel": "FairPari kanali 📢", "support": "Yordam 🆘", "bonus": "Bonusni olish"},
}

MENU = {
    "en": ("💭 Did you know you can earn money just by watching football?\n\n"
           "{name}, imagine:\n"
           "✅ Your favourite team wins — you get a payout.\n"
           "✅ A player scores — your balance grows.\n"
           "✅ You make a good prediction — you take home a big win!\n\n"
           "All of this is already happening at FairPari right now. Join the fun! 😱\n\n"
           "🎰 Play your favourite casino games!\n"
           "Want a break from sports? Welcome to our casino! We have all the most popular games you love, "
           "plus exciting new slots to spin.\n\n"
           "🔥 Start with a big welcome bonus:\n"
           "⚽ Sports: up to {sport}!\n"
           "🎰 Casino: up to {casino} + 150 free spins!\n\n"
           "Don't wait! Sign up today and start winning! 🚀"),
    "es": ("💭 ¿Sabías que puedes ganar dinero solo por ver fútbol?\n\n"
           "{name}, imagina:\n"
           "✅ Tu equipo favorito gana y recibes un pago.\n"
           "✅ Un jugador marca un gol y tu saldo crece.\n"
           "✅ Aciertas un pronóstico y te llevas una gran ganancia.\n\n"
           "Todo esto ya está pasando en FairPari ahora mismo. ¡Únete a la diversión! 😱\n\n"
           "🎰 ¡Juega a tus juegos de casino favoritos!\n"
           "¿Quieres un descanso del deporte? ¡Bienvenido a nuestro casino! Tenemos los juegos más populares "
           "que te encantan y nuevas tragamonedas emocionantes.\n\n"
           "🔥 Empieza con un gran bono de bienvenida:\n"
           "⚽ Deportes: ¡hasta {sport}!\n"
           "🎰 Casino: ¡hasta {casino} + 150 giros gratis!\n\n"
           "¡No esperes! Regístrate hoy y empieza a ganar. 🚀"),
    "pt": ("💭 Sabia que pode ganhar dinheiro só assistindo futebol?\n\n"
           "{name}, imagine:\n"
           "✅ O seu time favorito vence — você recebe um pagamento.\n"
           "✅ Um jogador marca um gol — o seu saldo cresce.\n"
           "✅ Você acerta um palpite — leva um grande prêmio!\n\n"
           "Tudo isso já está acontecendo na FairPari agora mesmo. Junte-se à diversão! 😱\n\n"
           "🎰 Jogue os seus jogos de cassino favoritos!\n"
           "Quer uma pausa do esporte? Bem-vindo ao nosso cassino! Temos os jogos mais populares que você adora "
           "e novos slots emocionantes para girar.\n\n"
           "🔥 Comece com um grande bônus de boas-vindas:\n"
           "⚽ Esportes: até {sport}!\n"
           "🎰 Cassino: até {casino} + 150 rodadas grátis!\n\n"
           "Não espere! Cadastre-se hoje e comece a ganhar! 🚀"),
    "uz": ("💭 Faqat futbol tomosha qilib pul ishlash mumkinligini bilarmidingiz?\n\n"
           "{name}, tasavvur qiling:\n"
           "✅ Sevimli jamoangiz g‘alaba qozonadi — siz to‘lov olasiz.\n"
           "✅ O‘yinchi gol uradi — balansingiz oshadi.\n"
           "✅ To‘g‘ri bashorat qilasiz — katta yutuqni olasiz!\n\n"
           "Bularning barchasi hozir FairPari’da sodir bo‘lmoqda. Bizga qo‘shiling! 😱\n\n"
           "🎰 Sevimli kazino o‘yinlaringizni o‘ynang!\n"
           "Sportdan dam olmoqchimisiz? Kazinomizga xush kelibsiz! Bizda siz yaxshi ko‘rgan eng mashhur o‘yinlar "
           "va yangi qiziqarli slotlar bor.\n\n"
           "🔥 Katta xush kelibsiz bonusi bilan boshlang:\n"
           "⚽ Sport uchun: {sport} gacha!\n"
           "🎰 Kazino uchun: {casino} gacha + 150 ta bepul aylantirish!\n\n"
           "Kechiktirmang! Bugun ro‘yxatdan o‘ting va yutishni boshlang! 🚀"),
}

# ---------- приветственный бонус через 5 минут после регистрации (С-13) ----------
WELCOME_BONUS = {
    "en": ("You're in! Welcome to FairPari — where real winners play! 🚀\n\n"
           "🔥 Tip: your first deposit gets you a welcome bonus — extra money that lets you bet more and win more! 💰\n\n"
           "So what are you waiting for? Luck won't fall into your lap by itself. Time to grab this bonus and start playing."),
    "es": ("¡Ya estás dentro! Bienvenido a FairPari, donde juegan los verdaderos ganadores. 🚀\n\n"
           "🔥 Consejo: con tu primer depósito recibes un bono de bienvenida: dinero extra para apostar más y ganar más. 💰\n\n"
           "¿A qué esperas? La suerte no cae del cielo. ¡Es hora de tomar este bono y empezar a jugar!"),
    "pt": ("Você está dentro! Bem-vindo à FairPari — aqui jogam os verdadeiros vencedores! 🚀\n\n"
           "🔥 Dica: no primeiro depósito você recebe um bônus de boas-vindas — dinheiro extra para apostar mais e ganhar mais! 💰\n\n"
           "Então, o que está esperando? A sorte não cai do céu. Hora de pegar este bônus e começar a jogar!"),
    "uz": ("Siz o‘yindasiz! FairPari’ga xush kelibsiz — bu yerda haqiqiy g‘oliblar o‘ynaydi! 🚀\n\n"
           "🔥 Maslahat: birinchi depozit uchun xush kelibsiz bonusini olasiz — bu ko‘proq tikish va ko‘proq "
           "yutish imkonini beradigan qo‘shimcha pul! 💰\n\n"
           "Nimani kutyapsiz? Omad o‘z-o‘zidan kelmaydi. Bonusni oling va o‘yinni boshlang!"),
}


def check_limits() -> None:
    """Лимиты Telegram из брифа: 120 / 512 / 1024 символа."""
    for lang, text in ABOUT.items():
        assert len(text) <= 120, f"About {lang}: {len(text)} > 120"
    for lang, text in DESCRIPTION.items():
        assert len(text) <= 512, f"Description {lang}: {len(text)} > 512"
    for lang in LANGS:
        sport, casino = BONUS[lang]
        caption = MENU[lang].format(name="X" * 32, sport=sport, casino=casino)
        assert len(caption) <= 1024, f"Menu {lang}: {len(caption)} > 1024"
        assert len(WELCOME_BONUS[lang]) <= 1024, f"Bonus {lang} > 1024"
