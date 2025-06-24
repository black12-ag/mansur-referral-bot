"""
Language management for Telegram Referral Bot
"""

import os
import importlib
from typing import Dict, List, Optional

# Default language
DEFAULT_LANGUAGE = "english"

# Available languages
language_modules = {}
_current_language = None

def load_languages():
    """Load all available language modules from the languages directory"""
    global language_modules
    
    # Get the directory of this file
    languages_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all Python files in the languages directory
    language_files = [f for f in os.listdir(languages_dir) 
                     if f.endswith('.py') and f != '__init__.py']
    
    # Import each language module
    for file in language_files:
        lang_name = file[:-3]  # Remove .py extension
        try:
            module = importlib.import_module(f"languages.{lang_name}")
            language_modules[lang_name] = module
            print(f"Loaded language: {module.LANGUAGE_NAME} ({lang_name})")
        except (ImportError, AttributeError) as e:
            print(f"Error loading language {lang_name}: {e}")
    
    return language_modules

def get_available_languages() -> List[Dict[str, str]]:
    """Get list of available languages with their details"""
    languages = []
    for name, module in language_modules.items():
        languages.append({
            'code': name,
            'name': getattr(module, 'LANGUAGE_NAME', name),
            'language_code': getattr(module, 'LANGUAGE_CODE', name[:2])
        })
    return languages

def get_language(lang_code: str = DEFAULT_LANGUAGE):
    """Get a specific language module"""
    global _current_language
    
    if not language_modules:
        load_languages()
    
    if lang_code in language_modules:
        _current_language = language_modules[lang_code]
        return _current_language
    
    # Fallback to default language
    _current_language = language_modules.get(DEFAULT_LANGUAGE)
    return _current_language

def get_text(key: str, **kwargs) -> str:
    """Get text in the current language with formatting"""
    if not _current_language:
        get_language()
    
    text = getattr(_current_language, key, f"Missing text: {key}")
    
    # Apply formatting if kwargs provided
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError as e:
            return f"Formatting error in {key}: {e}"
    
    return text

# Initialize languages on import
load_languages() 