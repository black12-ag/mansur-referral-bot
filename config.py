import os

# Telegram Referral Bot Configuration
# Copy this file and rename it to config.py, then fill in your actual values

# =============================================================================
# REQUIRED CONFIGURATION - YOU MUST CHANGE THESE VALUES
# =============================================================================

# Your bot token from @BotFather
# Example: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
# Use environment variable for security or fallback to the provided value
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Your channel username (with @) or channel ID
# Examples: "@mychannel" or "-1001234567890"
CHANNEL_ID = os.environ.get("TELEGRAM_CHANNEL_ID", "@Kabir_Forex")

# Your Telegram user ID (get it from @userinfobot)
# Example: 123456789
ADMIN_USER_ID = int(os.environ.get("TELEGRAM_ADMIN_USER_ID", "5406887259"))

# =============================================================================
# OPTIONAL CONFIGURATION - YOU CAN MODIFY THESE IF NEEDED
# =============================================================================

# Database file name
DATABASE_NAME = "referral_bot.db"

# Maximum number of users to show in /topusers command
MAX_TOP_USERS = 50

# Default number of users to show in leaderboard
DEFAULT_LEADERBOARD_SIZE = 10

# Welcome message customization
WELCOME_MESSAGE_NEW = """Welcome to the Referral Bot, {first_name}! 🎉

Your unique invite link: {invite_link}

📢 Share this link to invite others to our channel!
🏆 The more people you refer, the higher you'll rank!

Use the buttons below to check your stats and leaderboard."""

WELCOME_MESSAGE_RETURNING = """Welcome back, {first_name}! 🎉

Your referrals: {referral_count}
Your invite link: {invite_link}

Share your link to get more referrals!"""

# Success message when someone gets referred
REFERRAL_SUCCESS_MESSAGE = "🎉 Great! {first_name} joined using your referral link!\nYour total referrals: {referral_count}"

# Help message
HELP_MESSAGE = """🤖 Referral Bot Help

📋 Available Commands:
/start - Start the bot and get your invite link
/help - Show this help message

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
/topusers [number] - View top users for giveaway"""

# Error messages
ERROR_MESSAGES = {
    "not_admin": "❌ You're not authorized to use this command.",
    "invite_link_failed": "❌ Sorry, I couldn't create your invite link. Please make sure I'm an admin in the channel.",
    "user_not_found": "❌ User data not found. Please use /start first.",
    "no_referrals": "📊 No referrals yet. Be the first to start referring!",
    "no_users": "📊 No users found."
}

# =============================================================================
# ADVANCED CONFIGURATION - ONLY MODIFY IF YOU KNOW WHAT YOU'RE DOING
# =============================================================================

# Logging configuration
LOG_LEVEL = "DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Database connection settings
DB_CHECK_SAME_THREAD = False
DB_TIMEOUT = 30

# Telegram API settings
TELEGRAM_READ_TIMEOUT = 30
TELEGRAM_WRITE_TIMEOUT = 30
TELEGRAM_CONNECT_TIMEOUT = 30

# Rate limiting (messages per second)
RATE_LIMIT = 30

# Maximum message length before splitting
MAX_MESSAGE_LENGTH = 4000

# Invite link settings
INVITE_LINK_MEMBER_LIMIT = None  # No limit
INVITE_LINK_NAME_TEMPLATE = "Referral by {display_name}"