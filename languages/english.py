"""
English language file for Telegram Referral Bot
This is the default language
"""

LANGUAGE_NAME = "English"
LANGUAGE_CODE = "en"

# Command descriptions
CMD_START = "Start the bot and get your invite link"
CMD_HELP = "Show help message"
CMD_STATS = "View your referral statistics"
CMD_LEADERBOARD = "View top referrers"
CMD_LANGUAGE = "Change language"
CMD_ADMIN_STATS = "View bot statistics (admin only)"
CMD_ADMIN_TOP_USERS = "View top users for giveaway (admin only)"
CMD_BROADCAST = "Send message to all users (admin only)"

# Button texts
BTN_MY_STATS = "📊 My Stats"
BTN_COPY_LINK = "🔗 Copy Link"
BTN_SHARE_LINK = "📤 Share Link"
BTN_LEADERBOARD = "🏆 Leaderboard"
BTN_LANGUAGE = "🌐 Change Language"
BTN_BACK = "◀️ Back"
BTN_CLICK_TO_COPY = "📋 Click to Copy Link"
BTN_SHARE_NOW = "📤 Share Now"
BTN_SHARE_TELEGRAM = "📱 Share via Telegram"
BTN_SHARE_WHATSAPP = "📱 Share via WhatsApp"
BTN_SHARE_TWITTER = "🐦 Share via Twitter"
BTN_COPY_SHARE_MSG = "📋 Copy Share Message"

# Welcome messages
WELCOME_NEW = """Welcome to the Referral Bot, {first_name}! 🎉

Your unique invite link: {invite_link}

📢 Share this link to invite others to our channel!
🏆 The more people you refer, the higher you'll rank!

Use the buttons below to check your stats and leaderboard."""

WELCOME_RETURNING = """Welcome back, {first_name}! 🎉

Your referrals: {referral_count}
Your invite link: {invite_link}

Share your link to get more referrals!"""

# Success messages
REFERRAL_SUCCESS = """🎉 Great! {first_name} joined using your referral link!
Your total referrals: {referral_count}"""

# Help message
HELP_MESSAGE = """🤖 Referral Bot Help

📋 Available Commands:
/start - Start the bot and get your invite link
/help - Show this help message
/stats - View your referral statistics
/leaderboard - View top referrers
/language - Change language

🎯 How it works:
1. Use /start to get your unique invite link
2. Share your link with friends
3. When someone joins the channel using your link, you get a referral point
4. Check the leaderboard to see your ranking

🏆 The users with the most referrals will be eligible for giveaways!

💡 Tip: Share your link on social media, groups, or with friends to get more referrals!"""

# Admin help addition
ADMIN_HELP_ADDITION = """\n\n👑 Admin Commands:
/adminstats - View bot statistics
/topusers [number] - View top users for giveaway
/broadcast <message> - Send message to all users"""

# Error messages
ERROR_NOT_ADMIN = "❌ You're not authorized to use this command."
ERROR_INVITE_LINK_FAILED = "❌ Sorry, I couldn't create your invite link. Please make sure I'm an admin in the channel."
ERROR_USER_NOT_FOUND = "❌ User data not found. Please use /start first."
ERROR_NO_REFERRALS = "📊 No referrals yet. Be the first to start referring!"
ERROR_NO_USERS = "📊 No users found."

# Stats messages
STATS_HEADER = "📊 Your Statistics"
STATS_NAME = "👤 Name: {first_name}"
STATS_USERNAME = "🆔 Username: @{username}"
STATS_REFERRALS = "🎯 Referrals: {referral_count}"
STATS_RANK = "🏆 Rank: #{rank}"
STATS_JOINED = "📅 Joined: {join_date}"
STATS_FOOTER = "Keep sharing your link to climb the leaderboard! 🚀"

# Invite link messages
INVITE_LINK_HEADER = "🔗 Your Unique Invite Link"
INVITE_LINK_SHARE = "📢 Share this link with your friends!"
INVITE_LINK_TIP = "💡 Tip: Share on social media, groups, or with friends to maximize your referrals!"

# Leaderboard messages
LEADERBOARD_HEADER = "🏆 Top Referrers Leaderboard"
LEADERBOARD_FOOTER = "🎯 Keep referring to climb higher!"

# Language selection
LANGUAGE_SELECTION = "🌐 Please select your language:"
LANGUAGE_CHANGED = "✅ Language changed to English!"

# Additional messages
COPIED_TO_CLIPBOARD = "✅ Your invite link has been copied to clipboard!"
SHARE_LINK_MESSAGE = "📱 Share your invite link directly from Telegram!"

# New copy and share functionality
LINK_COPIED_ALERT = "Link copied to clipboard!"
YOUR_INVITE_LINK = "Your Invite Link"
LINK_COPIED = "Link copied to clipboard!"
SHARE_LINK_PROMPT = "Share this link with your friends!"
REFERRAL_EXPLANATION = "Every person who joins through your link counts as a referral!"
LINK_NO_LIMITS = "This link has NO LIMITS - unlimited members and never expires!"
SHARING_TIP = "Tip: Share on social media, groups, or with friends to maximize your referrals!"

# Share options
SHARE_INVITE_LINK = "Share Your Invite Link"
CHOOSE_SHARE_METHOD = "Choose how you want to share your referral link"
YOUR_LINK = "Your link"
SHARE_MORE_REFERRALS = "The more you share, the more referrals you get!"
JOIN_CHANNEL_PROMPT = "Join our amazing channel through my referral link!"
EXCLUSIVE_CONTENT = "Get exclusive content and updates"
GROWING_COMMUNITY = "Be part of our growing community"
CLICK_TO_JOIN = "Click here to join"
SHARED_BY = "Shared by" 