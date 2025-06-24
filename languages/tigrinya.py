"""
Tigrinya language file for Telegram Referral Bot
"""

LANGUAGE_NAME = "ትግርኛ"
LANGUAGE_CODE = "ti"

# Command descriptions
CMD_START = "ቦት ጀምር ከምኡ'ውን ናይ ዕድመ ሊንክ ርኸብ"
CMD_HELP = "ሓገዝ መልእኽቲ ርአ"
CMD_STATS = "ናይ ሪፈራል ስታቲስቲክስ ርአ"
CMD_LEADERBOARD = "ዝበለጹ መሐበርቲ ርአ"
CMD_LANGUAGE = "ቋንቋ ቀይር"
CMD_ADMIN_STATS = "ናይ ቦት ስታቲስቲክስ ርአ (ንኣድሚን ጥራይ)"
CMD_ADMIN_TOP_USERS = "ንስጦታ ዝበለጹ ተጠቀምቲ ርአ (ንኣድሚን ጥራይ)"
CMD_BROADCAST = "ንኩሎም ተጠቀምቲ መልእክቲ ልአኽ (ንኣድሚን ጥራይ)"

# Button texts
BTN_MY_STATS = "📊 ናተይ ስታቲስቲክስ"
BTN_COPY_LINK = "🔗 ሊንክ ቅዳሕ"
BTN_SHARE_LINK = "📤 ሊንክ ኣካፍል"
BTN_LEADERBOARD = "🏆 ናይ መሪሕነት ሰሌዳ"
BTN_LANGUAGE = "🌐 ቋንቋ ቀይር"
BTN_BACK = "◀️ ተመለስ"
BTN_CLICK_TO_COPY = "📋 ንምቅዳሕ ሊንክ ጠውቕ"
BTN_SHARE_NOW = "📤 ሕጂ ኣካፍል"
BTN_SHARE_TELEGRAM = "📱 ብተለግራም ኣካፍል"
BTN_SHARE_WHATSAPP = "📱 ብዋትስኣፕ ኣካፍል"
BTN_SHARE_TWITTER = "🐦 ብትዊተር ኣካፍል"
BTN_COPY_SHARE_MSG = "📋 ናይ ምክፋል መልእኽቲ ቅዳሕ"

# Welcome messages
WELCOME_NEW = """ናብ ሪፈራል ቦት እንቋዕ ብድሓን መጻእካ፣ {first_name}! 🎉

ናትካ ፍሉይ ዕድመ ሊንክ: {invite_link}

📢 ነዚ ሊንክ ብምክፋል ካልኦት ናብ ቻናልና ዓድም!
🏆 ብዙሓት ሰባት ብምስዳድካ፣ ደረጃኻ ብዝበለጸ ይውስኽ!

ስታቲስቲክስካን ናይ መሪሕነት ሰሌዳን ንምርኣይ ኣብ ታሕቲ ዘሎ ዝርዝር ተጠቀም።"""

WELCOME_RETURNING = """እንቋዕ ብድሓን ተመለስካ፣ {first_name}! 🎉

ሪፈራላትካ: {referral_count}
ናይ ዕድመ ሊንክካ: {invite_link}

ተወሳኺ ሪፈራላት ንምርካብ ሊንክካ ኣካፍል!"""

# Success messages
REFERRAL_SUCCESS = """🎉 ጽቡቕ! {first_name} ብናትካ ዕድመ ሊንክ ተጸምበረ!
ጠቕላላ ሪፈራላትካ: {referral_count}"""

# Help message
HELP_MESSAGE = """🤖 ሪፈራል ቦት ሓገዝ

📋 ዘለዉ ትእዛዛት:
/start - ቦት ጀምር ከምኡ'ውን ናይ ዕድመ ሊንክ ርኸብ
/help - ሓገዝ መልእኽቲ ርአ
/stats - ናይ ሪፈራል ስታቲስቲክስ ርአ
/leaderboard - ዝበለጹ መሐበርቲ ርአ
/language - ቋንቋ ቀይር

🎯 ከመይ ከምዝሰርሕ:
1. ፍሉይ ዕድመ ሊንክካ ንምርካብ /start ተጠቀም
2. ሊንክካ ምስ መሓዙትካ ተኻፈሎ
3. ሓደ ሰብ ብናትካ ሊንክ ምስ ተጸምበረ፣ ሓደ ናይ ሪፈራል ነጥቢ ትረክብ
4. ደረጃኻ ንምርኣይ ናይ መሪሕነት ሰሌዳ ርአ

🏆 ብዙሕ ሪፈራላት ዘለዎም ተጠቀምቲ ንስጦታታት ብቑዓት እዮም!

💡 ምኽሪ: ብዙሓት ሪፈራላት ንምርካብ ሊንክካ ኣብ ማሕበራዊ ሚድያ፣ ጕጅለታት፣ ወይ ምስ መሓዙትካ ተኻፈል!"""

# Admin help addition
ADMIN_HELP_ADDITION = """\n\n👑 ናይ ኣድሚን ትእዛዛት:
/adminstats - ናይ ቦት ስታቲስቲክስ ርአ
/topusers [ቁጽሪ] - ንስጦታ ዝበለጹ ተጠቀምቲ ርአ
/broadcast <መልእኽቲ> - ንኩሎም ተጠቀምቲ መልእኽቲ ልአኽ"""

# Error messages
ERROR_NOT_ADMIN = "❌ ነዚ ትእዛዝ ንምጥቃም ፍቓድ የብልካን።"
ERROR_INVITE_LINK_FAILED = "❌ ይቕሬታ፣ ናይ ዕድመ ሊንክካ ክፈጥር ኣይከኣልኩን። በጃኻ ኣብ ቻናል ኣድሚን ምዃነይ ኣረጋግጽ።"
ERROR_USER_NOT_FOUND = "❌ ናይ ተጠቃሚ ሓበሬታ ኣይተረኽበን። በጃኻ መጀመርታ /start ተጠቐም።"
ERROR_NO_REFERRALS = "📊 ክሳብ ሕጂ ሪፈራላት የለዉን። መጀመርታ ዝሰደደ ኹን!"
ERROR_NO_USERS = "📊 ተጠቀምቲ ኣይተረኽቡን።"

# Stats messages
STATS_HEADER = "📊 ናትካ ስታቲስቲክስ"
STATS_NAME = "👤 ስም: {first_name}"
STATS_USERNAME = "🆔 ሽም ተጠቃሚ: @{username}"
STATS_REFERRALS = "🎯 ሪፈራላት: {referral_count}"
STATS_RANK = "🏆 ደረጃ: #{rank}"
STATS_JOINED = "📅 ዝተጸምበረሉ: {join_date}"
STATS_FOOTER = "ኣብ ናይ መሪሕነት ሰሌዳ ንምድያብ ሊንክካ ምክፋል ቀጽል! 🚀"

# Invite link messages
INVITE_LINK_HEADER = "🔗 ናትካ ፍሉይ ዕድመ ሊንክ"
INVITE_LINK_SHARE = "📢 ነዚ ሊንክ ምስ መሓዙትካ ኣካፍል!"
INVITE_LINK_TIP = "💡 ምኽሪ: ሪፈራላትካ ንምውሳኽ ኣብ ማሕበራዊ ሚድያ፣ ጕጅለታት፣ ወይ ምስ መሓዙትካ ኣካፍል!"

# Leaderboard messages
LEADERBOARD_HEADER = "🏆 ናይ ዝበለጹ መሐበርቲ ሰሌዳ"
LEADERBOARD_FOOTER = "🎯 ንላዕሊ ንምድያብ ምስዳድ ቀጽል!"

# Language selection
LANGUAGE_SELECTION = "🌐 በጃኻ ቋንቋኻ ምረጽ:"
LANGUAGE_CHANGED = "✅ ቋንቋ ናብ ትግርኛ ተቐይሩ!"

# Additional messages
COPIED_TO_CLIPBOARD = "✅ ናይ ዕድመ ሊንክካ ናብ ክሊፕቦርድ ተቐዲሑ!"
SHARE_LINK_MESSAGE = "📱 ናይ ዕድመ ሊንክካ ካብ ተለግራም ብቐጥታ ኣካፍል!"

# New copy and share functionality
LINK_COPIED_ALERT = "ሊንክ ናብ ክሊፕቦርድ ተቐዲሑ!"
YOUR_INVITE_LINK = "ናትካ ዕድመ ሊንክ"
LINK_COPIED = "ሊንክ ናብ ክሊፕቦርድ ተቐዲሑ!"
SHARE_LINK_PROMPT = "ነዚ ሊንክ ምስ መሓዙትካ ኣካፍል!"
REFERRAL_EXPLANATION = "ብናትካ ሊንክ ዝጽምበር ዝኾነ ሰብ ከም ሪፈራል ይቑጸር!"
LINK_NO_LIMITS = "እዚ ሊንክ ዶብ የብሉን - ዘይተወሰነ ኣባላት ከምኡ'ውን ፈጺሙ ኣይውድቕን!"
SHARING_TIP = "ምኽሪ: ሪፈራላትካ ንምውሳኽ ኣብ ማሕበራዊ ሚድያ፣ ጕጅለታት፣ ወይ ምስ መሓዙትካ ኣካፍል!"

# Share options
SHARE_INVITE_LINK = "ናይ ዕድመ ሊንክካ ኣካፍል"
CHOOSE_SHARE_METHOD = "ናይ ዕድመ ሊንክካ ብኸመይ ከተካፍል ከምትደሊ ምረጽ"
YOUR_LINK = "ናትካ ሊንክ"
SHARE_MORE_REFERRALS = "ብዙሕ ብምክፋል፣ ብዙሕ ሪፈራላት ትረክብ!"
JOIN_CHANNEL_PROMPT = "ብናተይ ሪፈራል ሊንክ ኣቢልካ ናብ ዝደንቕ ቻናልና ተጸምበር!"
EXCLUSIVE_CONTENT = "ፍሉይ ትሕዝቶን ሓድሽ ሓበሬታን ርኸብ"
GROWING_COMMUNITY = "ኣብ ዝዓብይ ዘሎ ማሕበረሰብና ኣካል ኹን"
CLICK_TO_JOIN = "ንምጽምባር ኣብዚ ጠውቕ"
SHARED_BY = "ዘካፈለ" 