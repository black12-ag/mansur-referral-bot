#!/usr/bin/env python3
"""
Telegram Referral Bot Starter Script
This script provides an easy way to start the bot with proper error handling.
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def load_env_file():
    """Load environment variables from .env file if it exists"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("🔑 Loading environment variables from .env file...")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")
        return True
    return False

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Try to load .env file if it exists
    env_loaded = load_env_file()
    if env_loaded:
        print("✅ Environment variables loaded from .env file")
    
    # Check if config.py exists
    if not os.path.exists("config.py"):
        print("❌ config.py not found!")
        print("💡 Run 'python setup.py' first to configure the bot")
        return False
    
    # Check if main bot file exists
    if not os.path.exists("telegram_referral_bot_improved.py"):
        print("❌ telegram_referral_bot_improved.py not found!")
        return False
    
    # Try to import required modules
    try:
        import telegram
        print("✅ python-telegram-bot is installed")
    except ImportError:
        print("❌ python-telegram-bot not installed")
        print("💡 Run 'pip install -r requirements.txt' to install dependencies")
        return False
    
    # Check config values and environment variables
    try:
        import config
        
        # Check if token is available (either in config or environment)
        if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" and "TELEGRAM_BOT_TOKEN" not in os.environ:
            print("❌ Bot token not configured in config.py or as TELEGRAM_BOT_TOKEN environment variable")
            return False
        
        # Check channel ID
        if config.CHANNEL_ID == "@your_channel" and "TELEGRAM_CHANNEL_ID" not in os.environ:
            print("❌ Channel ID not configured in config.py or as TELEGRAM_CHANNEL_ID environment variable")
            return False
        
        # Check admin user ID
        if config.ADMIN_USER_ID == 123456789 and "TELEGRAM_ADMIN_USER_ID" not in os.environ:
            print("❌ Admin user ID not configured in config.py or as TELEGRAM_ADMIN_USER_ID environment variable")
            return False
        
        print("✅ Configuration looks good")
    except ImportError:
        print("❌ Could not import config.py")
        return False
    except Exception as e:
        print(f"❌ Error in config.py: {e}")
        return False
    
    return True

def show_bot_info():
    """Show bot information before starting"""
    try:
        import config
        print("\n" + "="*50)
        print("🤖 TELEGRAM REFERRAL BOT")
        print("="*50)
        print(f"📢 Channel: {config.CHANNEL_ID}")
        print(f"👑 Admin ID: {config.ADMIN_USER_ID}")
        print(f"📊 Database: {config.DATABASE_NAME}")
        print(f"📅 Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show which configuration source is being used
        if "TELEGRAM_BOT_TOKEN" in os.environ:
            print("🔒 Using environment variables for sensitive data")
        else:
            print("⚠️ Using values from config.py (consider using environment variables)")
        
        print("="*50)
    except Exception as e:
        print(f"⚠️ Could not load config: {e}")

def start_bot():
    """Start the bot with proper error handling"""
    print("\n🚀 Starting the bot...")
    print("💡 Press Ctrl+C to stop the bot\n")
    
    try:
        # Import and run the bot
        import telegram_referral_bot_improved
        telegram_referral_bot_improved.main()
    except KeyboardInterrupt:
        print("\n\n🛑 Bot stopped by user")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all files are in the same directory")
    except Exception as e:
        print(f"❌ Bot crashed: {e}")
        print("💡 Check the error message above for details")
        return False
    
    return True

def show_help():
    """Show help information"""
    print("\n📋 Telegram Referral Bot Starter")
    print("\nUsage:")
    print("  python start_bot.py        - Start the bot")
    print("  python start_bot.py --help - Show this help")
    print("  python start_bot.py --check - Check requirements only")
    print("\nFirst time setup:")
    print("  1. Run 'python setup.py' to configure the bot")
    print("  2. Add your bot as admin to your Telegram channel")
    print("  3. Run 'python start_bot.py' to start the bot")
    print("\nEnvironment variables (recommended):")
    print("  - TELEGRAM_BOT_TOKEN: Your bot token")
    print("  - TELEGRAM_CHANNEL_ID: Your channel ID or username")
    print("  - TELEGRAM_ADMIN_USER_ID: Your Telegram user ID")
    print("  These can be set in a .env file or as system environment variables")
    print("\nTroubleshooting:")
    print("  - Make sure config.py is properly configured")
    print("  - Check that your bot token is valid")
    print("  - Ensure the bot is admin in your channel")
    print("  - Verify your channel ID is correct")

def main():
    """Main function"""
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            show_help()
            return
        elif sys.argv[1] == "--check":
            if check_requirements():
                print("✅ All requirements met!")
            else:
                print("❌ Some requirements are missing")
            return
    
    # Check requirements
    if not check_requirements():
        print("\n💡 Fix the issues above and try again")
        return
    
    # Show bot info
    show_bot_info()
    
    # Start the bot
    if start_bot():
        print("\n✅ Bot session ended normally")
    else:
        print("\n❌ Bot session ended with errors")
        print("💡 Check the logs above for details")

if __name__ == "__main__":
    main()