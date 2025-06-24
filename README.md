# Telegram Referral Bot

A powerful Telegram bot that creates unique invite links for users to track referrals and run giveaways. Perfect for growing your Telegram channel with gamified referral system.

## Features

🎯 **Unique Invite Links**: Each user gets a personalized channel invite link
📊 **Referral Tracking**: Automatically counts referrals for each user
🏆 **Leaderboard**: Shows top referrers in real-time
📈 **Admin Dashboard**: View statistics and top users for giveaways
🎁 **Giveaway Ready**: Easy selection of top referrers for prizes
💾 **Persistent Data**: SQLite database stores all user data

## Setup Instructions

### 1. Prerequisites

- Python 3.7 or higher
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)
- Admin access to your Telegram channel

### 2. Installation

1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration

There are two ways to configure the bot:

#### Option A: Using Setup Script (Recommended)
```bash
python setup.py
```
This interactive script will:
1. Check your Python version
2. Install required packages
3. Guide you through configuration
4. Create a sample .env file

#### Option B: Manual Configuration

1. Create a `.env` file with the following variables:
   ```
   TELEGRAM_BOT_TOKEN="your_bot_token_here"
   TELEGRAM_CHANNEL_ID="@your_channel"
   TELEGRAM_ADMIN_USER_ID="your_user_id"
   ```

2. Alternatively, set these as environment variables:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_bot_token_here"
   export TELEGRAM_CHANNEL_ID="@your_channel" 
   export TELEGRAM_ADMIN_USER_ID="your_user_id"
```

#### How to get your Telegram User ID:
1. Message [@userinfobot](https://t.me/userinfobot)
2. It will reply with your user ID

#### How to get your Channel ID:
- If your channel has a username: use `@username`
- If no username: forward a message from your channel to [@userinfobot](https://t.me/userinfobot)

### 4. Bot Setup

1. **Add bot to your channel**:
   - Go to your channel
   - Add the bot as an administrator
   - Give it permission to "Invite users via link"

2. **Start the bot**:
   ```bash
   python start_bot.py
   ```

## How It Works

### For Users:
1. User starts the bot with `/start`
2. Bot creates a unique invite link for the channel
3. User shares their link with friends
4. When someone joins via their link, they get a referral point
5. Users can check stats and leaderboard anytime

### For Admins:
- View bot statistics with `/adminstats`
- Get top users list for giveaways with `/topusers`
- Monitor referral activity in real-time
- Send broadcast messages to all users with `/broadcast`

## Bot Commands

### User Commands:
- `/start` - Get your unique invite link and start referring
- `/help` - Show help and instructions

### Admin Commands:
- `/adminstats` - View total users, referrals, and top referrer
- `/topusers [number]` - Get detailed list of top referrers (default: 20, max: 50)
- `/broadcast <message>` - Send a message to all bot users

### Interactive Buttons:
- 📊 **My Stats** - View your referral count and rank
- 🔗 **Copy Link** - Copy your unique invite link
- 📤 **Share Link** - Directly share your link
- 🏆 **Leaderboard** - See top 10 referrers

## Database Structure

The bot uses SQLite database with the following tables:

### Users Table:
- `user_id` - Telegram user ID (Primary Key)
- `username` - Telegram username
- `first_name` - User's first name
- `invite_link` - Unique channel invite link
- `referral_count` - Number of successful referrals
- `referred_by` - ID of user who referred them
- `join_date` - When user started the bot
- `is_active` - Whether user is active

### Referrals Table:
- `id` - Auto-increment ID
- `referrer_id` - User who made the referral
- `referred_id` - User who was referred
- `referral_date` - When referral happened
- `is_valid` - Whether referral is valid

### Additional tables for improved version:
- `bot_stats` - Daily statistics
- `invite_link_usage` - Tracking of invite link usage

## Running Giveaways

1. Use `/topusers` command to get list of top referrers
2. Copy user IDs and details for your giveaway
3. Contact winners directly using their user IDs
4. Announce winners in your channel

## Troubleshooting

### Common Issues:

1. **"Couldn't create invite link"**:
   - Make sure bot is admin in your channel
   - Check bot has "Invite users via link" permission
   - Verify CHANNEL_ID is correct

2. **Bot not responding**:
   - Check BOT_TOKEN is correct
   - Ensure bot is running
   - Check internet connection

3. **Referrals not counting**:
   - Users must join via the specific invite link
   - Each link is unique to one user
   - Bot must be admin when user joins

### Error Logs:
The bot logs all activities. Check console output for detailed error messages.

## Security Notes

- Use environment variables for sensitive information
- Only share admin commands with trusted users
- Regularly backup your database file (`referral_bot.db`)
- Monitor bot logs for suspicious activity
- Never commit your actual bot token to version control

## Customization

You can customize:
- Welcome messages
- Button texts
- Leaderboard size
- Database schema
- Admin permissions

## Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify all configuration values
3. Check bot permissions in your channel
4. Review error logs in console

## License

This project is open source. Feel free to modify and distribute.

---

**Happy referring! 🚀**