"""
Amharic language file for Telegram Referral Bot
"""

LANGUAGE_NAME = "አማርኛ"
LANGUAGE_CODE = "am"

# Command descriptions
CMD_START = "ቦቱን ያስጀምሩ እና የግል ማስተላለፊያ ሊንክዎን ያግኙ"
CMD_HELP = "የእገዛ መልዕክት አሳይ"
CMD_STATS = "የእርስዎን የማስተላለፍ ስታቲስቲክስ ይመልከቱ"
CMD_LEADERBOARD = "ከፍተኛ አማላፊዎችን ይመልከቱ"
CMD_LANGUAGE = "ቋንቋ ይቀይሩ"
CMD_ADMIN_STATS = "የቦት ስታቲስቲክስ ይመልከቱ (ለአስተዳዳሪ ብቻ)"
CMD_ADMIN_TOP_USERS = "ለስጦታ ከፍተኛ ተጠቃሚዎችን ይመልከቱ (ለአስተዳዳሪ ብቻ)"
CMD_BROADCAST = "ለሁሉም ተጠቃሚዎች መልዕክት ላክ (ለአስተዳዳሪ ብቻ)"

# Button texts
BTN_MY_STATS = "📊 የእኔ ስታቲስቲክስ"
BTN_COPY_LINK = "🔗 ሊንክ ቅዳ"
BTN_SHARE_LINK = "📤 ሊንክ አጋራ"
BTN_LEADERBOARD = "🏆 የአሸናፊዎች ሰንጠረዥ"
BTN_LANGUAGE = "🌐 ቋንቋ ቀይር"
BTN_BACK = "◀️ ተመለስ"

# Welcome messages
WELCOME_NEW = """ለማስተላለፊያ ቦት እንኳን ደህና መጡ፣ {first_name}! 🎉

የእርስዎ ልዩ ማስተላለፊያ ሊንክ: {invite_link}

📢 ይህንን ሊንክ ለጓደኞችዎ ያጋሩ እና ወደ ቻናላችን ይጋብዙ!
🏆 ብዙ ሰዎችን በማስተላለፍ ደረጃዎን ከፍ ያድርጉ!

ስታቲስቲክስዎን እና የአሸናፊዎች ሰንጠረዥን ለመመልከት ከታች ያሉትን አዝራሮች ይጠቀሙ።"""

WELCOME_RETURNING = """እንኳን ደህና መጡ፣ {first_name}! 🎉

የእርስዎ ማስተላለፊያዎች: {referral_count}
የእርስዎ ማስተላለፊያ ሊንክ: {invite_link}

ተጨማሪ ማስተላለፊያዎችን ለማግኘት ሊንክዎን ያጋሩ!"""

# Success messages
REFERRAL_SUCCESS = """🎉 አዎ! {first_name} በእርስዎ ማስተላለፊያ ሊንክ አማካኝነት ተቀላቅሏል!
የእርስዎ ጠቅላላ ማስተላለፊያዎች: {referral_count}"""

# Help message
HELP_MESSAGE = """🤖 የማስተላለፊያ ቦት እገዛ

📋 የሚገኙ ትዕዛዞች:
/start - ቦቱን ያስጀምሩ እና የግል ማስተላለፊያ ሊንክዎን ያግኙ
/help - የእገዛ መልዕክት አሳይ
/stats - የእርስዎን የማስተላለፍ ስታቲስቲክስ ይመልከቱ
/leaderboard - ከፍተኛ አማላፊዎችን ይመልከቱ
/language - ቋንቋ ይቀይሩ

🎯 እንዴት እንደሚሰራ:
1. የእርስዎን ልዩ ማስተላለፊያ ሊንክ ለማግኘት /start ይጠቀሙ
2. ሊንክዎን ለጓደኞችዎ ያጋሩ
3. አንድ ሰው በእርስዎ ሊንክ አማካኝነት ቻናሉን ሲቀላቀል፣ አንድ የማስተላለፊያ ነጥብ ያገኛሉ
4. ደረጃዎን ለማወቅ የአሸናፊዎች ሰንጠረዥን ይመልከቱ

🏆 ከፍተኛ ማስተላለፊያዎች ያላቸው ተጠቃሚዎች ለስጦታዎች ብቁ ይሆናሉ!

💡 ምክር: ብዙ ማስተላለፊያዎችን ለማግኘት ሊንክዎን በማህበራዊ ሚዲያ፣ በቡድኖች ወይም ከጓደኞችዎ ጋር ያጋሩ!"""

# Admin help addition
ADMIN_HELP_ADDITION = """\n\n👑 የአስተዳዳሪ ትዕዛዞች:
/adminstats - የቦት ስታቲስቲክስ ይመልከቱ
/topusers [number] - ለስጦታ ከፍተኛ ተጠቃሚዎችን ይመልከቱ
/broadcast <message> - ለሁሉም ተጠቃሚዎች መልዕክት ላክ"""

# Error messages
ERROR_NOT_ADMIN = "❌ ይህን ትዕዛዝ ለመጠቀም ፈቃድ የለዎትም።"
ERROR_INVITE_LINK_FAILED = "❌ ይቅርታ፣ የማስተላለፊያ ሊንክዎን መፍጠር አልቻልኩም። እባክዎ በቻናሉ ውስጥ አስተዳዳሪ መሆኔን ያረጋግጡ።"
ERROR_USER_NOT_FOUND = "❌ የተጠቃሚ ዳታ አልተገኘም። እባክዎ መጀመሪያ /start ይጠቀሙ።"
ERROR_NO_REFERRALS = "📊 እስካሁን ምንም ማስተላለፊያዎች የሉም። መጀመሪያ የሚያስተላልፍ ይሁኑ!"
ERROR_NO_USERS = "📊 ምንም ተጠቃሚዎች አልተገኙም።"

# Stats messages
STATS_HEADER = "📊 የእርስዎ ስታቲስቲክስ"
STATS_NAME = "👤 ስም: {first_name}"
STATS_USERNAME = "🆔 የተጠቃሚ ስም: @{username}"
STATS_REFERRALS = "🎯 ማስተላለፊያዎች: {referral_count}"
STATS_RANK = "🏆 ደረጃ: #{rank}"
STATS_JOINED = "📅 የተቀላቀሉበት: {join_date}"
STATS_FOOTER = "የአሸናፊዎች ሰንጠረዡን ለመውጣት ሊንክዎን ማጋራትዎን ይቀጥሉ! 🚀"

# Invite link messages
INVITE_LINK_HEADER = "🔗 የእርስዎ ልዩ ማስተላለፊያ ሊንክ"
INVITE_LINK_SHARE = "📢 ይህንን ሊንክ ከጓደኞችዎ ጋር ያጋሩ!"
INVITE_LINK_TIP = "💡 ምክር: ማስተላለፊያዎችዎን ለመጨመር በማህበራዊ ሚዲያ፣ በቡድኖች ወይም ከጓደኞችዎ ጋር ያጋሩ!"

# Leaderboard messages
LEADERBOARD_HEADER = "🏆 የከፍተኛ አማላፊዎች ሰንጠረዥ"
LEADERBOARD_FOOTER = "🎯 ከፍ ለማለት ማስተላለፍ ይቀጥሉ!"

# Language selection
LANGUAGE_SELECTION = "🌐 እባክዎ ቋንቋዎን ይምረጡ:"
LANGUAGE_CHANGED = "✅ ቋንቋ ወደ አማርኛ ተቀይሯል!"

# Additional messages
COPIED_TO_CLIPBOARD = "✅ የእርስዎ ማስተላለፊያ ሊንክ ወደ ክሊፕቦርድ ተቀድቷል!"
SHARE_LINK_MESSAGE = "📱 ማስተላለፊያ ሊንክዎን ከቴሌግራም በቀጥታ ያጋሩ!"
