"""
Oromo language file for Telegram Referral Bot
"""

LANGUAGE_NAME = "Afaan Oromoo"
LANGUAGE_CODE = "om"

# Command descriptions
CMD_START = "Booticha jalqabi fi linki affeerraa kee argadhu"
CMD_HELP = "Ergaa gargaarsaa agarsiisi"
CMD_STATS = "Istaatistiiksii ergisiisaa kee ilaali"
CMD_LEADERBOARD = "Warra ergisiistota ol'aanaa ilaali"
CMD_LANGUAGE = "Afaan jijjiiri"
CMD_ADMIN_STATS = "Istaatistiiksii bootichaa ilaalaa (admin qofaaf)"
CMD_ADMIN_TOP_USERS = "Fayyadamtoota ol'aanoo kenniinsa shallaguu ilaalaa (admin qofaaf)"
CMD_BROADCAST = "Fayyadamtoota hundaaf ergaa ergi (admin qofaaf)"

# Button texts
BTN_MY_STATS = "📊 Istaatistiiksii Koo"
BTN_COPY_LINK = "🔗 Linki Garagalchi"
BTN_SHARE_LINK = "📤 Linki Qoodi"
BTN_LEADERBOARD = "🏆 Gabatee Durattootaa"
BTN_LANGUAGE = "🌐 Afaan Jijjiiri"
BTN_BACK = "◀️ Duubatti Deebi'i"
BTN_CLICK_TO_COPY = "📋 Garagalchuuf Linki Tuqi"
BTN_SHARE_NOW = "📤 Amma Qoodi"
BTN_SHARE_TELEGRAM = "📱 Telegram'n Qoodi"
BTN_SHARE_WHATSAPP = "📱 WhatsApp'n Qoodi"
BTN_SHARE_TWITTER = "🐦 Twitter'n Qoodi"
BTN_COPY_SHARE_MSG = "📋 Ergaa Qoodiinsaa Garagalchi"

# Welcome messages
WELCOME_NEW = """Baga Nagaan Booticha Ergisiisaatti Dhuftan, {first_name}! 🎉

Linki affeerraa kee addaa: {invite_link}

📢 Linki kana qooduun namoota kaanal keenyatti affeeraa!
🏆 Namoonni baay'een kan ergisiiftuu taatan, sadarkaan keessan ol ka'a!

Istaatistiiksii kee ilaaluuf fi gabatee durattootaa ilaaluuf batanii gadii fayyadami."""

WELCOME_RETURNING = """Baga Deebitan, {first_name}! 🎉

Ergisiiftuun kee: {referral_count}
Linki affeerraa kee: {invite_link}

Ergisiiftuu dabalataaf linki kee qoodi!"""

# Success messages
REFERRAL_SUCCESS = """🎉 Galatoomaa! {first_name} linki kee fayyadamuun makameera!
Waliigala ergisiiftuu kee: {referral_count}"""

# Help message
HELP_MESSAGE = """🤖 Gargaarsa Bootichaa Ergisiisaa

📋 Ajajawwan Jiran:
/start - Booticha jalqabi fi linki affeerraa kee argadhu
/help - Ergaa gargaarsaa agarsiisi
/stats - Istaatistiiksii ergisiisaa kee ilaali
/leaderboard - Warra ergisiistota ol'aanaa ilaali
/language - Afaan jijjiiri

🎯 Akkataan inni hojjetu:
1. Linki affeerraa kee addaa argachuuf /start fayyadami
2. Linki kee hiriyoota keetiif qoodi
3. Yeroo namni tokko linki keetiin kaanal makamu, qabxii ergisiisuu tokko argattu
4. Sadarkaa kee ilaaluuf gabatee durattootaa ilaali

🏆 Fayyadamtoonni ergisiisuu baay'ee qaban kenniinsa shallaguu argatu!

💡 Gorsa: Ergisiisawwan baay'ee argachuuf linki kee miidiyaa hawaasaa, gareelee, ykn hiriyoota kee waliin qoodi!"""

# Admin help addition
ADMIN_HELP_ADDITION = """\n\n👑 Ajajawwan Admin:
/adminstats - Istaatistiiksii bootichaa ilaali
/topusers [lakkoofsa] - Fayyadamtoota ol'aanoo kenniinsa shallaguu ilaali
/broadcast <ergaa> - Fayyadamtoota hundaaf ergaa ergi"""

# Error messages
ERROR_NOT_ADMIN = "❌ Ajaja kana fayyadamuuf mirga hin qabdu."
ERROR_INVITE_LINK_FAILED = "❌ Dhiifama, linki affeerraa kee uumuu hin dandeenye. Maaloo kaanalicha keessatti admin ta'uu koo mirkaneeffadhu."
ERROR_USER_NOT_FOUND = "❌ Daataan fayyadamaa hin argamne. Maaloo jalqaba /start fayyadami."
ERROR_NO_REFERRALS = "📊 Hanga ammaatti ergisiisni hin jiru. Kan jalqaba ta'i!"
ERROR_NO_USERS = "📊 Fayyadamtoonni hin argamne."

# Stats messages
STATS_HEADER = "📊 Istaatistiiksii Kee"
STATS_NAME = "👤 Maqaa: {first_name}"
STATS_USERNAME = "🆔 Maqaa fayyadamaa: @{username}"
STATS_REFERRALS = "🎯 Ergisiisawwan: {referral_count}"
STATS_RANK = "🏆 Sadarkaa: #{rank}"
STATS_JOINED = "📅 Kan makame: {join_date}"
STATS_FOOTER = "Gabatee durattootaa irratti ol bahuuf linki kee qooduu itti fufi! 🚀"

# Invite link messages
INVITE_LINK_HEADER = "🔗 Linki Affeerraa Kee Addaa"
INVITE_LINK_SHARE = "📢 Linki kana hiriyoota keetiif qoodi!"
INVITE_LINK_TIP = "💡 Gorsa: Ergisiisawwan kee dabaluuf miidiyaa hawaasaa, gareelee, ykn hiriyoota kee waliin qoodi!"

# Leaderboard messages
LEADERBOARD_HEADER = "🏆 Gabatee Ergisiistota Ol'aanaa"
LEADERBOARD_FOOTER = "🎯 Ol ka'uuf ergisiisuu itti fufi!"

# Language selection
LANGUAGE_SELECTION = "🌐 Maaloo afaan kee filadhu:"
LANGUAGE_CHANGED = "✅ Afaan gara Afaan Oromootti jijjiirameera!"

# Additional messages
COPIED_TO_CLIPBOARD = "✅ Linki affeerraa kee gara clipboard garagalfameera!"
SHARE_LINK_MESSAGE = "📱 Linki affeerraa kee Telegram irraa kallattiin qoodi!"

# New copy and share functionality
LINK_COPIED_ALERT = "Linki gara clipboard garagalfameera!"
YOUR_INVITE_LINK = "Linki Affeerraa Kee"
LINK_COPIED = "Linki gara clipboard garagalfameera!"
SHARE_LINK_PROMPT = "Linki kana hiriyoota keetiif qoodi!"
REFERRAL_EXPLANATION = "Namni kamiyyuu linki keetiin seenu akka ergisiisaatti lakkaa'ama!"
LINK_NO_LIMITS = "Linki kun daangaa hin qabu - miseensota daangaa hin qabne fi gonkumaa hin dhumatu!"
SHARING_TIP = "Gorsa: Ergisiisawwan kee dabaluuf miidiyaa hawaasaa, gareelee, ykn hiriyoota kee waliin qoodi!"

# Share options
SHARE_INVITE_LINK = "Linki Affeerraa Kee Qoodi"
CHOOSE_SHARE_METHOD = "Linki affeerraa kee akkamitti qooduuf akka barbaaddu filadhu"
YOUR_LINK = "Linki kee"
SHARE_MORE_REFERRALS = "Baay'ee yoo qooddu, ergisiisawwan baay'ee argattu!"
JOIN_CHANNEL_PROMPT = "Linki ergisiisaa koo fayyadamuun kaanal keenya bareeda seeni!"
EXCLUSIVE_CONTENT = "Qabiyyee addaa fi haaromsa argadhu"
GROWING_COMMUNITY = "Hawaasa keenya guddachaa jiru keessatti hirmaadhu"
CLICK_TO_JOIN = "Makachuuf asitti tuqi"
SHARED_BY = "Kan qoode" 