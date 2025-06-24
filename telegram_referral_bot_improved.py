import logging
import sqlite3
import time
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, BotCommandScopeChat
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import asyncio
import os
from telegram.error import TelegramError
import config
import logging
import languages
from urllib.parse import quote

# Configure logging
logging.basicConfig(
    format=config.LOG_FORMAT,
    level=getattr(logging, config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)


class ReferralBot:
    def __init__(self):
        self.init_database()
        self.languages = languages.get_available_languages()

    def init_database(self):
        """Initialize SQLite database"""
        self.conn = sqlite3.connect(
            config.DATABASE_NAME,
            check_same_thread=config.DB_CHECK_SAME_THREAD,
            timeout=config.DB_TIMEOUT
        )
        self.cursor = self.conn.cursor()

        # Create users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                invite_link TEXT UNIQUE,
                referral_count INTEGER DEFAULT 0,
                referred_by INTEGER,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                language_code TEXT DEFAULT 'english'
            )
        ''')

        # Create referrals table for tracking
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER,
                referred_id INTEGER,
                referral_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_valid BOOLEAN DEFAULT 1,
                FOREIGN KEY (referrer_id) REFERENCES users (user_id),
                FOREIGN KEY (referred_id) REFERENCES users (user_id)
            )
        ''')

        # Create bot_stats table for tracking bot performance
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT CURRENT_DATE,
                new_users INTEGER DEFAULT 0,
                total_referrals INTEGER DEFAULT 0,
                active_users INTEGER DEFAULT 0
            )
        ''')

        # Create invite_link_usage table for tracking actual channel joins
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS invite_link_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invite_link TEXT,
                owner_user_id INTEGER,
                uses_count INTEGER DEFAULT 0,
                last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_user_id) REFERENCES users (user_id)
            )
        ''')

        self.conn.commit()
        logger.info("Database initialized successfully")

    def get_user_language(self, user_id):
        """Get user's preferred language"""
        self.cursor.execute(
    "SELECT language_code FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return 'english'  # Default language

    def set_user_language(self, user_id, language_code):
        """Set user's preferred language"""
        self.cursor.execute("UPDATE users SET language_code = ? WHERE user_id = ?",
                           (language_code, user_id))
        self.conn.commit()
        return True

    async def start_command(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = user.id
        username = user.username or "No username"
        first_name = user.first_name or "Unknown"

        logger.info(f"User {user_id} ({first_name}) started the bot")

        # Get telegram locale or fallback to english
        telegram_locale = user.language_code
        if telegram_locale:
            # Map common language codes to our language codes
            if telegram_locale.startswith('am'):
                initial_lang = 'amharic'
            elif telegram_locale.startswith('om'):
                initial_lang = 'oromo'
            elif telegram_locale.startswith('ti'):
                initial_lang = 'tigrinya'
            else:
                initial_lang = 'english'
        else:
            initial_lang = 'english'

        # Check if user already exists
        self.cursor.execute(
    "SELECT * FROM users WHERE user_id = ?", (user_id,))
        existing_user = self.cursor.fetchone()

        if existing_user:
            # Get user's preferred language
            user_lang = self.get_user_language(user_id)
            lang = languages.get_language(user_lang)

            invite_link = existing_user[3]
            referral_count = existing_user[4]

            # Create share message for direct Telegram sharing
            share_message = (
                f"{lang.JOIN_CHANNEL_PROMPT}\n\n"
                f"{lang.EXCLUSIVE_CONTENT}\n"
                f"{lang.GROWING_COMMUNITY}\n\n"
                f"{lang.CLICK_TO_JOIN}: {invite_link}\n\n"
                f"{lang.SHARED_BY} {first_name}"
            )

            # Encode message for URL sharing
            encoded_message = quote(share_message)

            # Create a direct copy button that will trigger a copy notification
            copy_button = InlineKeyboardButton(
                lang.BTN_COPY_LINK,
                callback_data="copy_link"
            )

            keyboard = [
                [InlineKeyboardButton(
                    lang.BTN_MY_STATS, callback_data="stats")],
                [copy_button,
                 InlineKeyboardButton(lang.BTN_SHARE_LINK, url=f"https://t.me/share/url?url={invite_link}&text={encoded_message}")],
                [InlineKeyboardButton(
                    lang.BTN_LEADERBOARD, callback_data="leaderboard")],
                [InlineKeyboardButton(
                    lang.BTN_LANGUAGE, callback_data="language")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Create welcome message with user's referral stats
            referral_count = self.get_user_referral_count(user_id)
            welcome_text = lang.WELCOME_RETURNING.format(
                first_name=first_name,
                referral_count=referral_count,
                # Make link monospace for easy copying
                invite_link=f"`{invite_link}`"
            )
            message_text = welcome_text

            await update.message.reply_text(message_text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            # Create new invite link for the user
            try:
                # Set user's initial language from Telegram locale
                initial_language = initial_lang

                # Create a unique invite link for this user
                # Use username if available, otherwise use first name
                display_name = username if username else first_name
                invite_link_name = config.INVITE_LINK_NAME_TEMPLATE.format(
                    display_name=display_name)

                # Create invite link with no member limit and no expiration
                invite_link = await context.bot.create_chat_invite_link(
                    chat_id=config.CHANNEL_ID,
                    name=invite_link_name
                    # No member_limit and no expire_date for unlimited usage
                )

                # Check if user was referred by someone
                referred_by = None
                if context.args:
                    try:
                        referred_by = int(context.args[0])
                        # Verify referrer exists
                        self.cursor.execute(
    "SELECT user_id FROM users WHERE user_id = ?", (referred_by,))
                        if not self.cursor.fetchone():
                            referred_by = None
                    except ValueError:
                        referred_by = None

                # Insert new user with language preference
                self.cursor.execute(
                    "INSERT INTO users (user_id, username, first_name, invite_link, referred_by, language_code) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id,
    username,
    first_name,
    invite_link.invite_link,
    referred_by,
     initial_language)
                )

                # Get language module for the user
                lang = languages.get_language(initial_language)

                # Add invite link to tracking table
                self.cursor.execute(
                    "INSERT INTO invite_link_usage (invite_link, owner_user_id, uses_count) VALUES (?, ?, 0)",
                    (invite_link.invite_link, user_id)
                )

                # If user was referred, update referrer's count and add to
                # referrals table
                if referred_by:
                    self.cursor.execute(
                        "UPDATE users SET referral_count = referral_count + 1 WHERE user_id = ?",
                        (referred_by,)
                    )
                    self.cursor.execute(
                        "INSERT INTO referrals (referrer_id, referred_id) VALUES (?, ?)",
                        (referred_by, user_id)
                    )

                    # Get updated referral count
                    updated_count = self.get_user_referral_count(referred_by)

                    # Get referrer's language
                    referrer_lang_code = self.get_user_language(referred_by)
                    referrer_lang = languages.get_language(referrer_lang_code)

                    # Notify referrer with enhanced real-time update
                    try:
                        # Get referrer info for personalized message
                        self.cursor.execute(
    "SELECT first_name, username FROM users WHERE user_id = ?", (referred_by,))
                        referrer_info = self.cursor.fetchone()
                        referrer_name = referrer_info[0] if referrer_info else "User"

                        notification_text = referrer_lang.REFERRAL_SUCCESS.format(
                            first_name=first_name,
                            referral_count=updated_count
                        )

                        await context.bot.send_message(
                            chat_id=referred_by,
                            text=notification_text
                        )
                        logger.info(
    f"Sent real-time referral update to {referred_by} (count: {updated_count})")
                    except TelegramError as e:
                        logger.warning(
    f"Could not notify referrer {referred_by}: {e}")

                self.conn.commit()

                # Create share message for direct Telegram sharing
                share_message = (
                    f"{lang.JOIN_CHANNEL_PROMPT}\n\n"
                    f"{lang.EXCLUSIVE_CONTENT}\n"
                    f"{lang.GROWING_COMMUNITY}\n\n"
                    f"{lang.CLICK_TO_JOIN}: {invite_link.invite_link}\n\n"
                    f"{lang.SHARED_BY} {first_name}"
                )

                # Encode message for URL sharing
                encoded_message = quote(share_message)

                # Create a direct copy button that will trigger a copy
                # notification
                copy_button = InlineKeyboardButton(
                    lang.BTN_COPY_LINK,
                    callback_data="copy_link"
                )

                keyboard = [
                    [InlineKeyboardButton(
                        lang.BTN_MY_STATS, callback_data="stats")],
                    [copy_button,
                     InlineKeyboardButton(lang.BTN_SHARE_LINK, url=f"https://t.me/share/url?url={invite_link.invite_link}&text={encoded_message}")],
                    [InlineKeyboardButton(
                        lang.BTN_LEADERBOARD, callback_data="leaderboard")],
                    [InlineKeyboardButton(
                        lang.BTN_LANGUAGE, callback_data="language")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                # Create welcome message for new user
                welcome_text = lang.WELCOME_NEW.format(
                    first_name=first_name,
                    # Make link monospace for easy copying
                    invite_link=f"`{invite_link.invite_link}`"
                )

                # Add referral success message if referred
                if referred_by:
                    welcome_text = "✅ " + lang.REFERRAL_SUCCESS.format(
                        first_name=first_name,
                        referral_count=0
                    ) + "\n\n" + welcome_text

                await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
                logger.info(f"Created new user {user_id} with invite link")

            except TelegramError as e:
                logger.error(
    f"Error creating invite link for user {user_id}: {e}")
                # Get language module for the user
                lang = languages.get_language(initial_lang)
                await update.message.reply_text(lang.ERROR_INVITE_LINK_FAILED)

    def get_user_referral_count(self, user_id):
        """Get user's current referral count"""
        self.cursor.execute(
    "SELECT referral_count FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    async def check_invite_link_usage(
    self, context: ContextTypes.DEFAULT_TYPE):
        """Check invite link usage and update referral counts based on actual channel joins"""
        try:
            # Get all invite links from the database
            self.cursor.execute(
                "SELECT invite_link, owner_user_id, uses_count FROM invite_link_usage")
            invite_links = self.cursor.fetchall()

            for invite_link, owner_user_id, current_uses in invite_links:
                try:
                    # Get current usage count from Telegram
                    link_info = await context.bot.get_chat_invite_link(
                        chat_id=config.CHANNEL_ID,
                        invite_link=invite_link
                    )

                    actual_uses = link_info.member_count or 0

                    # If there are new uses, update the referral count
                    if actual_uses > current_uses:
                        new_referrals = actual_uses - current_uses

                        # Update user's referral count
                        self.cursor.execute(
                            "UPDATE users SET referral_count = referral_count + ? WHERE user_id = ?",
                            (new_referrals, owner_user_id)
                        )

                        # Update invite link usage count
                        self.cursor.execute(
                            "UPDATE invite_link_usage SET uses_count = ?, last_checked = CURRENT_TIMESTAMP WHERE invite_link = ?",
                            (actual_uses, invite_link)
                        )

                        # Get updated referral count and user info
                        self.cursor.execute(
    "SELECT first_name, referral_count FROM users WHERE user_id = ?", (owner_user_id,))
                        user_info = self.cursor.fetchone()

                        if user_info:
                            first_name, total_referrals = user_info

                            # Send notification to the referrer
                            notification_text = f"🎉 GREAT NEWS {first_name}!\n\n" \
                                              f"✅ {new_referrals} new member(s) joined through your invite link!\n" \
                                              f"📊 Your TOTAL referrals: {total_referrals}\n\n" \
                                              f"🚀 Keep sharing your link to get more referrals!\n" \
                                              f"🏆 Check /start to see your updated stats!"

                            try:
                                await context.bot.send_message(
                                    chat_id=owner_user_id,
                                    text=notification_text
                                )
                                logger.info(
    f"Notified user {owner_user_id} about {new_referrals} new channel joins")
                            except TelegramError as e:
                                logger.warning(
    f"Could not notify user {owner_user_id}: {e}")

                        self.conn.commit()
                        logger.info(
    f"Updated referral count for user {owner_user_id}: +{new_referrals} (total: {actual_uses})")

                    else:
                        # Just update the last checked time
                        self.cursor.execute(
                            "UPDATE invite_link_usage SET last_checked = CURRENT_TIMESTAMP WHERE invite_link = ?",
                            (invite_link,)
                        )

                except TelegramError as e:
                    logger.warning(
    f"Could not check invite link {invite_link}: {e}")
                    continue

            self.conn.commit()

        except Exception as e:
            logger.error(f"Error checking invite link usage: {e}")

    async def button_callback(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id

        # Get user language
        user_lang = self.get_user_language(user_id)
        lang = languages.get_language(user_lang)

        if query.data == "stats":
            await self.show_user_stats(query, user_id)
        elif query.data == "copy_link":
            await self.show_copy_link(query, user_id)
        elif query.data == "copy_link_again":
            # Just show the copy notification again without changing the screen
            self.cursor.execute(
    "SELECT invite_link FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()
            if result:
                await query.answer(lang.LINK_COPIED_ALERT, show_alert=True)
                logger.info(f"User {user_id} copied link again")
            else:
                await query.answer(config.ERROR_MESSAGES["user_not_found"], show_alert=True)
        elif query.data == "share_link":
            await self.show_share_link(query, user_id)
        elif query.data.startswith("copy_share_"):
            await self.handle_copy_share_message(query, user_id)
        elif query.data == "leaderboard":
            await self.show_leaderboard(query, user_id)
        elif query.data == "main_menu":
            await self.show_main_menu(query, user_id)
        elif query.data == "language":
            await self.show_language_selection(query, user_id)
        elif query.data.startswith("setlang_"):
            language_code = query.data.split("_")[1]
            await self.set_language(query, user_id, language_code)

    async def show_user_stats(self, query, user_id):
        """Show user statistics"""
        self.cursor.execute(
            "SELECT username, first_name, referral_count, join_date FROM users WHERE user_id = ?",
            (user_id,)
        )
        user_data = self.cursor.fetchone()

        if user_data:
            username, first_name, referral_count, join_date = user_data

            # Get user's rank
            self.cursor.execute(
                "SELECT COUNT(*) + 1 FROM users WHERE referral_count > (SELECT referral_count FROM users WHERE user_id = ?)",
                (user_id,)
            )
            rank = self.cursor.fetchone()[0]

            # Get total users for percentage calculation
            self.cursor.execute("SELECT COUNT(*) FROM users")
            total_users = self.cursor.fetchone()[0]

            percentage = round(
    (total_users - rank + 1) / total_users * 100,
     1) if total_users > 0 else 0

            stats_text = (
                f"📊 Your Statistics\n\n"
                f"👤 Name: {first_name}\n"
                f"🆔 Username: @{username}\n"
                f"🎯 Referrals: {referral_count}\n"
                f"🏆 Rank: #{rank} (Top {percentage}%)\n"
                f"📅 Joined: {join_date[:10]}\n\n"
                f"Keep sharing your link to climb the leaderboard! 🚀"
            )

            # Add back button
            keyboard = [[InlineKeyboardButton(
                "🔙 Back to Menu", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(stats_text, reply_markup=reply_markup)
            logger.info(f"Showed stats for user {user_id}")
        else:
            await query.edit_message_text(config.ERROR_MESSAGES["user_not_found"])

    async def show_copy_link(self, query, user_id):
        """Show user's invite link for copying"""
        self.cursor.execute(
    "SELECT invite_link FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()

        if result:
            invite_link = result[0]

            # Get user language
            user_lang = self.get_user_language(user_id)
            lang = languages.get_language(user_lang)

            # Answer callback query with notification that link is copied
            await query.answer(lang.LINK_COPIED_ALERT, show_alert=True)

            link_text = (
                f"🔗 {lang.YOUR_INVITE_LINK}\n\n"
                f"`{invite_link}`\n\n"
                f"✅ {lang.LINK_COPIED}\n"
                f"📢 {lang.SHARE_LINK_PROMPT}\n"
                f"🎁 {lang.REFERRAL_EXPLANATION}\n\n"
                f"✨ {lang.LINK_NO_LIMITS}\n"
                f"💡 {lang.SHARING_TIP}"
            )

            # Create keyboard with buttons for copy and share
            keyboard = [
                [InlineKeyboardButton(
                    lang.BTN_CLICK_TO_COPY, callback_data="copy_link_again")],
                [InlineKeyboardButton(lang.BTN_SHARE_NOW,
                                      callback_data="share_link")],
                [InlineKeyboardButton(
                    lang.BTN_BACK, callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(link_text, reply_markup=reply_markup, parse_mode='Markdown')
            logger.info(f"Showed copy link for user {user_id}")
        else:
            await query.edit_message_text(config.ERROR_MESSAGES["user_not_found"])

    async def show_share_link(self, query, user_id):
        """Show direct share options for user's invite link"""
        self.cursor.execute(
    "SELECT invite_link, first_name FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()

        if result:
            invite_link, first_name = result

            # Get user language
            user_lang = self.get_user_language(user_id)
            lang = languages.get_language(user_lang)

            # Create share message
            share_message = (
                f"🎉 {lang.JOIN_CHANNEL_PROMPT}\n\n"
                f"👥 {lang.EXCLUSIVE_CONTENT}\n"
                f"🚀 {lang.GROWING_COMMUNITY}\n\n"
                f"{lang.CLICK_TO_JOIN}: {invite_link}\n\n"
                f"{lang.SHARED_BY} {first_name} 😊"
            )

            # Encode message for URL sharing
            encoded_message = quote(share_message)

            # Create inline keyboard with direct share options
            keyboard = [
                [
    InlineKeyboardButton(
        lang.BTN_SHARE_TELEGRAM,
         url=f"https://t.me/share/url?url={invite_link}&text={encoded_message}")],
                [InlineKeyboardButton(
                    lang.BTN_SHARE_WHATSAPP, url=f"https://wa.me/?text={encoded_message}")],
                [InlineKeyboardButton(
                    lang.BTN_SHARE_TWITTER, url=f"https://twitter.com/intent/tweet?text={encoded_message}")],
                [InlineKeyboardButton(
                    lang.BTN_COPY_SHARE_MSG, callback_data=f"copy_share_{user_id}")],
                [InlineKeyboardButton(
                    lang.BTN_BACK, callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            share_text = (
                f"📤 {lang.SHARE_INVITE_LINK}\n\n"
                f"{lang.CHOOSE_SHARE_METHOD}:\n\n"
                f"🔗 {lang.YOUR_LINK}: `{invite_link}`\n\n"
                f"💡 {lang.SHARE_MORE_REFERRALS}"
            )

            await query.edit_message_text(share_text, reply_markup=reply_markup, parse_mode='Markdown')
            logger.info(f"Showed direct share options for user {user_id}")
        else:
            await query.edit_message_text(config.ERROR_MESSAGES["user_not_found"])

    async def show_leaderboard(self, query, user_id):
        """Show top referrers leaderboard with user's rank and privacy protection"""
        is_admin = user_id == config.ADMIN_USER_ID

        # Get top users
        self.cursor.execute(
            "SELECT first_name, username, referral_count FROM users WHERE referral_count > 0 ORDER BY referral_count DESC LIMIT ?",
            (config.DEFAULT_LEADERBOARD_SIZE,)
        )
        top_users = self.cursor.fetchall()

        # Get user's rank and info
        self.cursor.execute(
            "SELECT COUNT(*) + 1 FROM users WHERE referral_count > (SELECT referral_count FROM users WHERE user_id = ?)",
            (user_id,)
        )
        user_rank = self.cursor.fetchone()[0]

        self.cursor.execute(
            "SELECT first_name, referral_count FROM users WHERE user_id = ?",
            (user_id,)
        )
        user_info = self.cursor.fetchone()

        def get_display_name(first_name, username, is_current_user=False):
            """Get display name with privacy protection"""
            if is_admin:
                # Admin can see full usernames
                username_display = f"@{username}" if username != "No username" else "No username"
                return f"{first_name} ({username_display})"
            elif is_current_user:
                # User can see their own full name
                return f"{first_name} (You)"
            else:
                # Other users see only partial first name
                if len(first_name) <= 2:
                    partial_name = first_name[0] + "*"
                else:
                    partial_name = first_name[:len(
                        first_name) // 2] + "*" * (len(first_name) - len(first_name) // 2)
                return partial_name

        if top_users:
            leaderboard_text = "🏆 Top Referrers Leaderboard\n\n"

            medals = ["🥇", "🥈", "🥉"]

            for i, (first_name, username, count) in enumerate(top_users, 1):
                medal = medals[i - 1] if i <= 3 else f"{i}."
                # Check if this is the current user in the leaderboard
                self.cursor.execute(
    "SELECT user_id FROM users WHERE first_name = ? AND username = ? AND referral_count = ?",
    (first_name,
    username,
     count))
                leaderboard_user_id = self.cursor.fetchone()
                is_current_user = leaderboard_user_id and leaderboard_user_id[0] == user_id

                display_name = get_display_name(
    first_name, username, is_current_user)
                leaderboard_text += f"{medal} {display_name} - {count} referrals\n"

            # Add user's rank if they're not in top list
            if user_info:
                user_name, user_referrals = user_info
                if user_rank > config.DEFAULT_LEADERBOARD_SIZE:
                    leaderboard_text += f"\n📍 Your Position:\n"
                    leaderboard_text += f"{user_rank}. {user_name} (You) - {user_referrals} referrals\n"
                else:
                    leaderboard_text += f"\n📍 You are #{user_rank} with {user_referrals} referrals!\n"

            leaderboard_text += "\n🎯 Keep referring to climb higher!"

            # Add back button
            keyboard = [[InlineKeyboardButton(
                "🔙 Back to Menu", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(leaderboard_text, reply_markup=reply_markup)
            logger.info("Showed leaderboard")
        else:
            await query.edit_message_text(config.ERROR_MESSAGES["no_referrals"])

    async def handle_copy_share_message(self, query, user_id):
        """Handle copy share message callback"""
        self.cursor.execute(
    "SELECT invite_link, first_name FROM users WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()

        if result:
            invite_link, first_name = result

            # Create share message
            share_message = (
                f"🎉 Join our amazing channel through my referral link!\n\n"
                f"👥 Get exclusive content and updates\n"
                f"🚀 Be part of our growing community\n\n"
                f"Click here to join: {invite_link}\n\n"
                f"Shared by {first_name} 😊"
            )

            copy_text = (
                f"📋 Copy the message below and share it anywhere:\n\n"
                f"`{share_message}`\n\n"
                f"💡 Tap and hold the message above to copy it!\n"
                f"📱 Share it on WhatsApp, Facebook, Twitter, or anywhere else!"
            )

            # Add back button
            keyboard = [[InlineKeyboardButton(
                "🔙 Back to Share Options", callback_data="share_link")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(copy_text, reply_markup=reply_markup, parse_mode='Markdown')
            logger.info(f"Showed copy share message for user {user_id}")
        else:
            await query.edit_message_text(config.ERROR_MESSAGES["user_not_found"])

    async def show_main_menu(self, query, user_id):
        """Show main menu with all options"""
        # Get user's preferred language
        user_lang = self.get_user_language(user_id)
        lang = languages.get_language(user_lang)

        # Get user's referral count
        referral_count = self.get_user_referral_count(user_id)

            # Get user's invite link
        self.cursor.execute(
    "SELECT invite_link, first_name FROM users WHERE user_id = ?", (user_id,))
        user_data = self.cursor.fetchone()
        if user_data:
            invite_link = user_data[0]
            first_name = user_data[1]

            keyboard = [
                [InlineKeyboardButton(
                    lang.BTN_MY_STATS, callback_data="stats")],
                [InlineKeyboardButton(lang.BTN_COPY_LINK, callback_data="copy_link"),
                 InlineKeyboardButton(lang.BTN_SHARE_LINK, callback_data="share_link")],
                [InlineKeyboardButton(
                    lang.BTN_LEADERBOARD, callback_data="leaderboard")],
                [InlineKeyboardButton(
                    lang.BTN_LANGUAGE, callback_data="language")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            welcome_text = lang.WELCOME_RETURNING.format(
                first_name=first_name,
                referral_count=referral_count,
                # Make link monospace for easy copying
                invite_link=f"`{invite_link}`"
            )

            await query.edit_message_text(text=welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await query.edit_message_text(lang.ERROR_USER_NOT_FOUND)

    async def show_language_selection(self, query, user_id):
        """Show language selection keyboard"""
        # Get user language
        user_lang = self.get_user_language(user_id)
        lang = languages.get_language(user_lang)

        # Create language selection buttons
        keyboard = []
        for language in self.languages:
            keyboard.append([
                InlineKeyboardButton(
                    f"{language['name']} {'✓' if language['code'] == user_lang else ''}",
                    callback_data=f"setlang_{language['code']}"
                )
            ])

        # Add back button
        keyboard.append([InlineKeyboardButton(
            lang.BTN_BACK, callback_data="main_menu")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Show language selection message
        await query.edit_message_text(
            lang.LANGUAGE_SELECTION,
            reply_markup=reply_markup
        )

    async def set_language(self, query, user_id, language_code):
        """Set user's preferred language"""
        # Update user's language in database
        self.set_user_language(user_id, language_code)

        # Get the new language
        lang = languages.get_language(language_code)

        # Show confirmation message
        await query.edit_message_text(
            lang.LANGUAGE_CHANGED,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    lang.BTN_BACK, callback_data="main_menu")]
            ])
        )

    async def language_command(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Handle /language command"""
        user_id = update.effective_user.id
        user_lang = self.get_user_language(user_id)
        lang = languages.get_language(user_lang)

        # Create language selection buttons
        keyboard = []
        for language in self.languages:
            keyboard.append([
                InlineKeyboardButton(
                    f"{language['name']} {'✓' if language['code'] == user_lang else ''}",
                    callback_data=f"setlang_{language['code']}"
                )
            ])

        # Add back button
        keyboard.append([InlineKeyboardButton(
            lang.BTN_BACK, callback_data="main_menu")])

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Show language selection message
        await update.message.reply_text(
            lang.LANGUAGE_SELECTION,
            reply_markup=reply_markup
        )

    async def admin_stats(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Admin command to view bot statistics"""
        if update.effective_user.id != config.ADMIN_USER_ID:
            await update.message.reply_text("❌ You're not authorized to use this command.")
            return

        # Always use English for admin commands
        # Ignoring user language preference for admin commands

        # Get today's date for the query
        today = datetime.now().strftime("%Y-%m-%d")

        try:
            # Get daily stats
            self.cursor.execute(
                "SELECT date, new_users, total_referrals, active_users FROM bot_stats "
                "WHERE date >= date('now', '-7 days') ORDER BY date DESC"
            )
            weekly_stats = self.cursor.fetchall()

            # Total user count
            self.cursor.execute("SELECT COUNT(*) FROM users")
            total_users = self.cursor.fetchone()[0]

            # Active user count (users with at least one referral)
            self.cursor.execute(
                "SELECT COUNT(*) FROM users WHERE referral_count > 0")
            active_referrers = self.cursor.fetchone()[0]

            # Total referrals
            self.cursor.execute("SELECT SUM(referral_count) FROM users")
            total_referrals = self.cursor.fetchone()[0] or 0

            # Average referrals per user
            avg_referrals = round(
    total_referrals / total_users,
     2) if total_users > 0 else 0

            # Conversion rate (percentage of users who have referred at least
            # one person)
            conversion_rate = round(
    active_referrers / total_users * 100,
     2) if total_users > 0 else 0

            # Format the stats message
            stats_message = (
                f"📊 **Bot Statistics**\n\n"
                f"👥 Total Users: {total_users}\n"
                f"🎯 Total Referrals: {total_referrals}\n"
                f"📈 Active Referrers: {active_referrers} ({conversion_rate}%)\n"
                f"📊 Avg. Referrals/User: {avg_referrals}\n\n"
                f"📅 **Last 7 Days Activity:**\n"
            )

            if weekly_stats:
                for date, new_users, day_referrals, day_active in weekly_stats:
                    stats_message += f"• {date}: +{new_users} users, +{day_referrals} referrals, {day_active} active\n"
            else:
                stats_message += "No activity recorded in the past 7 days\n"

            await update.message.reply_text(stats_message, parse_mode='Markdown')
            logger.info(f"Admin {update.effective_user.id} viewed statistics")
        except Exception as e:
            logger.error(f"Error in admin_stats: {e}")
            await update.message.reply_text(f"❌ Error retrieving stats: {e}")

    async def admin_top_users(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Admin command to view top referrers for giveaways"""
        if update.effective_user.id != config.ADMIN_USER_ID:
            await update.message.reply_text("❌ You're not authorized to use this command.")
            return

        # Always use English for admin commands
        # Ignoring user language preference for admin commands

        # Get number of top users to show (default: 10)
        try:
            limit = int(context.args[0]) if context.args else 10
            limit = max(1, min(limit, 100))  # Ensure between 1 and 100
        except (ValueError, IndexError):
            limit = 10

        try:
            # Get top users with details for contacting them
            self.cursor.execute(
                "SELECT user_id, username, first_name, referral_count FROM users "
                "WHERE referral_count > 0 ORDER BY referral_count DESC LIMIT ?",
                (limit,)
            )
            top_users = self.cursor.fetchall()

            if not top_users:
                await update.message.reply_text("📊 No users with referrals found.")
                return

            # Format the message
            top_users_message = f"🏆 **Top {
    len(top_users)} Users for Giveaway**\n\n"

            for i, (user_id, username, first_name,
                    referral_count) in enumerate(top_users, 1):
                # Add emoji for top 3
                position = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else f"{i}."

                # Format username or user ID for admin to contact
                if username and username != "No username":
                    user_handle = f"@{username}"
                else:
                    user_handle = f"[User ID: {user_id}]"

                top_users_message += f"{position} {first_name} ({user_handle}) - {referral_count} referrals\n"

            top_users_message += f"\n💡 Use these results to select giveaway winners."

            await update.message.reply_text(top_users_message, parse_mode='Markdown')
            logger.info(
    f"Admin {
        update.effective_user.id} viewed top {limit} users")
        except Exception as e:
            logger.error(f"Error in admin_top_users: {e}")
            await update.message.reply_text(f"❌ Error retrieving top users: {e}")

    async def help_command(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = update.effective_user.id
        user_lang = self.get_user_language(user_id)
        lang = languages.get_language(user_lang)

        is_admin = user_id == config.ADMIN_USER_ID

        # Get base help message from language file
        help_message = lang.HELP_MESSAGE

        # For admin users, add admin commands in English regardless of user's
        # language preference
        if is_admin:
            admin_lang = languages.get_language("english")
            help_message += admin_lang.ADMIN_HELP_ADDITION

        await update.message.reply_text(help_message, parse_mode='Markdown')
        logger.info(
    f"Help command used by {
        'admin ' if is_admin else ''}{user_id}")

    async def stats_command(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        user_lang = self.get_user_language(user_id)
        lang = languages.get_language(user_lang)

        try:
            # Get user data
            self.cursor.execute(
                "SELECT first_name, username, referral_count, join_date FROM users WHERE user_id = ?",
                (user_id,)
            )
            user_data = self.cursor.fetchone()

            if not user_data:
                await update.message.reply_text(
                    "❌ User data not found. Please use /start first."
                )
                return

            first_name, username, referral_count, join_date = user_data

            # Get user rank
            self.cursor.execute(
                "SELECT COUNT(*) + 1 FROM users WHERE referral_count > ?",
                (referral_count,)
            )
            rank = self.cursor.fetchone()[0]

            # Get total users count for percentile
            self.cursor.execute("SELECT COUNT(*) FROM users")
            total_users = self.cursor.fetchone()[0]

            # Calculate percentile (higher is better)
            percentile = round(
    (total_users - rank) / total_users * 100,
     1) if total_users > 1 else 0

            # Format the stats message
            stats_text = (
                f"📊 {lang.STATS_HEADER}\n\n"
                f"{lang.STATS_NAME.format(first_name=first_name)}\n"
            )

            if username and username != "No username":
                stats_text += f"{
    lang.STATS_USERNAME.format(
        username=username)}\n"

            stats_text += (
                f"{
    lang.STATS_REFERRALS.format(
        referral_count=referral_count)}\n"
                f"{
    lang.STATS_RANK.format(
        rank=rank)} {
            f'(top {percentile}%)' if percentile > 0 else ''}\n"
                f"{lang.STATS_JOINED.format(join_date=join_date)}\n\n"
                f"{lang.STATS_FOOTER}"
            )

            # Create keyboard with navigation buttons
            keyboard = [
                [InlineKeyboardButton(languages.get_text(
                    "BTN_LEADERBOARD"), callback_data="leaderboard")],
                [InlineKeyboardButton(languages.get_text("BTN_COPY_LINK"), callback_data="copy_link"),
                 InlineKeyboardButton(languages.get_text("BTN_SHARE_LINK"), callback_data="share_link")],
                [InlineKeyboardButton(languages.get_text(
                    "BTN_MAIN_MENU"), callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(stats_text, reply_markup=reply_markup)
            logger.info(f"Stats command used by {user_id}")

        except Exception as e:
            logger.error(f"Error in stats_command: {e}")
            await update.message.reply_text(f"❌ Error retrieving stats: {e}")

    async def broadcast_message(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Admin command to broadcast a message to all users"""
        if update.effective_user.id != config.ADMIN_USER_ID:
            await update.message.reply_text("❌ You're not authorized to use this command.")
            return

        # Always use English for admin commands
        # No language dependency - using hardcoded English for admin interface

        # Get message to broadcast
        if context.args:
            # If arguments are provided with the command, use them
            broadcast_msg = ' '.join(context.args)
            await self._send_broadcast(update, context, broadcast_msg)
        else:
            # Otherwise, ask for the message and set up a conversation handler
            context.user_data['waiting_for_broadcast'] = True
            await update.message.reply_text(
                "📢 Please enter the message you want to broadcast to all users:",
                parse_mode='Markdown'
            )
            return

    async def _send_broadcast(
    self,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
     broadcast_msg):
        """Helper method to send broadcast messages"""
        try:
            # Get all active users
            self.cursor.execute(
                "SELECT user_id FROM users WHERE is_active = 1")
            users = self.cursor.fetchall()

            if not users:
                await update.message.reply_text("📊 No active users found.")
                return

            # Send status message first
            status_message = await update.message.reply_text(
                f"🔄 Broadcasting message to {len(users)} users...\n"
                f"0/{len(users)} completed (0%)"
            )

            # Track successful and failed sends
            success_count = 0
            failed_count = 0
            # Update status every 10% or at least once
            update_interval = max(1, len(users) // 10)

            # Include the admin's name in the broadcast
            admin_name = update.effective_user.first_name
            full_message = f"📢 **Announcement from {admin_name}**\n\n{broadcast_msg}"

            # Send the message to all users with progress updates
            for i, (user_id,) in enumerate(users, 1):
                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=full_message,
                        parse_mode='Markdown'
                    )
                    success_count += 1
                except TelegramError:
                    failed_count += 1

                # Update status message periodically
                if i % update_interval == 0 or i == len(users):
                    progress = int(i / len(users) * 100)
                    await status_message.edit_text(
                        f"🔄 Broadcasting message...\n"
                        f"{i}/{len(users)} completed ({progress}%)\n"
                        f"✅ Success: {success_count}\n"
                        f"❌ Failed: {failed_count}"
                    )

            # Final status update
            await status_message.edit_text(
                f"✅ Broadcast completed!\n"
                f"📊 Total users: {len(users)}\n"
                f"✅ Successfully sent: {success_count}\n"
                f"❌ Failed: {failed_count}"
            )

            logger.info(
    f"Admin {
        update.effective_user.id} broadcast a message to {
            len(users)} users")

        except Exception as e:
            logger.error(f"Error in _send_broadcast: {e}")
            await update.message.reply_text(f"❌ Error broadcasting message: {e}")

    async def admin_reset_all(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Admin command to reset all referral counts (DESTRUCTIVE)"""
        if update.effective_user.id != config.ADMIN_USER_ID:
            await update.message.reply_text("❌ You're not authorized to use this command.")
            return

        # Always use English for admin commands
        # No language dependency - using hardcoded English for admin interface

        # Get confirmation code
        if not context.args or context.args[0].lower() != "confirm":
            await update.message.reply_text(
                "⚠️ **WARNING: This will reset ALL referral data!**\n\n"
                "This action will:\n"
                "- Set all user referral counts to zero\n"
                "- Clear the referrals tracking table\n"
                "- Keep user accounts and invite links\n\n"
                "To proceed, use: `/reset confirm`",
                parse_mode='Markdown'
            )
            return

        try:
            # Reset all referral counts
            self.cursor.execute("UPDATE users SET referral_count = 0")

            # Clear referrals table
            self.cursor.execute("DELETE FROM referrals")

            # Clear invite link usage table
            self.cursor.execute("UPDATE invite_link_usage SET uses_count = 0")

            self.conn.commit()

            await update.message.reply_text(
                "✅ All referral data has been reset!\n\n"
                "- All user referral counts set to zero\n"
                "- Referrals tracking table cleared\n"
                "- Invite link usage counts reset",
                parse_mode='Markdown'
            )

            logger.warning(
    f"Admin {
        update.effective_user.id} reset all referral data")

        except Exception as e:
            logger.error(f"Error in admin_reset_all: {e}")
            await update.message.reply_text(f"❌ Error resetting data: {e}")

    async def admin_menu(
    self,
    update: Update,
     context: ContextTypes.DEFAULT_TYPE):
        """Admin menu with all admin commands"""
        if update.effective_user.id != config.ADMIN_USER_ID:
            await update.message.reply_text("❌ You're not authorized to use this command.")
            return

        # Always use English for admin commands
        # No language dependency - using hardcoded English for admin interface

        admin_menu_text = (
            "👑 **Admin Control Panel**\n\n"
            "Available commands:\n\n"
            "📊 *Statistics*\n"
            "/adminstats - View bot usage statistics\n\n"
            "👥 *User Management*\n"
            "/topusers [number] - View top users for giveaway\n\n"
            "📢 *Communication*\n"
            "/broadcast [message] - Send message to all users\n\n"
            "⚙️ *Advanced*\n"
            "/reset - Reset all referral data (requires confirmation)\n\n"
            "For regular commands, use /help"
        )

        await update.message.reply_text(admin_menu_text, parse_mode='Markdown')
        logger.info(f"Admin {update.effective_user.id} viewed admin menu")

    async def leaderboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /leaderboard command"""
        user_id = update.effective_user.id
        user_lang = self.get_user_language(user_id)
        lang = languages.get_language(user_lang)

        try:
            # Get top users (limit to DEFAULT_LEADERBOARD_SIZE)
            self.cursor.execute(
                "SELECT user_id, first_name, username, referral_count FROM users "
                "ORDER BY referral_count DESC LIMIT ?",
                (config.DEFAULT_LEADERBOARD_SIZE,)
            )
            top_users = self.cursor.fetchall()

            if not top_users:
                await update.message.reply_text("📊 No users with referrals found.")
                return

            # Get current user's rank
            self.cursor.execute(
                "SELECT referral_count FROM users WHERE user_id = ?",
                (user_id,)
            )
            user_result = self.cursor.fetchone()
            if not user_result:
                await update.message.reply_text("❌ User data not found. Please use /start first.")
                return

            user_referrals = user_result[0]

            self.cursor.execute(
                "SELECT COUNT(*) + 1 FROM users WHERE referral_count > ?",
                (user_referrals,)
            )
            user_rank = self.cursor.fetchone()[0]

            # Helper function to format display names
            def get_display_name(first_name, username, is_current_user=False):
                if is_current_user:
                    return f"👉 {first_name}"
                return first_name

            # Format the leaderboard message
            leaderboard_text = f"🏆 {languages.get_text('LEADERBOARD_TITLE')}\n\n"
            
            for i, (leaderboard_user_id, first_name, username, referral_count) in enumerate(top_users, 1):
                # Add emoji for top 3
                position = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"{i}."
                
                is_current_user = leaderboard_user_id == user_id
                display_name = get_display_name(first_name, username, is_current_user)
                
                leaderboard_text += f"{position} {display_name} - {referral_count} {languages.get_text('REFERRALS')}\n"
            
            # Add user's position if not in top list
            user_in_top = any(user[0] == user_id for user in top_users)
            if not user_in_top:
                leaderboard_text += f"\n📍 {languages.get_text('YOUR_POSITION', rank=user_rank, referrals=user_referrals)}"
            
            # Create keyboard with navigation buttons
            keyboard = [
                [InlineKeyboardButton(languages.get_text("BTN_MY_STATS"), callback_data="stats")],
                [InlineKeyboardButton(languages.get_text("BTN_COPY_LINK"), callback_data="copy_link"),
                 InlineKeyboardButton(languages.get_text("BTN_SHARE_LINK"), callback_data="share_link")],
                [InlineKeyboardButton(languages.get_text("BTN_MAIN_MENU"), callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(leaderboard_text, reply_markup=reply_markup)
            logger.info(f"Leaderboard command used by {user_id}")
            
        except Exception as e:
            logger.error(f"Error in leaderboard_command: {e}")
            await update.message.reply_text(f"❌ Error retrieving leaderboard: {e}")
            
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user_id = update.effective_user.id
        
        # Check if we're waiting for a broadcast message from admin
        if user_id == config.ADMIN_USER_ID and context.user_data.get('waiting_for_broadcast'):
            # Get the message text
            broadcast_msg = update.message.text
            
            # Reset the waiting flag
            context.user_data['waiting_for_broadcast'] = False
            
            # Send the broadcast
            await self._send_broadcast(update, context, broadcast_msg)
            return

async def setup_bot_commands(application):
    """Setup bot commands menu with different commands for users and admins"""
    # User commands (visible to all users)
    user_commands = [
        BotCommand("start", "🚀 Start the bot and get your invite link"),
        BotCommand("help", "❓ Get help and see available commands"),
        BotCommand("stats", "📊 View your referral statistics"),
        BotCommand("leaderboard", "🏆 View the referrals leaderboard"),
        BotCommand("language", "🌐 Change language")
    ]
    
    # Admin commands (visible only to admin)
    admin_commands = user_commands + [
        BotCommand("adminmenu", "⚙️ Admin control panel"),
        BotCommand("adminstats", "📈 View bot statistics"),
        BotCommand("topusers", "👥 View top users"),
        BotCommand("broadcast", "📢 Send message to all users"),
        BotCommand("reset", "🔄 Reset all referral data")
    ]
    
    try:
        # Set default commands for all users
        await application.bot.set_my_commands(user_commands)
        
        # Set admin commands for admin user
        admin_scope = BotCommandScopeChat(chat_id=config.ADMIN_USER_ID)
        await application.bot.set_my_commands(admin_commands, scope=admin_scope)
        
        logger.info("Bot commands menu set successfully for users and admin")
    except Exception as e:
        logger.error(f"Failed to set bot commands: {e}")

def main():
    """Main function to start the bot"""
    # Create and configure the application
    application = Application.builder().token(config.BOT_TOKEN).build()
    
    # Set up commands
    bot = ReferralBot()
    
    # User commands
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("stats", bot.stats_command))
    application.add_handler(CommandHandler("leaderboard", bot.leaderboard_command))
    application.add_handler(CommandHandler("language", bot.language_command))
    
    # Admin commands
    application.add_handler(CommandHandler("adminstats", bot.admin_stats))
    application.add_handler(CommandHandler("topusers", bot.admin_top_users))
    application.add_handler(CommandHandler("broadcast", bot.broadcast_message))
    application.add_handler(CommandHandler("adminmenu", bot.admin_menu))
    application.add_handler(CommandHandler("reset", bot.admin_reset_all))
    
    # Button callbacks
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    
    # Text message handler (for broadcast functionality)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_text_message))
    
    # Background tasks
    job_queue = application.job_queue
    job_queue.run_repeating(bot.check_invite_link_usage, interval=3600, first=10)  # Check every hour
    
    # Setup bot commands at initialization
    # Use proper way to handle coroutine
    async def post_init(app):
        """Post initialization tasks"""
        await setup_bot_commands(app)
    
    application.post_init = post_init
    
    # Run the bot until the user presses Ctrl-C
    try:
        logger.info("Starting bot...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            read_timeout=config.TELEGRAM_READ_TIMEOUT,
            write_timeout=config.TELEGRAM_WRITE_TIMEOUT,
            connect_timeout=config.TELEGRAM_CONNECT_TIMEOUT,
            pool_timeout=None
        )
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
    finally:
        # Close database connection
        if hasattr(bot, 'conn'):
            bot.conn.close()

if __name__ == '__main__':
    main()