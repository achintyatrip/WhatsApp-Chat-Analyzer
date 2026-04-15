# ==============================================================================
# WhatsApp Analytics | Enterprise Edition
# Modern, Minimalist, Offline NLP Engine for Corporate & Personal Insight
# ==============================================================================

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, font as tkfont
from tkinter.scrolledtext import ScrolledText
import re
import os
import io
import sys
import base64
import json
import time
import math
import threading
import traceback
import webbrowser
import warnings
import platform
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import string
import textwrap
from pathlib import Path

# Data Science & Plotting
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch
import seaborn as sns
import emoji

# Optional wordcloud
try:
    from wordcloud import WordCloud
    WORDCLOUD_AVAILABLE = True
except Exception:
    WORDCLOUD_AVAILABLE = False

HABITS_FILE = Path("enterprise_habits_db.json")

# ==============================================================================
# MASSIVE OFFLINE LEXICONS & DICTIONARIES (NLP Core)
# ==============================================================================

STOPWORDS_EN = {
    "the", "to", "and", "is", "in", "of", "a", "for", "on", "it", "this", "that", 
    "i", "you", "me", "my", "so", "are", "was", "but", "be", "at", "we", "they", 
    "he", "she", "them", "our", "your", "or", "as", "if", "not", "with", "just", 
    "ok", "okay", "k", "yeah", "yes", "no", "do", "did", "does", "can", "could", 
    "would", "should", "will", "shall", "have", "has", "had", "what", "when", 
    "where", "who", "why", "how", "from", "about", "into", "through", "during", 
    "before", "after", "above", "below", "up", "down", "out", "off", "over", 
    "under", "again", "further", "then", "once", "here", "there", "all", "any", 
    "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", 
    "not", "only", "own", "same", "than", "too", "very", "s", "t", "can", "will", 
    "just", "don", "should", "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", 
    "aren", "couldn", "didn", "doesn", "hadn", "hasn", "haven", "isn", "ma", 
    "mightn", "mustn", "needn", "shan", "shouldn", "wasn", "weren", "won", "wouldn",
    "omitted", "media", "image", "video", "message", "deleted", "this", "im", "ill",
    "am", "pm", "got", "get", "go", "going", "went", "gone", "like", "know", "think",
    "see", "say", "said", "tell", "told", "come", "came", "make", "made", "take", "took",
    "well", "way", "even", "new", "want", "because", "anyway", "two", "much", "many",
    "those", "these", "us", "let", "lets", "give", "gave", "look", "looking", "find"
}

STOPWORDS_HINDI_HINGLISH = {
    "hai", "h", "ho", "hu", "haan", "ha", "nahi", "nhi", "na", "mat", "kya", "kyu", 
    "kaise", "kab", "kaha", "kaun", "kis", "kisko", "kisne", "ki", "ka", "ke", 
    "ko", "mein", "me", "se", "par", "pe", "tak", "liye", "bhi", "hi", "to", "toh", 
    "aur", "ya", "lekin", "parantu", "kyunki", "jab", "tab", "agar", "magar", 
    "phir", "fir", "ab", "aaj", "kal", "ek", "do", "ye", "yeh", "wo", "woh", 
    "us", "un", "in", "is", "jaisa", "waisa", "kuch", "koi", "sab", "bahut", 
    "bht", "kam", "jyada", "zyada", "mujhe", "mera", "meri", "mere", "tujhe", 
    "tera", "teri", "tere", "usko", "uska", "uski", "uske", "unko", "unka", 
    "unki", "unke", "hum", "hume", "hamara", "hamari", "hamare", "aap", "aapko", 
    "aapka", "aapki", "aapke", "tum", "tumko", "tumhara", "tumhari", "tumhare", 
    "tu", "yaar", "bhai", "bro", "sir", "madam", "mam", "ji", "acha", "accha", 
    "thik", "theek", "sahi", "galat", "karo", "karna", "kar", "raha", "rahi", 
    "rahe", "hona", "hua", "hui", "hue", "gaya", "gayi", "gaye", "aaya", "aayi", 
    "aaye", "diya", "diyi", "diye", "liya", "liyi", "liye", "tha", "thi", "the", 
    "hoga", "hogi", "hoge", "chahiye", "chuka", "chuki", "chuke", "wala", "wali", 
    "wale", "lol", "lmao", "rofl", "omg", "wtf", "idk", "idc", "btw", "tbh", 
    "brb", "ttyl", "gn", "gm", "tc", "sd", "sweet", "dreams", "take", "care", 
    "good", "night", "morning", "evening", "afternoon", "hi", "hello", "hey", 
    "bye", "tata", "cya", "aur", "bta", "btao", "kuch", "nai", "kuchh", "bas",
    "de", "dega", "degi", "dena", "denge", "le", "lega", "legi", "lena", "lenge",
    "aa", "aana", "aayega", "aayegi", "aayenge", "ja", "jaana", "jayega", "jayegi",
    "khud", "khudko", "apna", "apne", "apni", "kya", "kaisa", "kaisi", "kaise"
}

CONFLICT_LEXICON = {
    "hate", "angry", "stupid", "idiot", "dumb", "shut", "up", "hell", "damn", "bs", 
    "wtf", "wtf is", "nonsense", "bullshit", "crazy", "insane", "mad", "furious", 
    "pissed", "annoyed", "irritated", "frustrated", "sick", "tired", "worst", "awful", 
    "terrible", "disgusting", "horrible", "pathetic", "loser", "jerk", "moron", "fool",
    "stfu", "gtfo", "lmao", "fake", "liar", "lie", "lying", "cheat", "cheating", 
    "betray", "betrayal", "argue", "arguing", "argument", "fight", "fighting", "stop",
    "don't", "never", "ruin", "ruined", "trash", "garbage", "waste", "useless", 
    "pointless", "meaningless", "ridiculous", "absurd", "lame", "sucks", "suck",
    "bakwas", "pagal", "gussa", "kutta", "kamine", "bewakoof", "gadha", "chup", 
    "bhaad", "mar", "marna", "marta", "khatam", "barbaad", "galeech", "shutup"
}

POLITENESS_LEXICON = {
    "please", "pls", "plz", "thank", "thanks", "thankyou", "appreciate", "kind", 
    "kindly", "welcome", "welcome", "grateful", "sorry", "apologies", "excuse", 
    "pardon", "sir", "maam", "madam", "respect", "glad", "happy to", "would you",
    "could you", "may i", "shukriya", "dhanyawad", "kripya", "maaf"
}

LAUGHTER_LEXICON = {
    "haha", "hahaha", "hahahaha", "lol", "lmao", "rofl", "lmfao", "xd", "hehe", 
    "hehehe", "hihi", "jaja", "jajaja", "kek", "kekw", "kekek", "lolz"
}

TOPIC_LEXICONS = {
    "Work & Business": {
        "work", "job", "office", "meeting", "boss", "manager", "client", "project", 
        "deadline", "task", "presentation", "report", "email", "mail", "resume", 
        "interview", "salary", "promotion", "business", "company", "colleague", 
        "team", "shift", "schedule", "leave", "holiday", "vacation", "wfh", "remote",
        "kaam", "office", "boss", "chutti", "salary", "paisa", "meeting"
    },
    "Finance & Money": {
        "money", "cash", "bank", "account", "transfer", "pay", "paid", "payment", 
        "bill", "invoice", "receipt", "tax", "taxes", "loan", "debt", "credit", 
        "debit", "card", "invest", "investment", "stock", "shares", "crypto", 
        "bitcoin", "budget", "expense", "cost", "price", "buy", "sell", "purchase",
        "paisa", "paise", "rupee", "rupees", "kharcha", "udhaar", "bank", "paytm", "gpay", "upi"
    },
    "Technology & Software": {
        "code", "coding", "programming", "software", "hardware", "computer", "pc", 
        "laptop", "phone", "mobile", "app", "website", "server", "database", "cloud", 
        "internet", "wifi", "network", "bug", "error", "fix", "update", "install", 
        "download", "upload", "file", "folder", "link", "url", "password", "login",
        "python", "java", "javascript", "html", "css", "react", "node", "git", "api"
    },
    "Social & Relationships": {
        "friend", "friends", "family", "mom", "dad", "brother", "sister", "wife", 
        "husband", "girlfriend", "boyfriend", "gf", "bf", "love", "miss", "hug", 
        "kiss", "date", "meet", "hangout", "party", "celebrate", "birthday", "bday", 
        "anniversary", "wedding", "marriage", "relationship", "together", "forever",
        "yaar", "dost", "bhai", "behen", "maa", "papa", "shaadi", "pyaar", "ishq", "mohabbat"
    },
    "Entertainment & Media": {
        "movie", "movies", "film", "cinema", "show", "series", "season", "episode", 
        "watch", "watching", "video", "youtube", "netflix", "amazon", "prime", 
        "music", "song", "songs", "listen", "listening", "spotify", "game", "games", 
        "gaming", "play", "playing", "ps5", "xbox", "pc", "stream", "streaming",
        "picture", "gaana", "gaane", "khel", "khelna", "match", "cricket", "football"
    },
    "Urgent & Important": {
        "urgent", "important", "emergency", "asap", "now", "quick", "quickly", 
        "fast", "hurry", "rush", "help", "help me", "call", "call me", "answer", 
        "reply", "respond", "wait", "waiting", "stop", "danger", "alert", "warning",
        "jaldi", "abhi", "turant", "emergency", "madad", "bachao", "phone utha", "reply kar"
    }
}

EMOTION_LEXICON = {
    "Joy & Happiness": {
        "happy", "glad", "great", "awesome", "excellent", "amazing", "wonderful", "fantastic", "yay", "yayy", 
        "woohoo", "cheers", "blessed", "delighted", "thrilled", "beautiful", "perfect", "good", "nice", "cool", 
        "sweet", "fun", "enjoy", "smile", "laugh", "haha", "lmao", "lol", "rofl", "xd", "hilarious", "funny",
        "brilliant", "marvelous", "fabulous", "splendid", "superb", "outstanding", "joy", "joyful", "ecstatic",
        "proud", "triumph", "victorious", "win", "won", "winning", "success", "successful", "luck", "lucky",
        "khush", "maza", "badhiya", "mast", "zabardast", "jhakas", "sukoon", "shanti"
    },
    "Sadness & Sorrow": {
        "sad", "depressed", "down", "unhappy", "cry", "crying", "tears", "heartbroken", "devastated", "miserable", 
        "sorrow", "grief", "tragic", "terrible", "awful", "bad", "worst", "unfortunately", "regret", "miss", 
        "missing", "lonely", "alone", "hurt", "pain", "sorry", "apologies", "apologize", "grief", "grieving",
        "mourn", "mourning", "loss", "lost", "fail", "failed", "failure", "disappointed", "disappointing",
        "gloomy", "melancholy", "tragic", "tragedy", "pity", "shame", "unfortunate",
        "dukhi", "rona", "dard", "takleef", "akela", "akeli", "udas", "nirash", "bura"
    },
    "Anger & Frustration": {
        "angry", "mad", "furious", "annoyed", "irritated", "frustrated", "rage", "hate", "hating", "disgusting", 
        "stupid", "idiot", "dumb", "fool", "crazy", "hell", "damn", "bs", "wtf", "pissed", "angry", "annoying", 
        "bother", "bothering", "upset", "outrageous", "terrible", "fuming", "livid", "infuriated", "infuriating",
        "wrath", "resentment", "resent", "bitter", "bitterness", "hostile", "hostility", "agitated", "aggravated",
        "gussa", "pagal", "bakwas", "dimag kharab", "kutta", "kamine", "bewakoof"
    },
    "Fear & Anxiety": {
        "scared", "terrified", "afraid", "fear", "panic", "panicking", "nervous", "anxious", "worried", "worry", 
        "worrying", "stress", "stressed", "creepy", "spooky", "horrifying", "horrible", "dread", "dreadful", 
        "threat", "threatened", "danger", "dangerous", "frightened", "frightening", "alarmed", "alarming",
        "terror", "horror", "appalled", "appalling", "uneasy", "uneasiness", "tense", "tension",
        "dar", "darna", "darr", "tension", "chinta", "ghabrahat", "pareshaan"
    },
    "Love & Affection": {
        "love", "loving", "heart", "xoxo", "kisses", "hugs", "babe", "baby", "darling", "sweetheart", "honey", 
        "dear", "adorable", "cute", "handsome", "gorgeous", "beautiful", "passion", "romantic", "romance", 
        "affection", "care", "caring", "miss you", "love you", "beloved", "cherish", "cherished", "adore",
        "adored", "infatuated", "fond", "fondness", "devotion", "devoted", "soulmate",
        "pyaar", "ishq", "mohabbat", "jaan", "jaanu", "babu", "shona", "dil"
    },
    "Surprise & Shock": {
        "wow", "omg", "woah", "whoa", "surprised", "shocked", "shocking", "unexpected", "unbelievable", "crazy", 
        "insane", "wild", "gasp", "astonishing", "astounded", "speechless", "kidding", "really", "seriously",
        "startled", "startling", "stunned", "stunning", "amazed", "amazing", "dumbfounded", "flabbergasted",
        "mind-blowing", "mindblown", "whoops", "oops",
        "kya", "sach", "sachme", "are baap re", "oh teri", "hairan", "shock"
    }
}

EMOJI_DICTIONARY = {
    "😂": "Face with Tears of Joy", "😭": "Loudly Crying Face", "🥺": "Pleading Face", 
    "🤣": "Rolling on the Floor Laughing", "❤️": "Red Heart", "✨": "Sparkles", 
    "😍": "Smiling Face with Heart-Eyes", "🙏": "Folded Hands", "😊": "Smiling Face with Smiling Eyes", 
    "🥰": "Smiling Face with Hearts", "👍": "Thumbs Up", "💕": "Smiling Face with Hearts", 
    "🤔": "Thinking Face", "😘": "Face Blowing a Kiss", "🔥": "Fire", 
    "🙂": "Smiling Face", "🤦‍♂️": "Man Facepalming", "🤦‍♀️": "Woman Facepalming", 
    "🙄": "Face with Rolling Eyes", "🤷‍♂️": "Man Shrugging", "🤷‍♀️": "Woman Shrugging", 
    "🙌": "Raising Hands", "😉": "Winking Face", "🎉": "Party Popper", 
    "😎": "Smiling Face with Sunglasses", "😔": "Pensive Face", "👀": "Face with Peeking Eyes", 
    "😅": "Grinning Face with Sweat", "💯": "Hundred Points", "🎶": "Musical Notes", 
    "👏": "Clapping Hands", "😁": "Grinning Face with Smiling Eyes", "💖": "Two Hearts", 
    "🎂": "Birthday Cake", "🎈": "Party Balloon", "✌️": "Raising Hands", 
    "👌": "OK Hand", "😜": "Winking Face with Tongue", "🙈": "See-No-Evil Monkey"
}

COMMON_DOMAINS = {
    "youtube.com": "YouTube", "youtu.be": "YouTube", "instagram.com": "Instagram",
    "twitter.com": "Twitter", "x.com": "Twitter", "facebook.com": "Facebook", "fb.com": "Facebook",
    "tiktok.com": "TikTok", "linkedin.com": "LinkedIn", "amazon.": "Amazon", "amzn.to": "Amazon",
    "spotify.com": "Spotify", "maps.google": "Google Maps", "drive.google": "Google Drive",
    "zoom.us": "Zoom", "meet.google": "Google Meet", "github.com": "GitHub",
    "reddit.com": "Reddit", "pinterest.com": "Pinterest", "snapchat.com": "Snapchat",
    "whatsapp.com": "WhatsApp", "telegram.org": "Telegram", "discord.gg": "Discord",
    "discord.com": "Discord", "twitch.tv": "Twitch", "netflix.com": "Netflix",
    "hulu.com": "Hulu", "disneyplus.com": "Disney+", "primevideo.com": "Prime Video",
    "apple.com": "Apple", "microsoft.com": "Microsoft", "google.com": "Google",
    "yahoo.com": "Yahoo", "bing.com": "Bing", "wikipedia.org": "Wikipedia",
    "quora.com": "Quora", "medium.com": "Medium", "stackoverflow.com": "Stack Overflow",
    "nytimes.com": "The New York Times", "cnn.com": "CNN", "bbc.co.uk": "BBC",
    "bbc.com": "BBC", "theguardian.com": "The Guardian", "washingtonpost.com": "The Washington Post",
    "wsj.com": "Wall Street Journal", "forbes.com": "Forbes", "bloomberg.com": "Bloomberg",
    "businessinsider.com": "Business Insider", "cnbc.com": "CNBC", "reuters.com": "Reuters"
}

# ==============================================================================
# CONFIGURATION & THEMES (Minimalist Corporate Restyle)
# ==============================================================================

class Theme:
    """Manages Colors and Visuals for the entire application. Professional MNC Style."""
    CONFIG_FILE = Path("enterprise_config.json")
    
    THEMES = {
        "Executive Light": {
            "BG_MAIN": "#F8FAFC", "BG_SURFACE": "#FFFFFF", "BG_SIDEBAR": "#F1F5F9",
            "ACCENT": "#2563EB", "ACCENT_HOVER": "#1D4ED8", "TEXT_WHITE": "#0F172A",
            "TEXT_GRAY": "#64748B", "BORDER": "#E2E8F0", "PLOT_STYLE": "default",
            "PLOT_PALETTE": "Blues", "ERROR": "#DC2626", "SUCCESS": "#059669"
        }
    }
    
    APP_FONTS = [
        "Segoe UI", "Helvetica Neue", "Arial", "Roboto", "Inter",
        "San Francisco", "Verdana", "Tahoma", "Trebuchet MS", "Georgia"
    ]
    
    current = THEMES["Executive Light"]
    current_font = "Segoe UI"
    
    @classmethod
    def set_theme(cls, theme_name):
        if theme_name in cls.THEMES:
            cls.current = cls.THEMES[theme_name]
            
    @classmethod
    def set_font(cls, font_name):
        if font_name in cls.APP_FONTS:
            cls.current_font = font_name

    @classmethod
    def load_config(cls):
        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    if "theme" in data and data["theme"] in cls.THEMES:
                        cls.set_theme(data["theme"])
                    if "font" in data and data["font"] in cls.APP_FONTS:
                        cls.set_font(data["font"])
            except Exception:
                pass

    @classmethod
    def save_config(cls, theme_name, font_name):
        try:
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump({"theme": theme_name, "font": font_name}, f)
        except Exception:
            pass

# ==============================================================================
# UTILITY HELPERS
# ==============================================================================

def wrap_text(text, width=60):
    if not isinstance(text, str): text = str(text)
    return "\n".join(textwrap.wrap(text, width=width))

def clean_word(word: str) -> str:
    return word.strip(string.punctuation + " \n\r\t").lower()

def is_url(text: str) -> bool:
    pattern = r'(https?://\S+)|(www\.\S+)'
    return re.search(pattern, text) is not None

def extract_domain(text: str) -> str:
    match = re.search(r'https?://(?:www\.)?([^/]+)', text)
    if match: return match.group(1)
    match = re.search(r'www\.([^/]+)', text)
    if match: return match.group(1)
    return ""

def adjust_color(hex_color, factor=1.1):
    """Lighten or darken a hex color string for subtle hover effects."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6: return '#' + hex_color
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    r = min(int(r * factor), 255)
    g = min(int(g * factor), 255)
    b = min(int(b * factor), 255)
    return f"#{r:02x}{g:02x}{b:02x}"

def export_plot_to_png(fig, title="plot"):
    path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=f"{title}_{int(time.time())}.png", filetypes=[("PNG", "*.png")])
    if path:
        try:
            fig.savefig(path, bbox_inches='tight', dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
            messagebox.showinfo("Success", f"Plot saved to {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save plot: {e}")

def apply_modern_plot_style(ax, title, xlabel="", ylabel=""):
    """Applies modern, borderless, minimalist styling to a matplotlib axis."""
    ax.set_title(title, color=Theme.current["TEXT_WHITE"], pad=15, fontsize=12, fontweight='normal', loc='left')
    ax.set_xlabel(xlabel, color=Theme.current["TEXT_GRAY"], fontsize=11)
    ax.set_ylabel(ylabel, color=Theme.current["TEXT_GRAY"], fontsize=11)
    ax.tick_params(colors=Theme.current["TEXT_GRAY"], labelsize=10, length=0)
    
    # Remove all spines for an ultra-clean corporate look
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Very subtle grid
    ax.grid(True, axis='y', linestyle='-', alpha=0.05, color=Theme.current["TEXT_GRAY"])

# ==============================================================================
# CUSTOM WIDGETS (Minimalist Corporate UI Elements)
# ==============================================================================

class ScrollableFrame(tk.Frame):
    """A highly reusable minimalist scrollable container for expanding dashboard tabs."""
    def __init__(self, parent, *args, **kwargs):
        # Extract bg color if provided, else fallback to current theme
        bg_color = kwargs.pop('bg', Theme.current["BG_MAIN"])
        kwargs['bg'] = bg_color
        
        super().__init__(parent, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg=bg_color, highlightthickness=0)
        
        # Minimalist scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_container = tk.Frame(self.canvas, bg=bg_color)

        self.scrollable_container.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_container, anchor="nw")

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Mousewheel binding
        self.bind_all("<MouseWheel>", self._on_mousewheel)
        # Linux mousewheel support
        self.bind_all("<Button-4>", self._on_mousewheel)
        self.bind_all("<Button-5>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        # Only scroll if the cursor is currently over this specific widget's toplevel to avoid cross-scrolling
        try:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
            else:
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except Exception:
            pass

    def update_theme_colors(self):
        bg_color = Theme.current["BG_MAIN"]
        self.configure(bg=bg_color)
        self.canvas.configure(bg=bg_color)
        self.scrollable_container.configure(bg=bg_color)

class NavTab(tk.Frame):
    """Custom flat navigation tab for SaaS layout"""
    def __init__(self, parent, text, command):
        super().__init__(parent, bg=Theme.current["BG_MAIN"])
        self.command = command
        self.text = text
        self.lbl = tk.Label(self, text=text, font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"], cursor="hand2")
        self.lbl.pack(pady=(8, 6), padx=12)
        self.indicator = tk.Frame(self, bg=Theme.current["BG_MAIN"], height=2)
        self.indicator.pack(fill="x", side="bottom")
        
        self.lbl.bind("<Button-1>", self.on_click)
        self.lbl.bind("<Enter>", self.on_hover)
        self.lbl.bind("<Leave>", self.on_leave)
        self.active = False
        
    def on_click(self, e):
        self.command(self.text)
        
    def on_hover(self, e):
        if not self.active:
            self.lbl.config(fg=Theme.current["TEXT_WHITE"])
            
    def on_leave(self, e):
        if not self.active:
            self.lbl.config(fg=Theme.current["TEXT_GRAY"])
            
    def set_active(self, active):
        self.active = active
        if active:
            self.lbl.config(fg=Theme.current["ACCENT"])
            self.indicator.config(bg=Theme.current["ACCENT"])
        else:
            self.lbl.config(fg=Theme.current["TEXT_GRAY"])
            self.indicator.config(bg=Theme.current["BG_MAIN"])

    def update_theme_colors(self):
        self.configure(bg=Theme.current["BG_MAIN"])
        self.lbl.configure(bg=Theme.current["BG_MAIN"], font=(Theme.current_font, 10, "bold"))
        if self.active:
            self.lbl.configure(fg=Theme.current["ACCENT"])
            self.indicator.configure(bg=Theme.current["ACCENT"])
        else:
            self.lbl.configure(fg=Theme.current["TEXT_GRAY"])
            self.indicator.configure(bg=Theme.current["BG_MAIN"])

class FlatNavButton(tk.Frame):
    """A flat action button styled identically to the NavTab, maintaining high contrast."""
    def __init__(self, parent, text, command, anchor="center"):
        # Force background to match the absolute background (BG_MAIN) for contrast
        self.bg_color = Theme.current["BG_MAIN"]
        super().__init__(parent, bg=self.bg_color)
        self.command = command
        self.text = text
        
        # Determine padding and layout based on anchor
        pack_opts = {"pady": (6, 4), "padx": 12, "anchor": anchor}
        if anchor == "w": pack_opts["padx"] = (25, 12)
        
        # Force foreground to bright TEXT_WHITE for excellent legibility
        self.lbl = tk.Label(self, text=text, font=(Theme.current_font, 9, "bold"), bg=self.bg_color, fg=Theme.current["TEXT_WHITE"], cursor="hand2")
        self.lbl.pack(**pack_opts)
        
        self.indicator = tk.Frame(self, bg=self.bg_color, height=2)
        self.indicator.pack(fill="x", side="bottom")
        
        self.lbl.bind("<Button-1>", self.on_click)
        self.lbl.bind("<Enter>", self.on_hover)
        self.lbl.bind("<Leave>", self.on_leave)
        
    def on_click(self, e):
        self.lbl.config(fg=Theme.current["TEXT_WHITE"])
        if self.command:
            self.after(50, self.command)
            
    def on_hover(self, e):
        self.lbl.config(fg=Theme.current["ACCENT"])
        self.indicator.config(bg=Theme.current["ACCENT"])
        
    def on_leave(self, e):
        self.lbl.config(fg=Theme.current["TEXT_WHITE"])
        self.indicator.config(bg=self.bg_color)

    def update_theme_colors(self):
        self.bg_color = Theme.current["BG_MAIN"]
        self.configure(bg=self.bg_color)
        self.lbl.configure(bg=self.bg_color, font=(Theme.current_font, 9, "bold"), fg=Theme.current["TEXT_WHITE"])
        self.indicator.configure(bg=self.bg_color)

class RoundedButton(tk.Canvas):
    """A custom, minimalist button built using Tkinter Canvas. (Radius=6 for SaaS look)"""
    def __init__(self, parent, text, command=None, radius=6, bg=None, fg=None, hover_bg=None, width=150, height=36, font=None, **kwargs):
        super().__init__(parent, width=width, height=height, bg=Theme.current["BG_MAIN"], highlightthickness=0, **kwargs)
        
        self.command = command
        self.radius = radius
        self.text = text
        self.is_custom_bg = bool(bg)
        self.is_custom_fg = bool(fg)
        
        self.bg_color = bg or Theme.current["ACCENT"]
        # Always use white font for accent buttons, fallback to provided custom colors
        self.fg_color = fg or "#FFFFFF"
            
        self.hover_bg = hover_bg or adjust_color(self.bg_color, 1.1)
        self.pressed_bg = adjust_color(self.bg_color, 0.9)
        self.font = font or (Theme.current_font, 9)
        
        # To match exact background of parent gracefully
        self.parent_bg = parent.cget("bg") if hasattr(parent, 'cget') else Theme.current["BG_MAIN"]
        self.configure(bg=self.parent_bg)
        
        self.rect = self._create_rounded_rect(1, 1, width-1, height-1, radius, fill=self.bg_color, outline="")
        self.text_id = self.create_text(width/2, height/2, text=self.text, fill=self.fg_color, font=self.font, justify="center")
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        
    def _create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
            x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
            x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
            x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
            x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
        
    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.hover_bg)
        self.config(cursor="hand2")
        
    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.bg_color)
        self.config(cursor="")
        
    def on_press(self, event):
        self.itemconfig(self.rect, fill=self.pressed_bg)
        
    def on_release(self, event):
        self.itemconfig(self.rect, fill=self.hover_bg)
        if self.command:
            self.after(50, self.command) # slight delay for visual feedback

    def update_theme_colors(self):
        """Allows dynamic refreshing of button colors without restarting app."""
        if not self.is_custom_bg:
            self.bg_color = Theme.current["ACCENT"]
            self.hover_bg = adjust_color(self.bg_color, 1.1)
            self.pressed_bg = adjust_color(self.bg_color, 0.9)
            self.itemconfig(self.rect, fill=self.bg_color)
            
        if not self.is_custom_fg:
            self.fg_color = "#FFFFFF"
            self.itemconfig(self.text_id, fill=self.fg_color, font=(Theme.current_font, self.font[1]))
            
        self.parent_bg = self.master.cget("bg") if hasattr(self.master, 'cget') else Theme.current["BG_MAIN"]
        self.configure(bg=self.parent_bg)

class InfoCard(tk.Frame):
    """A Modern SaaS KPI Card with minimalist layout."""
    def __init__(self, parent, title, icon="📊", width=180, height=80):
        super().__init__(
            parent,
            bg=Theme.current["BG_SURFACE"],
            highlightbackground=Theme.current["BORDER"],
            highlightthickness=1,
            padx=15,
            pady=10
        )
        self.pack_propagate(False)
        self.configure(width=width, height=height)

        # Left accent line using a thin frame
        self.accent = tk.Frame(self, bg=Theme.current["ACCENT"], width=3)
        self.accent.place(relx=0, rely=0, relheight=1)

        header_frame = tk.Frame(self, bg=Theme.current["BG_SURFACE"])
        header_frame.pack(fill="x")
        
        self.lbl_title = tk.Label(header_frame, text=f"{title}", font=(Theme.current_font, 8), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], anchor="w")
        self.lbl_title.pack(side="left")
        
        if icon:
            self.lbl_icon = tk.Label(header_frame, text=icon, font=(Theme.current_font, 9), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], anchor="e")
            self.lbl_icon.pack(side="right")
        else:
            self.lbl_icon = None

        self.lbl_value = tk.Label(self, text="0", font=(Theme.current_font, 18, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"], anchor="w")
        self.lbl_value.pack(fill="x", pady=(4, 0))

        self.lbl_sub = tk.Label(self, text="", font=(Theme.current_font, 8), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], anchor="w")
        self.lbl_sub.pack(fill="x")

    def update_value(self, value, subtitle: str = ""):
        self.lbl_value.config(text=str(value))
        self.lbl_sub.config(text=str(subtitle))

    def update_theme_colors(self):
        """Dynamically applies updated themes to all subcomponents."""
        self.configure(bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"])
        self.accent.configure(bg=Theme.current["ACCENT"])
        
        for child in self.winfo_children():
            if isinstance(child, tk.Frame) and child != self.accent:
                child.configure(bg=Theme.current["BG_SURFACE"])
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Label):
                        grandchild.configure(bg=Theme.current["BG_SURFACE"])
                        
        self.lbl_title.configure(bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], font=(Theme.current_font, 8))
        if self.lbl_icon:
            self.lbl_icon.configure(bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], font=(Theme.current_font, 9))
        self.lbl_value.configure(bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"], font=(Theme.current_font, 18, "bold"))
        self.lbl_sub.configure(bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], font=(Theme.current_font, 8))

# ==============================================================================
# LOGIC: HIGH-FAULT-TOLERANCE PARSER
# ==============================================================================

class ChatParser:
    """
    Handles raw text parsing into structured DataFrames.
    Extremely robust multi-pass regex to handle global WhatsApp export formats.
    """
    
    PATTERNS = [
        r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}(?:\s?[aApP][mM])?)\s+-\s+(.*)$',
        r'^\[(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}:\d{2}(?:\s?[aApP][mM])?)\]\s+(.*)$',
        r'^(\d{2,4}/\d{1,2}/\d{1,2}),\s+(\d{1,2}:\d{2}(?:\s?[aApP][mM])?)\s+-\s+(.*)$',
        r'^(\d{4}-\d{1,2}-\d{1,2}),\s+(\d{1,2}:\d{2}(?:\s?[aApP][mM])?)\s+-\s+(.*)$'
    ]

    @staticmethod
    def parse_file(filepath):
        data = []
        encodings = ['utf-8-sig', 'utf-8', 'utf-16', 'latin-1', 'cp1252']
        lines = []
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    lines = f.readlines()
                if lines: break
            except: continue

        if not lines: raise ValueError("Could not read file with any standard encoding.")

        message_buffer = []
        date, time_str, sender = None, None, None

        for raw_line in lines:
            line = raw_line.rstrip("\n")
            stripped = line.strip()
            if not stripped: continue
            
            match = None
            for pat in ChatParser.PATTERNS:
                match = re.match(pat, stripped)
                if match: break

            if match:
                if message_buffer:
                    data.append([date, time_str, sender, '\n'.join(message_buffer)])
                    message_buffer = []

                date, time_str, rest = match.groups()
                if ": " in rest:
                    sender, msg = rest.split(": ", 1)
                    message_buffer.append(msg)
                else:
                    sender = "System Notification"
                    message_buffer.append(rest)
            else:
                if message_buffer: message_buffer.append(stripped)

        if message_buffer: data.append([date, time_str, sender, '\n'.join(message_buffer)])

        df = pd.DataFrame(data, columns=['date', 'time', 'sender', 'message'])
        if df.empty: return df

        # Robust Datetime Conversion
        df['datetime_str'] = df['date'] + ' ' + df['time']
        
        # Try multiple parsing strategies safely suppressing dateutil fallback warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            try:
                # Pandas >= 2.0 prefers explicit format='mixed'
                df['datetime'] = pd.to_datetime(df['datetime_str'], dayfirst=True, format='mixed', errors='coerce')
                missing = df['datetime'].isna()
                if missing.any():
                    df.loc[missing, 'datetime'] = pd.to_datetime(df.loc[missing, 'datetime_str'], dayfirst=False, format='mixed', errors='coerce')
            except (ValueError, TypeError):
                # Fallback for older Pandas versions (< 2.0)
                df['datetime'] = pd.to_datetime(df['datetime_str'], dayfirst=True, errors='coerce')
                missing = df['datetime'].isna()
                if missing.any():
                    df.loc[missing, 'datetime'] = pd.to_datetime(df.loc[missing, 'datetime_str'], dayfirst=False, errors='coerce')
        
        df.dropna(subset=['datetime'], inplace=True)

        df['year'] = df['datetime'].dt.year
        df['month_num'] = df['datetime'].dt.month
        df['month'] = df['datetime'].dt.month_name()
        df['day'] = df['datetime'].dt.day
        df['day_name'] = df['datetime'].dt.day_name()
        df['hour'] = df['datetime'].dt.hour
        df['minute'] = df['datetime'].dt.minute
        df['only_date'] = df['datetime'].dt.date

        df['message'] = df['message'].astype(str)
        df['word_count'] = df['message'].apply(lambda x: len(str(x).split()))
        df['char_count'] = df['message'].apply(len)
        df['is_media'] = df['message'].str.contains(r'<Media omitted>|image omitted|video omitted|sticker omitted|audio omitted', case=False)
        df['is_deleted'] = df['message'].str.contains(r'This message was deleted|You deleted this message', case=False)
        df['has_link'] = df['message'].apply(is_url)
        df['domain'] = df['message'].apply(lambda x: extract_domain(x) if is_url(x) else "")
        
        df['is_question'] = df['message'].str.contains(r'\?', regex=True)
        df['is_laughter'] = df['message'].str.lower().str.contains(r'\bhaha|\blol|\blmao|\brofl|\bhehe|😂|🤣', regex=True)
        df['is_polite'] = df['message'].str.lower().str.contains(r'\bplease\b|\bpls\b|\bthanks\b|\bthank you\b|\bwelcome\b', regex=True)

        return df

class AdvancedAnalyzer:
    """Performs heavy lifting for statistics, emotions, topics, and response times."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.all_stopwords = STOPWORDS_EN.union(STOPWORDS_HINDI_HINGLISH)

    def get_basic_stats(self):
        if self.df.empty: return {}
        start_date = self.df['only_date'].min()
        end_date = self.df['only_date'].max()
        days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days + 1 if pd.notna(start_date) and pd.notna(end_date) else 0
        avg_per_day = round(self.df.shape[0] / days, 2) if days > 0 else 0
        
        real_df = self.df[self.df['sender'] != 'System Notification']
        avg_words_overall = round(real_df['word_count'].mean(), 2) if not real_df.empty else 0
        peak_hour = self.df['hour'].mode().iloc[0] if not self.df.empty else 0

        return {
            "total_msgs": self.df.shape[0],
            "total_words": int(self.df['word_count'].sum()),
            "media_count": int(self.df['is_media'].sum()),
            "deleted_count": int(self.df['is_deleted'].sum()),
            "links_count": int(self.df['has_link'].sum()),
            "users": int(real_df['sender'].nunique()),
            "start_date": start_date,
            "end_date": end_date,
            "days": days,
            "avg_per_day": avg_per_day,
            "avg_words_overall": avg_words_overall,
            "peak_hour": f"{peak_hour}:00"
        }

    def fetch_monthly_timeline(self):
        timeline = self.df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
        timeline['time'] = timeline['month'].astype(str).str[:3] + " " + timeline['year'].astype(str).str[-2:]
        return timeline

    def fetch_activity_heatmap(self):
        activity = self.df.pivot_table(index='day_name', columns='hour', values='message', aggfunc='count').fillna(0)
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        activity = activity.reindex(days_order)
        return activity

    def fetch_hourly_activity(self):
        hourly = self.df.groupby('hour').count()['message'].reset_index()
        hourly.rename(columns={'message': 'count'}, inplace=True)
        return hourly

    def fetch_weekday_activity(self):
        weekday = self.df.groupby('day_name').count()['message'].reset_index()
        ordering = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday['day_name'] = pd.Categorical(weekday['day_name'], categories=ordering, ordered=True)
        weekday.sort_values('day_name', inplace=True)
        weekday.rename(columns={'message': 'count'}, inplace=True)
        return weekday

    def fetch_top_users(self, n=10):
        df_real = self.df[self.df['sender'] != 'System Notification']
        return df_real['sender'].value_counts().head(n)

    def fetch_user_stats(self):
        df_real = self.df[self.df['sender'] != 'System Notification']
        grouped = df_real.groupby('sender').agg(
            messages=('message', 'count'),
            words=('word_count', 'sum'),
            media=('is_media', 'sum'),
            deleted=('is_deleted', 'sum'),
            links=('has_link', 'sum'),
            questions=('is_question', 'sum'),
            laughs=('is_laughter', 'sum'),
            polite=('is_polite', 'sum')
        ).reset_index()
        grouped['avg_words_per_msg'] = (grouped['words'] / grouped['messages']).round(2)
        return grouped.sort_values(by='messages', ascending=False)

    def fetch_message_type_distribution(self):
        """Returns distribution of Text vs Media vs Links."""
        if self.df.empty: return {}
        media = int(self.df['is_media'].sum())
        links = int(self.df['has_link'].sum())
        text = int(self.df.shape[0] - media - links)
        # Ensure non-negative if a message is both link and media
        text = max(0, text)
        return {"Text Only": text, "Media": media, "Links": links}

    def fetch_engagement_stats(self):
        """Calculate Response Times, Conversation Starters, Double Texting, and Max Silence broken."""
        df_real = self.df[self.df['sender'] != 'System Notification'].sort_values('datetime').reset_index(drop=True)
        if df_real.empty: return pd.DataFrame()
        
        df_real['time_diff'] = df_real['datetime'].diff().dt.total_seconds() / 60.0
        df_real['prev_sender'] = df_real['sender'].shift(1)
        df_real['is_starter'] = df_real['time_diff'] > 480
        
        responses = df_real[(df_real['sender'] != df_real['prev_sender']) & (df_real['time_diff'] < 60) & (df_real['time_diff'] > 0)]
        
        # New features: Avg messages per turn and Max silence broken
        df_real['is_new_turn'] = df_real['sender'] != df_real['prev_sender']
        df_real.loc[0, 'is_new_turn'] = True # First message is always a new turn
        
        stats = []
        for user in df_real['sender'].unique():
            user_msgs = df_real[df_real['sender'] == user]
            user_responses = responses[responses['sender'] == user]
            
            avg_response_time = user_responses['time_diff'].mean() if not user_responses.empty else 0
            starters = user_msgs[user_msgs['is_starter']].shape[0]
            
            turns = user_msgs['is_new_turn'].sum()
            msgs_per_turn = user_msgs.shape[0] / turns if turns > 0 else 1
            
            user_starts = user_msgs[(user_msgs['is_new_turn']) & (user_msgs['time_diff'].notna())]
            max_silence = (user_starts['time_diff'].max() / 60.0) if not user_starts.empty else 0
            
            stats.append({
                "Sender": user, 
                "Avg Response Time (min)": round(avg_response_time, 2), 
                "Conversation Starters": starters,
                "Avg Msgs/Turn": round(msgs_per_turn, 2),
                "Max Silence Broken (hrs)": round(max_silence, 1)
            })
            
        return pd.DataFrame(stats).sort_values("Conversation Starters", ascending=False)

    def fetch_night_owls_early_birds(self):
        df_real = self.df[self.df['sender'] != 'System Notification']
        if df_real.empty: return pd.DataFrame()
        night_owls = df_real[(df_real['hour'] >= 0) & (df_real['hour'] < 5)]
        early_birds = df_real[(df_real['hour'] >= 5) & (df_real['hour'] < 10)]
        night_counts = night_owls['sender'].value_counts().to_dict()
        early_counts = early_birds['sender'].value_counts().to_dict()
        stats = []
        for user in df_real['sender'].unique():
            stats.append({
                "Sender": user, "Night Owl Msgs (12AM-5AM)": night_counts.get(user, 0), "Early Bird Msgs (5AM-10AM)": early_counts.get(user, 0)
            })
        return pd.DataFrame(stats).sort_values("Night Owl Msgs (12AM-5AM)", ascending=False)

    def fetch_emoji_stats(self, top_n=15):
        emojis = []
        for message in self.df['message']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        counter = Counter(emojis).most_common(top_n)
        translated = []
        for em, count in counter:
            meaning = EMOJI_DICTIONARY.get(em, "Unknown Emoji")
            translated.append((em, meaning, count))
        return translated

    def fetch_word_frequency(self, top_n=40, include_stopwords=False):
        words = []
        for msg in self.df[~self.df['is_media']]['message']:
            for raw_word in str(msg).split():
                w = clean_word(raw_word)
                if not w or len(w) <= 2: continue
                if not include_stopwords and w in self.all_stopwords: continue
                words.append(w)
        return Counter(words).most_common(top_n)

    def fetch_top_domains(self, top_n=10):
        domains = self.df[self.df['has_link']]['domain'].tolist()
        cleaned = []
        for d in domains:
            if not d: continue
            matched = False
            for k, v in COMMON_DOMAINS.items():
                if k in d:
                    cleaned.append(v)
                    matched = True
                    break
            if not matched: cleaned.append(d)
        return Counter(cleaned).most_common(top_n)

    def fetch_emotion_radar(self):
        emotion_counts = {k: 0 for k in EMOTION_LEXICON.keys()}
        for msg in self.df[~self.df['is_media']]['message']:
            words = set([clean_word(w) for w in str(msg).split()])
            for emotion, keywords in EMOTION_LEXICON.items():
                if words.intersection(keywords):
                    emotion_counts[emotion] += 1
        return emotion_counts

    def fetch_topic_distribution(self):
        topic_counts = {k: 0 for k in TOPIC_LEXICONS.keys()}
        for msg in self.df[~self.df['is_media']]['message']:
            words = set([clean_word(w) for w in str(msg).split()])
            for topic, keywords in TOPIC_LEXICONS.items():
                if words.intersection(keywords):
                    topic_counts[topic] += 1
        return topic_counts

    def fetch_conflict_data(self):
        """Returns comprehensive data about conflict and toxicity."""
        conflict_dates = defaultdict(int)
        conflict_senders = defaultdict(int)
        conflict_words = defaultdict(int)
        
        total_conflicts = 0
        
        for _, row in self.df[~self.df['is_media']].iterrows():
            words = [clean_word(w) for w in str(row['message']).split()]
            for w in words:
                if w in CONFLICT_LEXICON:
                    conflict_dates[str(row['only_date'])] += 1
                    if row['sender'] != 'System Notification':
                        conflict_senders[row['sender']] += 1
                    conflict_words[w] += 1
                    total_conflicts += 1
                    
        return {
            "total": total_conflicts,
            "timeline": sorted(conflict_dates.items()),
            "senders": sorted(conflict_senders.items(), key=lambda x: x[1], reverse=True),
            "words": sorted(conflict_words.items(), key=lambda x: x[1], reverse=True)[:15]
        }

    def fetch_longest_messages(self, top_n=5):
        """Finds the absolute longest single messages sent."""
        df_real = self.df[(self.df['sender'] != 'System Notification') & (~self.df['is_media'])]
        if df_real.empty: return []
        top_msgs = df_real.nlargest(top_n, 'word_count')[['datetime', 'sender', 'word_count', 'message']]
        return top_msgs.values.tolist()

    def fetch_lexicon_extras(self, top_n=10):
        """Extracts frequency of specific politeness and laughter markers."""
        polite_counter = Counter()
        laugh_counter = Counter()
        for msg in self.df[~self.df['is_media']]['message']:
            words = [clean_word(w) for w in str(msg).split()]
            for w in words:
                if w in POLITENESS_LEXICON: polite_counter[w] += 1
                if w in LAUGHTER_LEXICON: laugh_counter[w] += 1
        return {
            "polite": polite_counter.most_common(top_n),
            "laughs": laugh_counter.most_common(top_n)
        }

    def fetch_sentiment_detailed_stats(self):
        """Scores each participant and timeline node based on emotion subsets."""
        if self.df.empty: return {}
        
        pos_words = EMOTION_LEXICON["Joy & Happiness"].union(EMOTION_LEXICON["Love & Affection"])
        neg_words = EMOTION_LEXICON["Anger & Frustration"].union(EMOTION_LEXICON["Sadness & Sorrow"]).union(EMOTION_LEXICON["Fear & Anxiety"])
        
        user_sentiment = defaultdict(lambda: {"pos": 0, "neg": 0})
        timeline_sentiment = defaultdict(lambda: {"pos": 0, "neg": 0})
        
        total_pos = 0
        total_neg = 0
        
        for _, row in self.df[~self.df['is_media']].iterrows():
            if row['sender'] == 'System Notification': continue
            words = [clean_word(w) for w in str(row['message']).split()]
            
            p_count = sum(1 for w in words if w in pos_words)
            n_count = sum(1 for w in words if w in neg_words)
            
            if p_count > 0 or n_count > 0:
                user_sentiment[row['sender']]["pos"] += p_count
                user_sentiment[row['sender']]["neg"] += n_count
                
                # Use YYYY-MM formatting for smoother timelines
                month_key = row['datetime'].strftime('%Y-%m')
                timeline_sentiment[month_key]["pos"] += p_count
                timeline_sentiment[month_key]["neg"] += n_count
                
                total_pos += p_count
                total_neg += n_count
                
        most_pos_user = "N/A"
        most_neg_user = "N/A"
        max_pos_ratio = -1
        max_neg_ratio = -1
        
        for user, counts in user_sentiment.items():
            total = counts["pos"] + counts["neg"]
            if total > 5: # min threshold to avoid skewed 1-message stats
                p_ratio = counts["pos"] / total
                n_ratio = counts["neg"] / total
                if p_ratio > max_pos_ratio:
                    max_pos_ratio = p_ratio
                    most_pos_user = user
                if n_ratio > max_neg_ratio:
                    max_neg_ratio = n_ratio
                    most_neg_user = user
                    
        return {
            "total_pos": total_pos,
            "total_neg": total_neg,
            "net_score": total_pos - total_neg,
            "most_pos_user": most_pos_user,
            "most_neg_user": most_neg_user,
            "user_data": user_sentiment,
            "timeline": sorted(timeline_sentiment.items())
        }

    def fetch_user_trophies(self):
        trophies = []
        df_real = self.df[self.df['sender'] != 'System Notification']
        if df_real.empty: return trophies
        
        stats = self.fetch_user_stats()
        owls = self.fetch_night_owls_early_birds()
        eng = self.fetch_engagement_stats()
        
        if not stats.empty:
            # 1. The Architect
            val = stats.loc[stats['avg_words_per_msg'].idxmax()]
            trophies.append({"icon": "🏛️", "title": "The Architect", "winner": val['sender'], "desc": f"Longest messages ({val['avg_words_per_msg']} avg words)"})
            
            # 2. The Orator
            val = stats.loc[stats['words'].idxmax()]
            trophies.append({"icon": "🗣️", "title": "The Orator", "winner": val['sender'], "desc": f"Most total words ({int(val['words']):,})"})

            # 3. The Observer
            val = stats.loc[stats['messages'].idxmin()]
            trophies.append({"icon": "👁️", "title": "The Observer", "winner": val['sender'], "desc": f"Fewest total messages ({int(val['messages']):,})"})

            # 4. The Visualist
            val = stats.loc[stats['media'].idxmax()]
            if val['media'] > 0:
                trophies.append({"icon": "📸", "title": "The Visualist", "winner": val['sender'], "desc": f"Highest media share ({int(val['media']):,} files)"})
            
            # 5. The Archivist
            val = stats.loc[stats['links'].idxmax()]
            if val['links'] > 0:
                trophies.append({"icon": "🔗", "title": "The Archivist", "winner": val['sender'], "desc": f"Most links shared ({int(val['links']):,} links)"})

            # 6. The Inquirer
            val = stats.loc[stats['questions'].idxmax()]
            if val['questions'] > 0:
                trophies.append({"icon": "❓", "title": "The Inquirer", "winner": val['sender'], "desc": f"Most questions asked ({int(val['questions']):,})"})

            # 7. The Humorist
            val = stats.loc[stats['laughs'].idxmax()]
            if val['laughs'] > 0:
                trophies.append({"icon": "😂", "title": "The Humorist", "winner": val['sender'], "desc": f"Highest laughter metric ({int(val['laughs']):,} laughs)"})

            # 8. The Diplomat
            val = stats.loc[stats['polite'].idxmax()]
            if val['polite'] > 0:
                trophies.append({"icon": "🤝", "title": "The Diplomat", "winner": val['sender'], "desc": f"Most polite vocabulary ({int(val['polite']):,} hits)"})
                
            # 9. The Phantom
            val = stats.loc[stats['deleted'].idxmax()]
            if val['deleted'] > 0:
                trophies.append({"icon": "👻", "title": "The Phantom", "winner": val['sender'], "desc": f"Most deleted messages ({int(val['deleted']):,})"})

        if not owls.empty:
            val = owls.loc[owls['Night Owl Msgs (12AM-5AM)'].idxmax()]
            if val['Night Owl Msgs (12AM-5AM)'] > 0:
                trophies.append({"icon": "🦉", "title": "The Night Owl", "winner": val['Sender'], "desc": "Peak activity between 12AM-5AM"})

            val = owls.loc[owls['Early Bird Msgs (5AM-10AM)'].idxmax()]
            if val['Early Bird Msgs (5AM-10AM)'] > 0:
                trophies.append({"icon": "🌅", "title": "The Early Riser", "winner": val['Sender'], "desc": "Peak activity between 5AM-10AM"})

        if not eng.empty:
            val = eng.loc[eng['Avg Response Time (min)'].idxmax()]
            trophies.append({"icon": "⏳", "title": "The Deliberator", "winner": val['Sender'], "desc": f"Slowest avg response ({val['Avg Response Time (min)']} min)"})
            
            fast_eng = eng[eng['Avg Response Time (min)'] > 0]
            if not fast_eng.empty:
                val = fast_eng.loc[fast_eng['Avg Response Time (min)'].idxmin()]
                trophies.append({"icon": "⚡", "title": "The Sprinter", "winner": val['Sender'], "desc": f"Fastest avg response ({val['Avg Response Time (min)']} min)"})

            val = eng.loc[eng['Conversation Starters'].idxmax()]
            if val['Conversation Starters'] > 0:
                trophies.append({"icon": "🎬", "title": "The Catalyst", "winner": val['Sender'], "desc": f"Most conversation initiations ({val['Conversation Starters']})"})

            val = eng.loc[eng['Avg Msgs/Turn'].idxmax()]
            if val['Avg Msgs/Turn'] > 1.5:
                trophies.append({"icon": "🎙️", "title": "The Monologist", "winner": val['Sender'], "desc": f"Highest double-texting rate ({val['Avg Msgs/Turn']} msgs/turn)"})

        return trophies


# ==============================================================================
# PDF REPORT GENERATOR (Modern Minimalist Summary)
# ==============================================================================
class PDFReportGenerator:
    """Generates a highly structured, modern PDF summary document leveraging Matplotlib directly."""
    
    @staticmethod
    def _draw_donut(ax, labels, values, palette_name, bg_color, text_color, line_color):
        if not values or sum(values) == 0:
            ax.text(0.5, 0.5, "Insufficient Data", ha='center', va='center', color=text_color)
            ax.axis('off')
            return
            
        palette = sns.color_palette(palette_name, len(labels))
        wedges, _ = ax.pie(values, colors=palette, startangle=140, wedgeprops=dict(width=0.4, edgecolor=bg_color))
        
        kw = dict(arrowprops=dict(arrowstyle="-", color=line_color, lw=1), zorder=0, va="center")
        total_sum = sum(values)
        
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            
            percent = (values[i] / total_sum) * 100
            if percent < 3.0: continue
            
            horizontalalignment = {-1: "right", 1: "left"}[1 if x >= 0 else -1]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            
            x_scale = 1.35 if x >= 0 else -1.35
            label_str = str(labels[i])
            if len(label_str) > 15: label_str = label_str[:13] + ".."
            
            ax.annotate(f"{label_str}\n{percent:.1f}%", xy=(x, y), xytext=(x_scale, 1.2 * y),
                        horizontalalignment=horizontalalignment, color=text_color, fontsize=9, **kw)
    
    @staticmethod
    def generate_report(app, filepath: str):
        # Gather Data
        stats = app.analyzer.get_basic_stats()
        users_stats = app.analyzer.fetch_user_stats()
        eng_stats = app.analyzer.fetch_engagement_stats()
        emotions = app.analyzer.fetch_emotion_radar()
        topics = app.analyzer.fetch_topic_distribution()
        msg_dist = app.analyzer.fetch_message_type_distribution()
        timeline = app.analyzer.fetch_monthly_timeline()
        hourly = app.analyzer.fetch_hourly_activity()
        heatmap = app.analyzer.fetch_activity_heatmap()
        
        # Design Tokens
        bg_col = Theme.current["BG_MAIN"]
        surface_col = Theme.current["BG_SURFACE"]
        text_col = Theme.current["TEXT_WHITE"]
        muted_col = Theme.current["TEXT_GRAY"]
        accent_col = Theme.current["ACCENT"]
        border_col = Theme.current["BORDER"]
        palette = Theme.current.get("PLOT_PALETTE", "Blues")
        
        with PdfPages(filepath) as pdf:
            # -----------------------------------------------------
            # PAGE 1: Title, Participants & Card-Based KPIs
            # -----------------------------------------------------
            fig = plt.figure(figsize=(8.5, 11))
            fig.patch.set_facecolor(bg_col)
            ax = fig.add_axes([0, 0, 1, 1])
            ax.set_facecolor(bg_col)
            ax.axis('off')
            
            # Determine Participant Titles
            unique_users = users_stats['sender'].tolist() if not users_stats.empty else []
            if len(unique_users) == 2:
                chat_title = f"{unique_users[0]} & {unique_users[1]}"
            elif len(unique_users) > 2:
                chat_title = f"Group Chat ({len(unique_users)} Participants)"
            else:
                chat_title = "Single User / Unknown Chat"

            fig.text(0.1, 0.90, "Communications Analytics", fontsize=28, fontweight='bold', color=text_col, fontfamily='sans-serif')
            fig.text(0.1, 0.86, f"Participant Analysis: {chat_title}", fontsize=14, color=accent_col, fontfamily='sans-serif')
            fig.text(0.1, 0.83, f"Report Generated: {datetime.now().strftime('%d %b %Y')} | Data Span: {stats.get('start_date', 'N/A')} to {stats.get('end_date', 'N/A')} ({stats.get('days', 0)} Days)", fontsize=10, color=muted_col, fontfamily='sans-serif')
            
            fig.add_artist(plt.Line2D((0.1, 0.9), (0.80, 0.80), color=border_col, linewidth=1.5))
            
            fig.text(0.1, 0.74, "Executive Summary & Key Metrics", fontsize=16, fontweight='bold', color=text_col, fontfamily='sans-serif')
            
            kpis = [
                ("Total Message Volume", f"{stats.get('total_msgs', 0):,} msgs", "Total number of recorded events."),
                ("Total Word Density", f"{stats.get('total_words', 0):,} words", "Total words exchanged."),
                ("Media Assets Shared", f"{stats.get('media_count', 0):,} files", "Images, videos, and documents."),
                ("External Links Exchanged", f"{stats.get('links_count', 0):,} links", "URLs shared in chat."),
                ("Peak Activity Hour", f"{stats.get('peak_hour', 'N/A')}", "Most active time of day."),
                ("Average Words per Msg", f"{stats.get('avg_words_overall', 0)}", "Message verbosity level.")
            ]
            
            # Draw KPI Cards
            for i, (title, val, desc) in enumerate(kpis):
                col = i % 2
                row = i // 2
                x = 0.1 + col * 0.42
                y = 0.60 - row * 0.14
                w = 0.38
                h = 0.11
                
                box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.02",
                                     ec=border_col, fc=surface_col, transform=fig.transFigure)
                fig.patches.append(box)
                
                fig.text(x + 0.02, y + h - 0.02, title.upper(), fontsize=9, color=muted_col, va='top', fontweight='bold', fontfamily='sans-serif')
                fig.text(x + 0.02, y + h/2 - 0.01, val, fontsize=18, color=text_col, va='center', fontweight='bold', fontfamily='sans-serif')
                fig.text(x + 0.02, y + 0.02, desc, fontsize=8, color=muted_col, va='bottom', fontfamily='sans-serif')
                
            fig.text(0.1, 0.1, "This document contains a structured breakdown of distribution, temporal trends, comparative analytics, and behavioral insights.", fontsize=10, color=muted_col, fontstyle='italic', fontfamily='sans-serif')
            
            pdf.savefig(fig, bbox_inches='tight', facecolor=bg_col)
            plt.close(fig)

            # -----------------------------------------------------
            # PAGE 2: Proportions & Distributions (Donut Charts)
            # -----------------------------------------------------
            fig = plt.figure(figsize=(8.5, 11))
            fig.patch.set_facecolor(bg_col)
            
            fig.text(0.1, 0.92, "Distribution Proportions", fontsize=22, fontweight='bold', color=text_col, fontfamily='sans-serif')
            fig.add_artist(plt.Line2D((0.1, 0.9), (0.89, 0.89), color=border_col, linewidth=1.5))
            
            fig.text(0.1, 0.85, "1. Message Structural Composition", fontsize=14, fontweight='bold', color=accent_col, fontfamily='sans-serif')
            fig.text(0.1, 0.82, textwrap.fill("This donut chart segments the total dataset into raw text, media assets, and external links.", 90), fontsize=10, color=muted_col, va='top', fontfamily='sans-serif')
            
            ax1 = fig.add_axes([0.1, 0.50, 0.8, 0.30])
            ax1.set_facecolor(bg_col)
            if msg_dist:
                PDFReportGenerator._draw_donut(ax1, list(msg_dist.keys()), list(msg_dist.values()), palette, bg_col, text_col, muted_col)

            fig.text(0.1, 0.45, "2. Categorical Topic Dispersion", fontsize=14, fontweight='bold', color=accent_col, fontfamily='sans-serif')
            fig.text(0.1, 0.42, textwrap.fill("Utilizing the offline NLP engine, this chart categorizes sentences into distinct subjects based on lexicon hits.", 90), fontsize=10, color=muted_col, va='top', fontfamily='sans-serif')
            
            ax2 = fig.add_axes([0.1, 0.10, 0.8, 0.30])
            ax2.set_facecolor(bg_col)
            t_labels = [k for k, v in topics.items() if v > 0]
            t_values = [v for k, v in topics.items() if v > 0]
            PDFReportGenerator._draw_donut(ax2, t_labels, t_values, palette, bg_col, text_col, muted_col)

            pdf.savefig(fig, bbox_inches='tight', facecolor=bg_col)
            plt.close(fig)

            # -----------------------------------------------------
            # PAGE 3: Temporal Trends (Line & Area)
            # -----------------------------------------------------
            fig = plt.figure(figsize=(8.5, 11))
            fig.patch.set_facecolor(bg_col)
            
            fig.text(0.1, 0.94, "Temporal & Activity Trends", fontsize=22, fontweight='bold', color=text_col, fontfamily='sans-serif')
            fig.add_artist(plt.Line2D((0.1, 0.9), (0.91, 0.91), color=border_col, linewidth=1.5))
            
            fig.text(0.1, 0.87, "Macro Timeline Volume", fontsize=12, fontweight='bold', color=accent_col, fontfamily='sans-serif')
            fig.text(0.1, 0.84, "Tracks total communication events month over month.", fontsize=10, color=muted_col, va='top', fontfamily='sans-serif')

            ax1 = fig.add_axes([0.1, 0.65, 0.8, 0.18])
            ax1.set_facecolor(bg_col)
            if not timeline.empty:
                ax1.plot(timeline['time'], timeline['message'], color=accent_col, marker='o', lw=2, markersize=4)
                ax1.fill_between(timeline['time'], timeline['message'], color=accent_col, alpha=0.15)
                ax1.tick_params(axis='x', rotation=45, colors=muted_col, labelsize=8)
            apply_modern_plot_style(ax1, "", ylabel="Msgs")

            fig.text(0.1, 0.58, "Intraday Velocity", fontsize=12, fontweight='bold', color=accent_col, fontfamily='sans-serif')
            fig.text(0.1, 0.55, "Highlights the average volume of messages sent per hour over the 24-hour clock.", fontsize=10, color=muted_col, va='top', fontfamily='sans-serif')

            ax2 = fig.add_axes([0.1, 0.36, 0.8, 0.18])
            ax2.set_facecolor(bg_col)
            if not hourly.empty:
                ax2.plot(hourly['hour'], hourly['count'], color=accent_col, marker='o', lw=2, markersize=4)
                ax2.set_xticks(range(0, 24))
            apply_modern_plot_style(ax2, "", xlabel="24h Clock", ylabel="Msgs")

            fig.text(0.1, 0.29, "Density Matrix (Day vs. Hour)", fontsize=12, fontweight='bold', color=accent_col, fontfamily='sans-serif')
            fig.text(0.1, 0.26, "Combines days of the week and hours of the day to identify exact periods of peak interaction.", fontsize=10, color=muted_col, va='top', fontfamily='sans-serif')

            ax3 = fig.add_axes([0.1, 0.05, 0.8, 0.20])
            ax3.set_facecolor(bg_col)
            if not heatmap.empty:
                sns.heatmap(heatmap, cmap=palette, ax=ax3, linewidths=1, linecolor=bg_col, cbar=False)
            apply_modern_plot_style(ax3, "")
            ax3.tick_params(labelsize=8)

            pdf.savefig(fig, bbox_inches='tight', facecolor=bg_col)
            plt.close(fig)

            # -----------------------------------------------------
            # PAGE 4: Comparative Analytics (Bar Charts)
            # -----------------------------------------------------
            fig = plt.figure(figsize=(8.5, 11))
            fig.patch.set_facecolor(bg_col)
            
            fig.text(0.1, 0.94, "Comparative Diagnostics", fontsize=22, fontweight='bold', color=text_col, fontfamily='sans-serif')
            fig.add_artist(plt.Line2D((0.1, 0.9), (0.91, 0.91), color=border_col, linewidth=1.5))
            
            fig.text(0.1, 0.87, "Participant Contribution Volume", fontsize=12, fontweight='bold', color=accent_col, fontfamily='sans-serif')
            fig.text(0.1, 0.84, "Total messages sent per individual, dictating conversational dominance.", fontsize=10, color=muted_col, va='top', fontfamily='sans-serif')

            ax1 = fig.add_axes([0.1, 0.65, 0.8, 0.18])
            ax1.set_facecolor(bg_col)
            if not users_stats.empty:
                ax1.bar(users_stats['sender'].str[:12], users_stats['messages'], color=accent_col, width=0.5)
            apply_modern_plot_style(ax1, "", ylabel="Msgs")

            fig.text(0.1, 0.58, "Average Response Delay", fontsize=12, fontweight='bold', color=accent_col, fontfamily='sans-serif')
            fig.text(0.1, 0.55, "Average gap in minutes before a participant responds to another.", fontsize=10, color=muted_col, va='top', fontfamily='sans-serif')

            ax2 = fig.add_axes([0.1, 0.36, 0.8, 0.18])
            ax2.set_facecolor(bg_col)
            if not eng_stats.empty:
                valid_resp = eng_stats[eng_stats['Avg Response Time (min)'] > 0].sort_values("Avg Response Time (min)")
                ax2.bar(valid_resp['Sender'].str[:12], valid_resp['Avg Response Time (min)'], color=Theme.current["SUCCESS"], width=0.5)
            apply_modern_plot_style(ax2, "", ylabel="Minutes")

            fig.text(0.1, 0.29, "Emotional State Mapping", fontsize=12, fontweight='bold', color=accent_col, fontfamily='sans-serif')
            fig.text(0.1, 0.26, "Overall usage of emotional terminology mapped against the offline NLP lexicon.", fontsize=10, color=muted_col, va='top', fontfamily='sans-serif')

            ax3 = fig.add_axes([0.1, 0.05, 0.8, 0.20])
            ax3.set_facecolor(bg_col)
            e_labels = list(emotions.keys())
            e_values = list(emotions.values())
            if sum(e_values) > 0:
                ax3.bar(e_labels, e_values, color=Theme.current["ERROR"], width=0.5)
            apply_modern_plot_style(ax3, "", ylabel="Lexicon Hits")

            pdf.savefig(fig, bbox_inches='tight', facecolor=bg_col)
            plt.close(fig)

            # -----------------------------------------------------
            # PAGE 5: Behavioral Conclusion & Insights
            # -----------------------------------------------------
            fig = plt.figure(figsize=(8.5, 11))
            fig.patch.set_facecolor(bg_col)
            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis('off')
            
            ax.text(0.1, 0.88, "Final Diagnostic Conclusion", fontsize=22, fontweight='bold', color=text_col, fontfamily='sans-serif')
            ax.add_artist(plt.Line2D((0.1, 0.9), (0.85, 0.85), color=border_col, linewidth=1.5))

            # Calculate Insights dynamically
            top_sender = users_stats.iloc[0]['sender'] if not users_stats.empty else "Unknown"
            top_sender_msgs = users_stats.iloc[0]['messages'] if not users_stats.empty else 0
            total_msgs = stats.get('total_msgs', 1)
            contribution_pct = (top_sender_msgs / total_msgs) * 100 if total_msgs > 0 else 0

            top_starter = eng_stats.iloc[0]['Sender'] if not eng_stats.empty else "Unknown"
            fastest = eng_stats.sort_values("Avg Response Time (min)").iloc[0]['Sender'] if not eng_stats.empty else "Unknown"
            fastest_time = eng_stats.sort_values("Avg Response Time (min)").iloc[0]['Avg Response Time (min)'] if not eng_stats.empty else 0
            
            top_emotion = max(emotions, key=emotions.get) if sum(emotions.values()) > 0 else "Neutral Context"
            top_topic = max(topics, key=topics.get) if sum(topics.values()) > 0 else "General Dialogue"

            # Construct Insights Paragraphs
            p1 = f"Based on the analysis of {total_msgs:,} data points, {top_sender} acts as the primary driver of communication volume, contributing approximately {contribution_pct:.1f}% of all total messages. This establishes a structural baseline for the engagement dynamic."
            p2 = f"However, initiation and responsiveness tell a deeper story. {top_starter} acts as the primary catalyst, breaking periods of extended silence (8+ hours) to initiate conversations more frequently than other participants. Once engaged, {fastest} exhibits the highest attention metrics, registering the fastest average response delay of just {fastest_time} minutes."
            p3 = f"Linguistically, the data indicates a predominantly '{top_emotion}' emotional baseline. When scanning for distinct conversational subject matter via the offline NLP engine, '{top_topic}' emerged as the most consistently referenced categorical topic."
            
            y_cursor = 0.80
            
            def add_section(title, text, y_pos):
                ax.text(0.1, y_pos, title, fontsize=14, fontweight='bold', color=accent_col, va='top', fontfamily='sans-serif')
                y_pos -= 0.03
                wrapped = textwrap.fill(text, width=85)
                ax.text(0.1, y_pos, wrapped, fontsize=11, color=muted_col, linespacing=1.6, va='top', fontfamily='sans-serif')
                lines = len(wrapped.split('\n'))
                return y_pos - (lines * 0.025) - 0.05
                
            y_cursor = add_section("1. Volume & Dominance", p1, y_cursor)
            y_cursor = add_section("2. Engagement & Responsiveness", p2, y_cursor)
            y_cursor = add_section("3. Linguistic & Emotional Tone", p3, y_cursor)

            ax.text(0.1, 0.1, "End of Analysis Report.", fontsize=10, color=border_col, fontstyle='italic', fontfamily='sans-serif')

            pdf.savefig(fig, bbox_inches='tight', facecolor=bg_col)
            plt.close(fig)

        return True


# ==============================================================================
# GUI: SUB-WINDOWS (Minimalist Corporate Restyle)
# ==============================================================================

class ThemeSettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Preferences")
        self.geometry("400x320")
        self.resizable(False, False)
        self.parent = parent
        self.configure(bg=Theme.current["BG_MAIN"])
        
        container = tk.Frame(self, bg=Theme.current["BG_MAIN"], padx=30, pady=30)
        container.pack(fill="both", expand=True)

        tk.Label(container, text="Application Theme", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"], anchor="w").pack(fill="x", pady=(0, 5))
        self.theme_var = tk.StringVar(value=next(k for k,v in Theme.THEMES.items() if v == Theme.current))
        ttk.Combobox(container, textvariable=self.theme_var, values=list(Theme.THEMES.keys()), state="readonly", style="Modern.TCombobox").pack(fill="x", pady=(0, 20))
        
        tk.Label(container, text="Typography", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"], anchor="w").pack(fill="x", pady=(0, 5))
        self.font_var = tk.StringVar(value=Theme.current_font)
        ttk.Combobox(container, textvariable=self.font_var, values=Theme.APP_FONTS, state="readonly", style="Modern.TCombobox").pack(fill="x", pady=(0, 30))

        RoundedButton(container, text="Apply Changes", command=self.apply, width=340).pack()
        
    def apply(self):
        theme_sel = self.theme_var.get()
        font_sel = self.font_var.get()
        
        Theme.set_theme(theme_sel)
        Theme.set_font(font_sel)
        Theme.save_config(theme_sel, font_sel)
        
        self.parent._apply_theme()
        if not self.parent.df.empty:
            self.parent.refresh_dashboard()
            
        messagebox.showinfo("Preferences Updated", "Display settings successfully applied & saved.\n\nCharts and Main interfaces have refreshed instantly. Note: A restart may be needed for minor sub-dialogs.")
        self.destroy()

class UserGuideGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Application Guide")
        self.geometry("800x650")
        self.resizable(False, False)
        font_choice = Theme.current_font
        self.configure(bg=Theme.current["BG_MAIN"])

        # Header
        header_frame = tk.Frame(self, bg=Theme.current["BG_MAIN"])
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        tk.Label(header_frame, text="User Guide & Documentation", font=(font_choice, 16, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"]).pack(anchor="w")
        tk.Label(header_frame, text="Learn how to navigate and utilize the analytics engine effectively.", font=(font_choice, 9), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"]).pack(anchor="w", pady=(2, 0))

        # Scrollable Container
        self.scroll_guide = ScrollableFrame(self, bg=Theme.current["BG_MAIN"])
        self.scroll_guide.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        container = self.scroll_guide.scrollable_container

        def add_section(title, content_dict):
            sec = tk.Frame(container, bg=Theme.current["BG_SURFACE"], highlightthickness=1, highlightbackground=Theme.current["BORDER"])
            sec.pack(fill="x", expand=True, padx=10, pady=(0, 15))
            tk.Label(sec, text=title, font=(font_choice, 12, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["ACCENT"]).pack(anchor="w", padx=20, pady=(15, 10))
            
            for k, v in content_dict.items():
                item_frame = tk.Frame(sec, bg=Theme.current["BG_SURFACE"])
                item_frame.pack(fill="x", padx=20, pady=(0, 10))
                if k:
                    tk.Label(item_frame, text=k, font=(font_choice, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(anchor="w")
                tk.Label(item_frame, text=v, font=(font_choice, 9), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], justify="left", wraplength=670).pack(anchor="w", pady=(2, 0))

        add_section("What is this App?", {
            "": "This application is a powerful, offline Natural Language Processing (NLP) engine designed to analyze exported WhatsApp chats. It processes conversations to extract behavioral insights, sentiment, conflict zones, and detailed engagement metrics without your data ever leaving your machine."
        })

        add_section("Core Functions (Sidebar)", {
            "Import Dataset": "Loads a standard WhatsApp .txt export. Note: Export your chat 'Without Media' from WhatsApp to generate this file.",
            "Export to PDF": "Generates a beautiful, multi-page PDF executive summary of the currently loaded dataset.",
            "Participant Filter": "Allows you to isolate the dashboard analytics to a single user's metrics.",
            "Apply Filter": "Refreshes the entire dashboard based on your selected participant or system log preferences."
        })

        add_section("Dashboard Modules (Top Tabs)", {
            "Overview": "High-level Key Performance Indicators (KPIs) and structural breakdown of messages.",
            "Timeline": "Macro-level volume tracking over months/years.",
            "Activity": "Granular breakdown of activity by hour, day, and a dense heatmap of peak interaction times.",
            "Engagement": "Calculates average response delays, who initiates conversations after long silences (8+ hours), and double-texting rates.",
            "Topics": "Categorizes conversations into subjects (Work, Finance, Social, etc.) using offline lexicons.",
            "Conflicts": "Identifies hostile terms, tracks arguments over time, and flags the primary instigators.",
            "Accolades": "Awards fun, behavioral trophies (e.g., 'The Deliberator', 'The Catalyst') based on user stats.",
            "Lexicon": "Visualizes vocabulary through word clouds, tracks shared domains, emoji usage, and micro-expressions.",
            "Sentiment": "Analyzes the emotional tone (Joy, Anger, Sadness, etc.) and compares the overall positivity vs negativity.",
            "Log View": "A raw, tabular view of the parsed dataset."
        })

        add_section("Utilities", {
            "Tracker": "A daily objective tracking matrix. Monitor habits, build strict streaks, and record lifetime completions.",
            "Converter": "A real-time, multi-category unit conversion tool with precision control and clipboard export.",
            "Deep Query": "An advanced search engine for your chat data. Supports RegEx, case sensitivity, participant filtering, and CSV exporting."
        })

class AccoladeCard(tk.Frame):
    """Custom Card UI for displaying participant trophies in a grid layout."""
    def __init__(self, parent, icon, title, winner, desc):
        super().__init__(parent, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        
        top_frame = tk.Frame(self, bg=Theme.current["BG_SURFACE"])
        top_frame.pack(fill="x", padx=15, pady=(15, 5))
        
        self.lbl_icon = tk.Label(top_frame, text=icon, font=(Theme.current_font, 16), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"])
        self.lbl_icon.pack(side="left", padx=(0, 8))
        
        self.lbl_title = tk.Label(top_frame, text=title, font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["ACCENT"])
        self.lbl_title.pack(side="left")
        
        # Wrapping logic to ensure long names (like phone numbers) don't blow up the grid
        winner_text = winner if len(winner) <= 22 else winner[:19] + "..."
        
        self.lbl_winner = tk.Label(self, text=winner_text, font=(Theme.current_font, 13, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"])
        self.lbl_winner.pack(anchor="w", padx=15, pady=(5, 0))
        
        self.lbl_desc = tk.Label(self, text=desc, font=(Theme.current_font, 9), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"])
        self.lbl_desc.pack(anchor="w", padx=15, pady=(2, 15))

    def update_theme_colors(self):
        self.configure(bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"])
        for child in self.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=Theme.current["BG_SURFACE"])
        self.lbl_icon.configure(bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"])
        self.lbl_title.configure(bg=Theme.current["BG_SURFACE"], fg=Theme.current["ACCENT"])
        self.lbl_winner.configure(bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"])
        self.lbl_desc.configure(bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"])

class ChatAnonymizerGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Data Anonymization Tool")
        self.geometry("450x250")
        self.resizable(False, False)
        self.parent = parent
        self.configure(bg=Theme.current["BG_MAIN"])
        
        container = tk.Frame(self, bg=Theme.current["BG_MAIN"], padx=30, pady=30)
        container.pack(fill="both", expand=True)
        
        tk.Label(container, text="Privacy Protection", font=(Theme.current_font, 14, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"], anchor="w").pack(fill="x", pady=(0, 5))
        tk.Label(container, text="Export the current dataset to CSV format\nwith all participant identities masked.", bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"], justify="left", font=(Theme.current_font, 9), anchor="w").pack(fill="x", pady=(0, 30))
        
        RoundedButton(container, text="Save Anonymized CSV", command=self.anonymize, width=390).pack()
        
    def anonymize(self):
        if self.parent.df_full.empty:
            messagebox.showerror("Error", "No dataset loaded.")
            return
            
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="anonymized_dataset.csv", filetypes=[("CSV", "*.csv")])
        if path:
            df_anon = self.parent.df_full.copy()
            unique_users = [u for u in df_anon['sender'].unique() if u != "System Notification"]
            user_map = {u: f"Participant {i+1}" for i, u in enumerate(unique_users)}
            user_map["System Notification"] = "System"
            
            df_anon['sender'] = df_anon['sender'].map(user_map)
            df_anon['message'] = df_anon['message'].str.replace(r'\+?\d{10,14}', '[REDACTED PHONE]', regex=True)
            
            df_anon.to_csv(path, index=False)
            messagebox.showinfo("Success", f"Anonymized record saved to {path}")
            self.destroy()

class UserCompareGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Participant Comparison")
        self.geometry("800x600")
        self.resizable(False, False)
        self.parent = parent
        self.configure(bg=Theme.current["BG_MAIN"])
        
        if parent.df_full.empty:
            tk.Label(self, text="Please load a dataset first.", bg=Theme.current["BG_MAIN"], fg=Theme.current["ERROR"], font=(Theme.current_font, 10)).pack(pady=50)
            return
            
        users = [u for u in parent.df_full['sender'].unique() if u != "System Notification"]
        if len(users) < 2:
            tk.Label(self, text="Insufficient participants for comparison (minimum 2).", bg=Theme.current["BG_MAIN"], fg=Theme.current["ERROR"], font=(Theme.current_font, 10)).pack(pady=50)
            return

        top_frame = tk.Frame(self, bg=Theme.current["BG_MAIN"], padx=40, pady=20)
        top_frame.pack(fill='x')
        
        self.u1_var = tk.StringVar(value=users[0])
        self.u2_var = tk.StringVar(value=users[1])
        
        ttk.Combobox(top_frame, textvariable=self.u1_var, values=users, state="readonly", font=(Theme.current_font, 9), style="Modern.TCombobox").pack(side='left')
        tk.Label(top_frame, text="vs", font=(Theme.current_font, 12, "italic"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"]).pack(side='left', expand=True)
        ttk.Combobox(top_frame, textvariable=self.u2_var, values=users, state="readonly", font=(Theme.current_font, 9), style="Modern.TCombobox").pack(side='right')
        
        RoundedButton(self, text="Generate Analysis", command=self.compare, width=200).pack(pady=10)
        
        self.chart_frame = tk.Frame(self, bg=Theme.current["BG_SURFACE"])
        self.chart_frame.pack(fill='both', expand=True, padx=40, pady=(10, 40))

    def compare(self):
        u1, u2 = self.u1_var.get(), self.u2_var.get()
        if u1 == u2:
            messagebox.showwarning("Invalid Selection", "Participants must be distinct.")
            return
            
        df1 = self.parent.df_full[self.parent.df_full['sender'] == u1]
        df2 = self.parent.df_full[self.parent.df_full['sender'] == u2]
        
        stats = {
            "Messages": [df1.shape[0], df2.shape[0]],
            "Words": [df1['word_count'].sum(), df2['word_count'].sum()],
            "Media": [df1['is_media'].sum(), df2['is_media'].sum()],
            "Links": [df1['has_link'].sum(), df2['has_link'].sum()]
        }
        
        for w in self.chart_frame.winfo_children(): w.destroy()
            
        plt.style.use(Theme.current["PLOT_STYLE"])
        fig, axes = plt.subplots(1, 4, figsize=(10, 4))
        fig.patch.set_facecolor(Theme.current["BG_SURFACE"])
        
        colors = [Theme.current["ACCENT"], Theme.current["TEXT_GRAY"]]
        
        for idx, (title, values) in enumerate(stats.items()):
            ax = axes[idx]
            ax.set_facecolor(Theme.current["BG_SURFACE"])
            ax.bar([u1[:8], u2[:8]], values, color=colors)
            apply_modern_plot_style(ax, title)
            ax.tick_params(colors=Theme.current["TEXT_GRAY"], rotation=0)
            
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

class SearchGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Deep Query Engine")
        self.geometry("950x700")
        self.resizable(False, False)
        self.parent = parent
        self.configure(bg=Theme.current["BG_MAIN"])
        font_choice = Theme.current_font

        self.current_results = pd.DataFrame()

        # Header
        header_frame = tk.Frame(self, bg=Theme.current["BG_MAIN"])
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        tk.Label(header_frame, text="Deep Query Engine", font=(font_choice, 14, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"]).pack(anchor="w")
        tk.Label(header_frame, text="Advanced text, regex, and participant-filtered search utility.", font=(font_choice, 9), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"]).pack(anchor="w", pady=(2, 0))

        # Control Panel
        ctrl_frame = tk.Frame(self, bg=Theme.current["BG_SURFACE"], highlightthickness=1, highlightbackground=Theme.current["BORDER"])
        ctrl_frame.pack(fill="x", padx=30, pady=10)

        # Row 1: Search Bar & User Filter
        row1 = tk.Frame(ctrl_frame, bg=Theme.current["BG_SURFACE"])
        row1.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(row1, text="Query:", bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"], font=(font_choice, 9, "bold")).pack(side="left", padx=(0, 10))
        self.entry = tk.Entry(row1, font=(font_choice, 11), width=45, bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"], insertbackground=Theme.current["TEXT_WHITE"], relief="flat", highlightthickness=1, highlightbackground=Theme.current["BORDER"])
        self.entry.pack(side="left", ipady=6, padx=(0, 20))

        tk.Label(row1, text="Target:", bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"], font=(font_choice, 9, "bold")).pack(side="left", padx=(0, 10))
        
        users = ["All Participants"]
        if not self.parent.df_full.empty:
            users += sorted(self.parent.df_full[self.parent.df_full['sender'] != 'System Notification']['sender'].unique().tolist())
        
        self.user_var = tk.StringVar(value="All Participants")
        self.user_combo = ttk.Combobox(row1, textvariable=self.user_var, values=users, state="readonly", font=(font_choice, 9), style="Modern.TCombobox", width=25)
        self.user_combo.pack(side="left")

        # Row 2: Options & Actions
        row2 = tk.Frame(ctrl_frame, bg=Theme.current["BG_SURFACE"])
        row2.pack(fill="x", padx=20, pady=(0, 20))

        # Toggles
        opts_frame = tk.Frame(row2, bg=Theme.current["BG_SURFACE"])
        opts_frame.pack(side="left")
        
        self.use_regex = tk.BooleanVar(value=False)
        self.case_sensitive = tk.BooleanVar(value=False)
        
        # Using basic Checkbuttons styled to match
        tk.Checkbutton(opts_frame, text="RegEx Mode", variable=self.use_regex, bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], selectcolor=Theme.current["BG_MAIN"], activebackground=Theme.current["BG_SURFACE"], activeforeground=Theme.current["TEXT_WHITE"], font=(font_choice, 9)).pack(side="left", padx=(0, 15))
        tk.Checkbutton(opts_frame, text="Case Sensitive", variable=self.case_sensitive, bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], selectcolor=Theme.current["BG_MAIN"], activebackground=Theme.current["BG_SURFACE"], activeforeground=Theme.current["TEXT_WHITE"], font=(font_choice, 9)).pack(side="left")

        # Buttons
        btns_frame = tk.Frame(row2, bg=Theme.current["BG_SURFACE"])
        btns_frame.pack(side="right")

        self.lbl_res = tk.Label(btns_frame, text="Ready.", bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], font=(font_choice, 9))
        self.lbl_res.pack(side="left", padx=(0, 15))

        RoundedButton(btns_frame, text="Export CSV", command=self.export_results, width=100, height=30, bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"]).pack(side="left", padx=(0, 10))
        RoundedButton(btns_frame, text="Search", command=self.do_search, width=100, height=30).pack(side="left")

        # Results Matrix
        res_frame = tk.Frame(self, bg=Theme.current["BG_SURFACE"], highlightthickness=1, highlightbackground=Theme.current["BORDER"])
        res_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        self.tree = ttk.Treeview(res_frame, columns=("Time", "Sender", "Message"), show="headings")
        self.tree.heading("Time", text="Timestamp")
        self.tree.heading("Sender", text="Participant")
        self.tree.heading("Message", text="Content")
        
        self.tree.column("Time", width=140, anchor="w")
        self.tree.column("Sender", width=150, anchor="w")
        self.tree.column("Message", width=580, anchor="w")

        scroll_y = ttk.Scrollbar(res_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scroll_y.pack(side="right", fill="y")
        
        self.entry.bind("<Return>", lambda e: self.do_search())

    def do_search(self):
        query = self.entry.get().strip()
        if not query: return
        
        for i in self.tree.get_children(): self.tree.delete(i)
        self.current_results = pd.DataFrame()
            
        try:
            df_search = self.parent.df_full.copy()
            
            # Feature: Participant Filter
            target_user = self.user_var.get()
            if target_user != "All Participants":
                df_search = df_search[df_search['sender'] == target_user]

            regex = self.use_regex.get()
            case_sens = self.case_sensitive.get()
            
            # Execute Search
            results = df_search[df_search['message'].str.contains(query, regex=regex, na=False, case=case_sens)]
            self.current_results = results.sort_values(by="datetime", ascending=False)
                
            self.lbl_res.config(text=f"{len(results)} matches found")
            
            for _, row in self.current_results.iterrows():
                t = row['datetime'].strftime("%Y-%m-%d %H:%M")
                self.tree.insert("", "end", values=(t, row['sender'], wrap_text(row['message'], 80)))
                
        except Exception as e:
            messagebox.showerror("Query Error", f"Invalid search parameters:\n{e}")

    def export_results(self):
        if self.current_results.empty:
            messagebox.showinfo("No Data", "Perform a valid search before exporting.")
            return
            
        path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile="query_results.csv", filetypes=[("CSV", "*.csv")])
        if path:
            export_df = self.current_results[['datetime_str', 'sender', 'message']].copy()
            export_df.rename(columns={'datetime_str': 'Timestamp', 'sender': 'Participant', 'message': 'Message'}, inplace=True)
            export_df.to_csv(path, index=False)
            messagebox.showinfo("Export Successful", f"Successfully exported {len(export_df)} matched records.")

class HabitTrackerGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Activity Tracker")
        self.geometry("750x600")
        self.resizable(False, False)
        font_choice = Theme.current_font
        self.configure(bg=Theme.current["BG_MAIN"])
        
        # Load Data
        self.habits = {}
        if HABITS_FILE.exists():
            try:
                with open(HABITS_FILE, 'r') as f:
                    self.habits = json.load(f)
            except: pass

        # Header
        header_frame = tk.Frame(self, bg=Theme.current["BG_MAIN"])
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        tk.Label(header_frame, text="Daily Objectives & Routines", font=(font_choice, 14, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"]).pack(anchor="w")
        tk.Label(header_frame, text="Monitor daily habits, build sequential streaks, and track aggregate lifetime completions.", font=(font_choice, 9), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"]).pack(anchor="w", pady=(2, 0))
        
        # Top KPI Row
        kpi_row = tk.Frame(self, bg=Theme.current["BG_MAIN"])
        kpi_row.pack(fill="x", padx=30, pady=(0, 15))
        
        self.card_active = InfoCard(kpi_row, "Active Objectives", "🎯", width=220, height=80)
        self.card_active.pack(side="left", padx=(0, 10))
        self.card_total = InfoCard(kpi_row, "Lifetime Completions", "✅", width=220, height=80)
        self.card_total.pack(side="left", padx=(0, 10))
        self.card_best = InfoCard(kpi_row, "Highest Streak", "🔥", width=220, height=80)
        self.card_best.pack(side="left")

        # Treeview Matrix
        list_frame = tk.Frame(self, bg=Theme.current["BG_SURFACE"], highlightthickness=1, highlightbackground=Theme.current["BORDER"])
        list_frame.pack(fill='both', expand=True, padx=30, pady=5)
        
        self.tree = ttk.Treeview(list_frame, columns=("Status", "Objective", "Current Streak", "Aggregate"), show="headings", height=8)
        self.tree.heading("Status", text="Status")
        self.tree.heading("Objective", text="Objective Name")
        self.tree.heading("Current Streak", text="Current Streak")
        self.tree.heading("Aggregate", text="Total Completions")
        
        self.tree.column("Status", width=90, anchor="center")
        self.tree.column("Objective", width=290, anchor="w")
        self.tree.column("Current Streak", width=140, anchor="center")
        self.tree.column("Aggregate", width=140, anchor="center")
        
        scroll_y = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        scroll_y.pack(side="right", fill="y")
        
        # Action Bar
        btn_frame = tk.Frame(self, bg=Theme.current["BG_MAIN"])
        btn_frame.pack(fill='x', padx=30, pady=20)
        
        RoundedButton(btn_frame, text="+ Add Objective", command=self.add_habit, width=130, height=32).pack(side='left', padx=(0, 10))
        RoundedButton(btn_frame, text="Mark Complete", command=self.mark_habit, width=130, height=32, bg=Theme.current["SUCCESS"]).pack(side='left', padx=(0, 10))
        RoundedButton(btn_frame, text="Reset Streak", command=self.reset_streak, width=120, height=32, bg="#64748B", fg="#FFFFFF").pack(side='left')
        RoundedButton(btn_frame, text="Remove", command=self.remove_habit, width=90, height=32, bg=Theme.current["ERROR"]).pack(side='right')

        self.refresh()
        
    def save(self):
        with open(HABITS_FILE, 'w') as f:
            json.dump(self.habits, f)

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        today_date = datetime.now().date()
        today_str = str(today_date)
        
        total_completions = 0
        best_streak = 0
        
        for h, data in self.habits.items():
            last = data.get("last_done", "")
            streak = data.get("streak", 0)
            total = data.get("total", 0)
            
            # Auto-break strict streak logic for display if they missed yesterday
            if last and last != today_str:
                try:
                    last_date = datetime.strptime(last, "%Y-%m-%d").date()
                    if (today_date - last_date).days > 1:
                        streak = 0
                        self.habits[h]["streak"] = 0
                except: pass
                
            done_today = (last == today_str)
            status_icon = "✅ Done" if done_today else "⏳ Pending"
            
            total_completions += total
            if streak > best_streak: best_streak = streak
            
            self.tree.insert("", "end", values=(status_icon, h, f"{streak} Days", total))
            
        self.save() # Persist any auto-broken streaks
            
        self.card_active.update_value(len(self.habits), "Monitored habits")
        self.card_total.update_value(total_completions, "Lifetime successes")
        self.card_best.update_value(f"{best_streak} Days", "Maximum continuity")
            
    def add_habit(self):
        h = simpledialog.askstring("New Objective", "Enter objective name (e.g., Drink 2L Water):")
        if h and h not in self.habits:
            self.habits[h] = {"streak": 0, "last_done": "", "total": 0}
            self.save()
            self.refresh()
            
    def mark_habit(self):
        sel = self.tree.selection()
        if sel:
            name = self.tree.item(sel[0])['values'][1]
            today_date = datetime.now().date()
            today_str = str(today_date)
            
            last = self.habits[name].get("last_done", "")
            
            if last != today_str:
                streak = self.habits[name].get("streak", 0)
                try:
                    if last:
                        last_date = datetime.strptime(last, "%Y-%m-%d").date()
                        if (today_date - last_date).days == 1:
                            streak += 1
                        else:
                            streak = 1 # Broken streak, restarts at 1
                    else:
                        streak = 1
                except:
                    streak = 1
                
                self.habits[name]["streak"] = streak
                self.habits[name]["last_done"] = today_str
            self.habits[name]["total"] = self.habits[name].get("total", 0) + 1
            self.save()
            self.refresh()
            
    def reset_streak(self):
        sel = self.tree.selection()
        if sel:
            name = self.tree.item(sel[0])['values'][1]
            if messagebox.askyesno("Confirm Reset", f"Reset consecutive streak for '{name}' to 0?\n(Lifetime aggregate will be preserved.)"):
                self.habits[name]["streak"] = 0
                self.habits[name]["last_done"] = ""
                self.save()
                self.refresh()
            
    def remove_habit(self):
        sel = self.tree.selection()
        if sel:
            name = self.tree.item(sel[0])['values'][1]
            if messagebox.askyesno("Confirm Deletion", f"Permanently remove objective '{name}'?"):
                del self.habits[name]
                self.save()
                self.refresh()

class AdvancedUnitConverterGUI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Unit Conversion Utility")
        self.geometry("750x480")
        self.resizable(False, False)
        font_choice = Theme.current_font
        self.configure(bg=Theme.current["BG_MAIN"])
        
        # Header
        header_frame = tk.Frame(self, bg=Theme.current["BG_MAIN"])
        header_frame.pack(fill="x", padx=30, pady=(20, 10))
        tk.Label(header_frame, text="Universal Converter", font=(font_choice, 14, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"]).pack(anchor="w")
        tk.Label(header_frame, text="Real-time multi-category unit conversions with precision control.", font=(font_choice, 9), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"]).pack(anchor="w", pady=(2, 0))

        # Main Container
        container = tk.Frame(self, bg=Theme.current["BG_SURFACE"], highlightthickness=1, highlightbackground=Theme.current["BORDER"])
        container.pack(fill="both", expand=True, padx=30, pady=(10, 30))

        # Controls Bar
        ctrl_frame = tk.Frame(container, bg=Theme.current["BG_SURFACE"])
        ctrl_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        tk.Label(ctrl_frame, text="Category Domain:", font=(font_choice, 9, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(side="left", padx=(0, 10))

        self.categories = {
            "Length": ["Meters", "Kilometers", "Centimeters", "Miles", "Feet", "Inches"],
            "Mass & Weight": ["Kilograms", "Grams", "Pounds", "Ounces"],
            "Temperature": ["Celsius", "Fahrenheit", "Kelvin"],
            "Digital Storage": ["Bytes", "Kilobytes", "Megabytes", "Gigabytes", "Terabytes"],
            "Volume": ["Liters", "Milliliters", "Gallons", "Fluid Ounces"],
            "Time": ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Years"],
            "Speed": ["Meters/Second", "Kilometers/Hour", "Miles/Hour", "Knots"]
        }

        self.cat_var = tk.StringVar(value="Length")
        self.cat_combo = ttk.Combobox(ctrl_frame, textvariable=self.cat_var, values=list(self.categories.keys()), state="readonly", font=(font_choice, 9), style="Modern.TCombobox", width=20)
        self.cat_combo.pack(side="left")
        self.cat_combo.bind("<<ComboboxSelected>>", self.on_category_change)
        
        # Feature: Precision Control
        tk.Label(ctrl_frame, text="Precision:", font=(font_choice, 9, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(side="left", padx=(30, 10))
        self.prec_var = tk.StringVar(value="4 Decimals")
        self.prec_combo = ttk.Combobox(ctrl_frame, textvariable=self.prec_var, values=["2 Decimals", "4 Decimals", "6 Decimals", "8 Decimals"], state="readonly", font=(font_choice, 9), style="Modern.TCombobox", width=12)
        self.prec_combo.pack(side="left")
        self.prec_combo.bind("<<ComboboxSelected>>", lambda e: self.convert())

        # Conversion Input Area
        conv_frame = tk.Frame(container, bg=Theme.current["BG_SURFACE"])
        conv_frame.pack(fill="x", padx=20, pady=10)

        # From Panel
        from_frame = tk.Frame(conv_frame, bg=Theme.current["BG_SURFACE"])
        from_frame.pack(side="left", expand=True, fill="both")
        
        self.amt_var = tk.StringVar(value="1")
        self.amt_var.trace_add("write", lambda *args: self.convert())
        
        # Flat Modern Entry
        self.amt_entry = tk.Entry(from_frame, textvariable=self.amt_var, font=(font_choice, 28, "bold"), justify="center", 
                                  bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"], relief="flat", insertbackground=Theme.current["TEXT_WHITE"], highlightthickness=1, highlightbackground=Theme.current["BORDER"], highlightcolor=Theme.current["ACCENT"])
        self.amt_entry.pack(fill="x", pady=(0, 10), ipady=10)
        
        self.from_unit = ttk.Combobox(from_frame, state="readonly", font=(font_choice, 9), style="Modern.TCombobox")
        self.from_unit.pack(fill="x")
        self.from_unit.bind("<<ComboboxSelected>>", lambda e: self.convert())

        # Swap Button
        swap_frame = tk.Frame(conv_frame, bg=Theme.current["BG_SURFACE"])
        swap_frame.pack(side="left", padx=20, pady=(0, 25))
        swap_btn = RoundedButton(swap_frame, text="⇄", command=self.swap_units, width=45, height=45, bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"])
        swap_btn.pack()

        # To Panel
        to_frame = tk.Frame(conv_frame, bg=Theme.current["BG_SURFACE"])
        to_frame.pack(side="left", expand=True, fill="both")
        
        self.res_var = tk.StringVar(value="")
        self.res_entry = tk.Entry(to_frame, textvariable=self.res_var, font=(font_choice, 28, "bold"), justify="center", 
                                  bg=Theme.current["BG_MAIN"], fg=Theme.current["ACCENT"], relief="flat", state="readonly", readonlybackground=Theme.current["BG_MAIN"], highlightthickness=1, highlightbackground=Theme.current["BORDER"])
        self.res_entry.pack(fill="x", pady=(0, 10), ipady=10)
        
        self.to_unit = ttk.Combobox(to_frame, state="readonly", font=(font_choice, 9), style="Modern.TCombobox")
        self.to_unit.pack(fill="x")
        self.to_unit.bind("<<ComboboxSelected>>", lambda e: self.convert())

        # Footer / Result Bar
        footer_frame = tk.Frame(container, bg=Theme.current["BG_SURFACE"])
        footer_frame.pack(fill="x", padx=20, pady=(20, 15))

        self.result_lbl = tk.Label(footer_frame, text="", font=(font_choice, 10), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"])
        self.result_lbl.pack(side="left")

        # Feature: Copy to Clipboard
        RoundedButton(footer_frame, text="Copy Result", command=self.copy_result, width=120, height=30, bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"]).pack(side="right")

        # Initialization Routine
        self.on_category_change()

    def on_category_change(self, event=None):
        cat = self.cat_var.get()
        units = self.categories[cat]
        self.from_unit.config(values=units)
        self.to_unit.config(values=units)
        self.from_unit.current(0)
        self.to_unit.current(1 if len(units) > 1 else 0)
        self.convert()

    def swap_units(self):
        u1, u2 = self.from_unit.get(), self.to_unit.get()
        self.from_unit.set(u2)
        self.to_unit.set(u1)
        self.convert()

    def copy_result(self):
        val = self.res_var.get()
        if val and val != "---":
            self.clipboard_clear()
            self.clipboard_append(val)
            messagebox.showinfo("Copied", "Conversion result copied to clipboard!", parent=self)

    def convert(self):
        val_str = self.amt_var.get().strip()
        if not val_str:
            self.res_var.set("")
            self.result_lbl.config(text="Enter a value to begin translation.")
            return
            
        try:
            amt = float(val_str)
            u1 = self.from_unit.get()
            u2 = self.to_unit.get()
            cat = self.cat_var.get()
            prec = int(self.prec_var.get().split()[0])

            res = 0.0

            if cat == "Temperature":
                if u1 == u2: res = amt
                elif u1 == "Celsius" and u2 == "Fahrenheit": res = (amt * 9/5) + 32
                elif u1 == "Celsius" and u2 == "Kelvin": res = amt + 273.15
                elif u1 == "Fahrenheit" and u2 == "Celsius": res = (amt - 32) * 5/9
                elif u1 == "Fahrenheit" and u2 == "Kelvin": res = (amt - 32) * 5/9 + 273.15
                elif u1 == "Kelvin" and u2 == "Celsius": res = amt - 273.15
                elif u1 == "Kelvin" and u2 == "Fahrenheit": res = (amt - 273.15) * 9/5 + 32
            else:
                # Dynamic base-unit conversion matrix
                base_factors = {
                    "Meters": 1, "Kilometers": 1000, "Centimeters": 0.01, "Miles": 1609.344, "Feet": 0.3048, "Inches": 0.0254,
                    "Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495,
                    "Bytes": 1, "Kilobytes": 1024, "Megabytes": 1024**2, "Gigabytes": 1024**3, "Terabytes": 1024**4,
                    "Liters": 1, "Milliliters": 0.001, "Gallons": 3.78541, "Fluid Ounces": 0.0295735,
                    "Seconds": 1, "Minutes": 60, "Hours": 3600, "Days": 86400, "Weeks": 604800, "Years": 31536000,
                    "Meters/Second": 1, "Kilometers/Hour": 1/3.6, "Miles/Hour": 0.44704, "Knots": 0.514444
                }
                if u1 in base_factors and u2 in base_factors:
                    base_val = amt * base_factors[u1]
                    res = base_val / base_factors[u2]

            # Intelligent formatting based on dynamic precision
            res_fmt = f"{res:.{prec}f}".rstrip('0').rstrip('.') if '.' in f"{res:.{prec}f}" else f"{res:.{prec}f}"
            if "e" in str(res): res_fmt = f"{res:.{prec}e}" 

            self.res_var.set(res_fmt)
            self.result_lbl.config(text=f"Formula: {amt} {u1} = {res_fmt} {u2}")

        except ValueError:
            self.res_var.set("---")
            self.result_lbl.config(text="Invalid numeric sequence detected.")

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Initializing")
        self.geometry("500x300")
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="#FFFFFF") 
        
        x = (self.winfo_screenwidth() // 2) - 250
        y = (self.winfo_screenheight() // 2) - 150
        self.geometry(f"+{x}+{y}")
        
        tk.Frame(self, bg="#2563EB", height=4).pack(fill="x", side="top")
        
        tk.Label(self, text="WhatsApp Analytics", font=('Inter', 22, 'bold'), bg="#FFFFFF", fg="#0F172A").pack(pady=(60, 5))
        tk.Label(self, text="Enterprise Edition", font=('Inter', 12), bg="#FFFFFF", fg="#64748B").pack()
        
        self.loading_text = tk.StringVar(value="Initializing core services...")
        tk.Label(self, textvariable=self.loading_text, font=('Inter', 9), bg="#FFFFFF", fg="#94A3B8").pack(pady=(50, 10))
        
        style = ttk.Style()
        style.configure("TProgressbar", thickness=2, background="#2563EB")
        self.progress = ttk.Progressbar(self, mode='determinate', length=300, style="TProgressbar")
        self.progress.pack()
        
        self._simulate_load()
        
    def _simulate_load(self):
        steps = [
            (300, "Loading Natural Language Processors...", 15),
            (600, "Compiling Corporate Lexicons...", 35),
            (900, "Initializing Fault-Tolerant Engines...", 55),
            (1200, "Configuring Graphical Subsystems...", 75),
            (1500, "Applying Minimalist Design Tokens...", 90),
            (1800, "Ready.", 100)
        ]
        for delay, text, val in steps:
            self.after(delay, lambda t=text, v=val: self._update_splash(t, v))
        self.after(2200, self.destroy)
        
    def _update_splash(self, text, val):
        self.loading_text.set(text)
        self.progress['value'] = val


# ==============================================================================
# GUI: MAIN APPLICATION
# ==============================================================================

class WhatsAppAnalyzerPro(tk.Tk):
    """
    Main Tkinter application for WhatsApp chat analytics.
    Modern, minimalist SaaS architecture layout.
    """

    def __init__(self):
        super().__init__()
        self.withdraw()
        
        splash = SplashScreen(self)
        self.wait_window(splash)
        
        self.deiconify()
        self.title("Communications Analytics - Enterprise Edition")
        
        self.geometry("1366x768")
        self.resizable(False, False) 
        
        self.df_full = pd.DataFrame()
        self.df = pd.DataFrame()
        self.analyzer: AdvancedAnalyzer | None = None
        self.current_file_path = None

        self.wrap_messages = tk.BooleanVar(value=True)
        self.show_system_messages = tk.BooleanVar(value=False)

        self._apply_theme()
        self._setup_menu()
        self._setup_shortcuts()
        self._build_layout()

    # ------------------------------------------
    # STYLES, MENU, SHORTCUTS, THEMES
    # ------------------------------------------

    def _apply_theme(self):
        self.configure(bg=Theme.current["BG_MAIN"])
        font_name = Theme.current_font
        style = ttk.Style()
        try: style.theme_use('clam')
        except: pass

        style.configure(
            "Treeview",
            background=Theme.current["BG_SURFACE"],
            foreground=Theme.current["TEXT_WHITE"],
            fieldbackground=Theme.current["BG_SURFACE"],
            borderwidth=0,
            rowheight=35,
            font=(font_name, 9)
        )
        style.configure(
            "Treeview.Heading",
            background=Theme.current["BG_MAIN"],
            foreground=Theme.current["TEXT_GRAY"],
            font=(font_name, 9, "bold"),
            relief="flat",
            padding=5
        )
        style.map("Treeview", background=[('selected', Theme.current["ACCENT"])], foreground=[('selected', "#FFFFFF")])
        style.configure(".", font=(font_name, 9), background=Theme.current["BG_MAIN"], foreground=Theme.current["TEXT_WHITE"])
        
        # --- Minimalist Scrollbar Styling (No Arrows, Flat) ---
        style.layout('Vertical.TScrollbar', [
            ('Vertical.Scrollbar.trough', {
                'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})],
                'sticky': 'ns'
            })
        ])
        style.layout('Horizontal.TScrollbar', [
            ('Horizontal.Scrollbar.trough', {
                'children': [('Horizontal.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})],
                'sticky': 'we'
            })
        ])
        style.configure('TScrollbar', 
            troughcolor=Theme.current["BG_MAIN"], 
            background=Theme.current["BORDER"],
            bordercolor=Theme.current["BG_MAIN"],
            darkcolor=Theme.current["BG_MAIN"],
            lightcolor=Theme.current["BG_MAIN"],
            relief='flat'
        )
        style.map('TScrollbar', 
            background=[('active', Theme.current["TEXT_GRAY"])],
            troughcolor=[('active', Theme.current["BG_MAIN"])]
        )

        # --- Advanced Dropdown (Combobox) Minimalist Styling ---
        self.option_add('*TCombobox*Listbox.background', Theme.current["BG_SURFACE"])
        self.option_add('*TCombobox*Listbox.foreground', Theme.current["TEXT_WHITE"])
        self.option_add('*TCombobox*Listbox.selectBackground', Theme.current["ACCENT"])
        self.option_add('*TCombobox*Listbox.selectForeground', '#FFFFFF')
        self.option_add('*TCombobox*Listbox.font', (font_name, 9))
        self.option_add('*TCombobox*Listbox.relief', 'flat')
        self.option_add('*TCombobox*Listbox.borderwidth', 0)
        self.option_add('*TCombobox*Listbox.selectBorderWidth', 0)
        self.option_add('*TCombobox*Listbox.activeStyle', 'none')
        
        style.layout('Modern.TCombobox', [
            ('Combobox.field', {'sticky': 'nswe', 'children': [
                ('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [
                    ('Combobox.textarea', {'sticky': 'nswe'})
                ]}),
                ('Combobox.downarrow', {'side': 'right', 'sticky': 'ns'})
            ]})
        ])
        
        style.configure('Modern.TCombobox',
            background=Theme.current["BG_SURFACE"],
            fieldbackground=Theme.current["BG_SURFACE"],
            foreground=Theme.current["TEXT_WHITE"],
            bordercolor=Theme.current["BORDER"],
            lightcolor=Theme.current["BG_SURFACE"],
            darkcolor=Theme.current["BG_SURFACE"],
            arrowcolor=Theme.current["TEXT_GRAY"],
            arrowsize=14,
            padding=6,
            relief='flat'
        )
        style.map('Modern.TCombobox',
            fieldbackground=[('readonly', Theme.current["BG_SURFACE"])],
            background=[('readonly', Theme.current["BG_SURFACE"])],
            foreground=[('readonly', Theme.current["TEXT_WHITE"])]
        )

        if hasattr(self, 'sidebar'):
            self.sidebar.config(bg=Theme.current["BG_SIDEBAR"])
            self.main_area.config(bg=Theme.current["BG_MAIN"])
            self.header.config(bg=Theme.current["BG_MAIN"])
            self.nav_frame.config(bg=Theme.current["BG_MAIN"])
            
            self.lbl_filename.config(bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"], font=(font_name, 20, "bold"))
            self.lbl_status.config(bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"], font=(font_name, 9))
            self.lbl_date_range.config(bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"], font=(font_name, 10))
            
            # Deep Recursive Styling application for main details frames (Dynamic Updating)
            def update_tree(widget):
                try:
                    w_class = widget.__class__.__name__
                    if w_class in ('Frame', 'LabelFrame', 'Canvas', 'FlatNavButton', 'ScrollableFrame'):
                        if w_class == 'RoundedButton':
                            widget.update_theme_colors()
                        elif w_class == 'FlatNavButton':
                            widget.update_theme_colors()
                        elif w_class == 'ScrollableFrame':
                            widget.update_theme_colors()
                        elif hasattr(widget, 'cget'):
                            # Ensure widgets containing explicit backgrounds get correct surface or main assignments based on thickness
                            bg_color = Theme.current["BG_SURFACE"] if int(widget.cget('highlightthickness')) > 0 else Theme.current["BG_MAIN"]
                            widget.configure(bg=bg_color)
                            if int(widget.cget('highlightthickness')) > 0:
                                widget.configure(highlightbackground=Theme.current["BORDER"])
                    elif w_class == 'Label':
                        widget.configure(bg=widget.master.cget('bg'))
                        font_str = str(widget.cget('font')).lower()
                        # Update text elements dynamically to retain structure
                        if "bold" in font_str and "20" not in font_str and "14" not in font_str:
                            widget.configure(fg=Theme.current["TEXT_WHITE"])
                        elif "bold" not in font_str:
                            widget.configure(fg=Theme.current["TEXT_GRAY"])

                    for child in widget.winfo_children():
                        if child.__class__.__name__ not in ('InfoCard', 'NavTab', 'FlatNavButton', 'RoundedButton'):
                            update_tree(child)
                except Exception:
                    pass

            # Force updates upon primary components
            if hasattr(self, 'content_container'):
                update_tree(self.content_container)
            if hasattr(self, 'sidebar'):
                update_tree(self.sidebar)

            # Update specialized widgets explicitly calling their specific handlers
            if hasattr(self, 'nav_buttons'):
                for btn in self.nav_buttons.values():
                    if hasattr(btn, 'update_theme_colors'): btn.update_theme_colors()
                        
            if hasattr(self, 'card_msgs'):
                # Add all info cards dynamically if they exist
                cards_to_update = [self.card_msgs, self.card_words, self.card_media, self.card_links, 
                                   self.card_sentiment, self.card_participants, self.card_avg_words, self.card_peak_hour]
                if hasattr(self, 'card_fastest'):
                    cards_to_update.extend([self.card_fastest, self.card_initiator, self.card_double_text])
                if hasattr(self, 'card_total_conflicts'):
                    cards_to_update.extend([self.card_total_conflicts, self.card_instigator, self.card_tense_day])
                if hasattr(self, 'card_pos_sentiment'):
                    cards_to_update.extend([self.card_pos_sentiment, self.card_neg_sentiment, self.card_top_pos, self.card_top_neg])
                for card in cards_to_update:
                    if hasattr(card, 'update_theme_colors'): card.update_theme_colors()

    def _setup_menu(self):
        menubar = tk.Menu(self, bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"], relief="flat")

        file_menu = tk.Menu(menubar, tearoff=0, bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"], relief="flat")
        file_menu.add_command(label="Import Dataset... (Ctrl+O)", command=self.load_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save Filtered CSV", command=self.export_csv)
        file_menu.add_command(label="Export Summary to PDF", command=self.export_pdf_report)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        tools_menu = tk.Menu(menubar, tearoff=0, bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"], relief="flat")
        tools_menu.add_command(label="Advanced Query... (Ctrl+F)", command=self.open_search_dialog)
        tools_menu.add_command(label="Participant Comparison", command=lambda: UserCompareGUI(self))
        tools_menu.add_command(label="Data Anonymization", command=lambda: ChatAnonymizerGUI(self))
        tools_menu.add_separator()
        tools_menu.add_command(label="Preferences", command=lambda: ThemeSettingsWindow(self))
        menubar.add_cascade(label="Tools", menu=tools_menu)

        view_menu = tk.Menu(menubar, tearoff=0, bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"], relief="flat")
        view_menu.add_checkbutton(label="Wrap Message Text", variable=self.wrap_messages, command=self.refresh_message_log)
        view_menu.add_checkbutton(label="Show System Logs", variable=self.show_system_messages, command=self.apply_filter)
        menubar.add_cascade(label="View", menu=view_menu)

        self.config(menu=menubar)

    def _setup_shortcuts(self):
        self.bind("<Control-o>", lambda e: self.load_file())
        self.bind("<Control-f>", lambda e: self.open_search_dialog())
        self.bind("<F5>", lambda e: self.refresh_dashboard())

    # ------------------------------------------
    # LAYOUT & CUSTOM NAVIGATION
    # ------------------------------------------

    def _build_layout(self):
        self.sidebar_container = tk.Frame(self, bg=Theme.current["BORDER"], width=261)
        self.sidebar_container.pack(side="left", fill="y")
        self.sidebar_container.pack_propagate(False)

        self.sidebar = tk.Frame(self.sidebar_container, bg=Theme.current["BG_SIDEBAR"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self._build_sidebar()

        self.main_area = tk.Frame(self, bg=Theme.current["BG_MAIN"])
        self.main_area.pack(side="right", fill="both", expand=True, padx=30, pady=30)

        self.header = tk.Frame(self.main_area, bg=Theme.current["BG_MAIN"])
        self.header.pack(fill="x", pady=(0, 20))

        self.lbl_filename = tk.Label(self.header, text="Workspace Idle", font=(Theme.current_font, 20, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"])
        self.lbl_filename.pack(side="left")

        self.lbl_status = tk.Label(self.header, text="Awaiting Dataset Import", font=(Theme.current_font, 9), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"])
        self.lbl_status.pack(side="right", anchor="s", pady=5)

        self.lbl_date_range = tk.Label(self.main_area, text="Import a standard WhatsApp text export to initiate analytics engine.", font=(Theme.current_font, 10), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"])
        self.lbl_date_range.pack(anchor="w", pady=(0, 15))

        # CUSTOM MODERN NAVIGATION BAR
        self.nav_frame = tk.Frame(self.main_area, bg=Theme.current["BG_MAIN"])
        self.nav_frame.pack(fill="x", pady=(0, 10))
        
        # Separation Line
        tk.Frame(self.main_area, bg=Theme.current["BORDER"], height=1).pack(fill="x", pady=(0, 15))
        
        self.content_container = tk.Frame(self.main_area, bg=Theme.current["BG_MAIN"])
        self.content_container.pack(fill="both", expand=True)

        self.tabs = {}
        self.nav_buttons = {}
        self.current_tab = None
        
        tab_names = ["Overview", "Timeline", "Activity", "Engagement", "Topics", "Conflicts", "Accolades", "Lexicon", "Sentiment", "Log View"]
        
        for name in tab_names:
            btn = NavTab(self.nav_frame, text=name, command=self._select_tab)
            btn.pack(side="left", padx=(0, 5))
            self.nav_buttons[name] = btn
            
            frame = tk.Frame(self.content_container, bg=Theme.current["BG_MAIN"])
            self.tabs[name] = frame

        self._init_tab_overview()
        self._init_tab_timeline()
        self._init_tab_activity()
        self._init_tab_engagement()
        self._init_tab_topics()
        self._init_tab_conflicts()
        self._init_tab_trophies()
        self._init_tab_words_media()
        self._init_tab_sentiment()
        self._init_tab_text()
        
        self._select_tab("Overview")

    def _select_tab(self, tab_name):
        if self.current_tab:
            self.nav_buttons[self.current_tab].set_active(False)
            self.tabs[self.current_tab].pack_forget()
            
        self.current_tab = tab_name
        self.nav_buttons[tab_name].set_active(True)
        self.tabs[tab_name].pack(fill="both", expand=True)

    def _build_sidebar(self):
        lbl_app = tk.Label(self.sidebar, text="WhatsApp Chat", font=(Theme.current_font, 14, "bold"), bg=Theme.current["BG_SIDEBAR"], fg=Theme.current["TEXT_WHITE"])
        lbl_app.pack(pady=(30, 2), padx=25, anchor="w")

        lbl_sub = tk.Label(self.sidebar, text="Analyzer", font=(Theme.current_font, 9), bg=Theme.current["BG_SIDEBAR"], fg=Theme.current["TEXT_GRAY"], justify="left")
        lbl_sub.pack(padx=25, anchor="w", pady=(0, 30))

        RoundedButton(self.sidebar, text="Import Dataset", command=self.load_file, width=210).pack(padx=25, pady=8)
        RoundedButton(self.sidebar, text="Export to PDF", command=self.export_pdf_report, width=210).pack(padx=25, pady=8)

        tk.Label(self.sidebar, text="DATA FILTERS", font=(Theme.current_font, 8, "bold"), bg=Theme.current["BG_SIDEBAR"], fg=Theme.current["TEXT_GRAY"]).pack(anchor="w", padx=25, pady=(30, 10))
        
        tk.Label(self.sidebar, text="Participant:", font=(Theme.current_font, 9), bg=Theme.current["BG_SIDEBAR"], fg=Theme.current["TEXT_WHITE"]).pack(anchor="w", padx=25)
        self.combo_users = ttk.Combobox(self.sidebar, state="readonly", values=["All Participants"], font=(Theme.current_font, 9), style="Modern.TCombobox")
        self.combo_users.current(0)
        self.combo_users.pack(fill="x", padx=25, pady=(5, 10))

        FlatNavButton(self.sidebar, text="Apply Filter", command=self.apply_filter, anchor="w").pack(pady=0, fill="x")
        
        tk.Label(self.sidebar, text="UTILITIES", font=(Theme.current_font, 8, "bold"), bg=Theme.current["BG_SIDEBAR"], fg=Theme.current["TEXT_GRAY"]).pack(anchor="w", padx=25, pady=(30, 10))

        tools = [
            ("Tracker", lambda: HabitTrackerGUI(self)),
            ("Converter", lambda: AdvancedUnitConverterGUI(self)),
            ("Deep Query", self.open_search_dialog),
            ("App Guide", lambda: UserGuideGUI(self))
        ]
        
        for text, cmd in tools:
            FlatNavButton(self.sidebar, text=text, command=cmd, anchor="w").pack(pady=2, fill="x")

    # ==========================================
    # TAB UI INITIALIZERS (CLEAN GRAPHS WITH DYNAMIC TOGGLES)
    # ==========================================

    def _create_chart_controls(self, parent_frame, title, default_type, redraw_command):
        top = tk.Frame(parent_frame, bg=Theme.current["BG_SURFACE"])
        top.pack(fill='x', pady=5)
        
        tk.Label(top, text=title, font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(side='left', padx=15)
        
        var = tk.StringVar(value=default_type)
        combo = ttk.Combobox(top, textvariable=var, values=["Bar Chart", "Pie Chart", "Line Chart", "Area Chart"], state="readonly", width=12, font=(Theme.current_font, 8), style="Modern.TCombobox")
        combo.pack(side='right', padx=(5, 15))
        
        FlatNavButton(top, text="Refresh", command=redraw_command).pack(side='right', padx=5)
        
        return var

    def _init_tab_overview(self):
        # Top KPI Row
        kpi_row_1 = tk.Frame(self.tabs["Overview"], bg=Theme.current["BG_MAIN"])
        kpi_row_1.pack(fill="x", pady=(0, 10))

        self.card_msgs = InfoCard(kpi_row_1, "Total Volume", "", width=180)
        self.card_msgs.pack(side="left", padx=(0, 10))
        self.card_words = InfoCard(kpi_row_1, "Word Density", "", width=180)
        self.card_words.pack(side="left", padx=(0, 10))
        self.card_media = InfoCard(kpi_row_1, "Media Assets", "", width=180)
        self.card_media.pack(side="left", padx=(0, 10))
        self.card_links = InfoCard(kpi_row_1, "External Links", "", width=180)
        self.card_links.pack(side="left", padx=(0, 10))
        self.card_sentiment = InfoCard(kpi_row_1, "Macro Sentiment", "", width=180)
        self.card_sentiment.pack(side="left")

        # Bottom KPI Row (Expanded Features)
        kpi_row_2 = tk.Frame(self.tabs["Overview"], bg=Theme.current["BG_MAIN"])
        kpi_row_2.pack(fill="x", pady=(0, 15))
        
        self.card_participants = InfoCard(kpi_row_2, "Active Participants", "", width=180)
        self.card_participants.pack(side="left", padx=(0, 10))
        self.card_avg_words = InfoCard(kpi_row_2, "Avg Words / Msg", "", width=180)
        self.card_avg_words.pack(side="left", padx=(0, 10))
        self.card_peak_hour = InfoCard(kpi_row_2, "Peak Activity Hour", "", width=180)
        self.card_peak_hour.pack(side="left", padx=(0, 10))

        # Two side-by-side charts for better overview
        charts_frame = tk.Frame(self.tabs["Overview"], bg=Theme.current["BG_MAIN"])
        charts_frame.pack(fill="both", expand=True)

        # Participant Chart
        self.frame_user_chart = tk.Frame(charts_frame, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_user_chart.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        self.chart_type_user = self._create_chart_controls(
            self.frame_user_chart, "Activity Distribution", "Bar Chart", 
            self.plot_user_distribution
        )
        self.frame_user_plot = tk.Frame(self.frame_user_chart, bg=Theme.current["BG_SURFACE"])
        self.frame_user_plot.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Message Types Chart
        self.frame_msg_type_chart = tk.Frame(charts_frame, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_msg_type_chart.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        self.chart_type_msg_types = self._create_chart_controls(
            self.frame_msg_type_chart, "Message Composition", "Pie Chart", 
            self.plot_msg_types
        )
        self.frame_msg_type_plot = tk.Frame(self.frame_msg_type_chart, bg=Theme.current["BG_SURFACE"])
        self.frame_msg_type_plot.pack(fill='both', expand=True, padx=10, pady=10)

    def _init_tab_timeline(self):
        self.frame_timeline = tk.Frame(self.tabs["Timeline"], bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_timeline.pack(fill="both", expand=True, pady=10)
        
        self.chart_type_timeline = self._create_chart_controls(
            self.frame_timeline, "Temporal Volume Analysis", "Area Chart", 
            self.plot_timeline
        )
        self.frame_timeline_plot = tk.Frame(self.frame_timeline, bg=Theme.current["BG_SURFACE"])
        self.frame_timeline_plot.pack(fill='both', expand=True, padx=10, pady=10)

    def _init_tab_activity(self):
        # Convert base tab to scrollable layout
        self.scroll_activity = ScrollableFrame(self.tabs["Activity"], bg=Theme.current["BG_MAIN"])
        self.scroll_activity.pack(fill='both', expand=True)
        scroll_container = self.scroll_activity.scrollable_container

        # Heatmap (Stacked Vertically)
        self.frame_heatmap = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_heatmap.pack(fill="x", expand=True, padx=10, pady=(10, 5))
        
        btn_frame1 = tk.Frame(self.frame_heatmap, bg=Theme.current["BG_SURFACE"])
        btn_frame1.pack(fill='x', pady=5)
        tk.Label(btn_frame1, text="Density Matrix (Day/Hour)", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(side='left', padx=15)
        
        self.frame_heat_plot = tk.Frame(self.frame_heatmap, bg=Theme.current["BG_SURFACE"])
        self.frame_heat_plot.pack(fill='both', expand=True, padx=10, pady=10)

        # Hourly Activity (Stacked Vertically)
        self.frame_hourly = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_hourly.pack(fill="x", expand=True, padx=10, pady=5)
        
        self.chart_type_hourly = self._create_chart_controls(self.frame_hourly, "Intraday Velocity", "Line Chart", self.plot_hourly_activity)
        self.frame_hour_plot = tk.Frame(self.frame_hourly, bg=Theme.current["BG_SURFACE"])
        self.frame_hour_plot.pack(fill='both', expand=True, padx=10, pady=10)

        # Weekday Activity (Stacked Vertically)
        self.frame_weekday = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_weekday.pack(fill="x", expand=True, padx=10, pady=(5, 15))
        
        self.chart_type_weekday = self._create_chart_controls(self.frame_weekday, "Weekly Distribution", "Bar Chart", self.plot_weekday_activity)
        self.frame_week_plot = tk.Frame(self.frame_weekday, bg=Theme.current["BG_SURFACE"])
        self.frame_week_plot.pack(fill='both', expand=True, padx=10, pady=10)

    def _init_tab_engagement(self):
        # Convert base tab to scrollable layout
        self.scroll_engagement = ScrollableFrame(self.tabs["Engagement"], bg=Theme.current["BG_MAIN"])
        self.scroll_engagement.pack(fill='both', expand=True)
        scroll_container = self.scroll_engagement.scrollable_container
        
        # Top KPI Row
        kpi_row = tk.Frame(scroll_container, bg=Theme.current["BG_MAIN"])
        kpi_row.pack(fill="x", padx=10, pady=(10, 15))
        
        self.card_fastest = InfoCard(kpi_row, "Fastest Responder", "", width=250)
        self.card_fastest.pack(side="left", padx=(0, 10))
        self.card_initiator = InfoCard(kpi_row, "Top Initiator", "", width=250)
        self.card_initiator.pack(side="left", padx=(0, 10))
        self.card_double_text = InfoCard(kpi_row, "Highest Double-Texter", "", width=250)
        self.card_double_text.pack(side="left", padx=(0, 10))
        
        # Chart Frame (Stacked Vertically)
        self.frame_eng_chart = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_eng_chart.pack(fill="x", expand=True, padx=10, pady=5)
        
        self.chart_type_eng = self._create_chart_controls(
            self.frame_eng_chart, "Avg Response Delay", "Bar Chart", 
            self.plot_engagement_chart
        )
        self.frame_eng_plot = tk.Frame(self.frame_eng_chart, bg=Theme.current["BG_SURFACE"])
        self.frame_eng_plot.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview Frame (Stacked Vertically)
        tree_frame = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        tree_frame.pack(fill="x", expand=True, padx=10, pady=(5, 15))
        
        tk.Label(tree_frame, text="Participant Engagement Matrix", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(anchor="w", padx=15, pady=(15, 5))
        tk.Label(tree_frame, text="Initiations count pauses > 8 hours.", font=(Theme.current_font, 9), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(anchor="w", padx=15, pady=(0, 10))
        
        self.tree_eng = ttk.Treeview(tree_frame, columns=("Sender", "Avg Resp (m)", "Starters", "Msgs/Turn", "Max Silence (h)"), show="headings", height=8)
        self.tree_eng.heading("Sender", text="Participant Identity")
        self.tree_eng.heading("Avg Resp (m)", text="Avg Response Delay (mins)")
        self.tree_eng.heading("Starters", text="Conversation Initiations")
        self.tree_eng.heading("Msgs/Turn", text="Messages Per Turn")
        self.tree_eng.heading("Max Silence (h)", text="Max Silence Broken (hrs)")
        
        # Expanded column widths to perfectly fill the UI space
        self.tree_eng.column("Sender", width=250, anchor='w')
        self.tree_eng.column("Avg Resp (m)", width=180, anchor='center')
        self.tree_eng.column("Starters", width=180, anchor='center')
        self.tree_eng.column("Msgs/Turn", width=160, anchor='center')
        self.tree_eng.column("Max Silence (h)", width=200, anchor='center')
        
        self.tree_eng.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def _init_tab_topics(self):
        self.frame_topics = tk.Frame(self.tabs["Topics"], bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_topics.pack(fill="both", expand=True, pady=10)
        
        self.chart_type_topics = self._create_chart_controls(
            self.frame_topics, "Categorical Subject Dispersion", "Bar Chart", 
            self.plot_topics
        )
        self.frame_topics_plot = tk.Frame(self.frame_topics, bg=Theme.current["BG_SURFACE"])
        self.frame_topics_plot.pack(fill='both', expand=True, padx=10, pady=10)

    def _init_tab_conflicts(self):
        # Convert base tab to scrollable layout
        self.scroll_conflicts = ScrollableFrame(self.tabs["Conflicts"], bg=Theme.current["BG_MAIN"])
        self.scroll_conflicts.pack(fill='both', expand=True)
        scroll_container = self.scroll_conflicts.scrollable_container
        
        # Header / Explanation
        header_frame = tk.Frame(scroll_container, bg=Theme.current["BG_MAIN"])
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        tk.Label(header_frame, text="Toxicity & Conflict Identification", font=(Theme.current_font, 14, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"]).pack(anchor='w')
        explanation = "This module scans the dataset against an offline NLP lexicon of hostile, aggressive, and high-stress terminology. It identifies peak tension periods, primary instigators, and the specific vocabulary driving the conflict."
        tk.Label(header_frame, text=explanation, font=(Theme.current_font, 9), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"], justify="left", wraplength=900).pack(anchor='w', pady=(5, 10))
        
        # KPIs
        kpi_row = tk.Frame(scroll_container, bg=Theme.current["BG_MAIN"])
        kpi_row.pack(fill="x", padx=10, pady=(0, 15))
        
        self.card_total_conflicts = InfoCard(kpi_row, "Hostile Markers", "⚠️", width=250)
        self.card_total_conflicts.pack(side="left", padx=(0, 10))
        self.card_instigator = InfoCard(kpi_row, "Primary Instigator", "👤", width=250)
        self.card_instigator.pack(side="left", padx=(0, 10))
        self.card_tense_day = InfoCard(kpi_row, "Peak Tension Date", "📅", width=250)
        self.card_tense_day.pack(side="left", padx=(0, 10))
        
        # Left Chart (Timeline) -> Now Full Width
        self.frame_conf_chart = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_conf_chart.pack(fill="x", expand=True, padx=10, pady=(0, 15))
        
        self.chart_type_conf = self._create_chart_controls(
            self.frame_conf_chart, "Tension Timeline", "Line Chart", 
            self.plot_conflict_chart
        )
        tk.Label(self.frame_conf_chart, text="Visualizes the frequency of hostile terminology over time. Spikes indicate high-stress events or arguments.", font=(Theme.current_font, 9, "italic"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(anchor='w', padx=15, pady=(0, 5))

        self.frame_conf_plot = tk.Frame(self.frame_conf_chart, bg=Theme.current["BG_SURFACE"])
        self.frame_conf_plot.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Instigators Tree -> Now Full Width
        inst_frame = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        inst_frame.pack(fill="x", expand=True, padx=10, pady=(0, 15))
        tk.Label(inst_frame, text="Participant Tension Index", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(anchor="w", padx=15, pady=(10, 0))
        tk.Label(inst_frame, text="Ranks participants based on their total usage of words found in the conflict lexicon. Higher numbers indicate a higher propensity for aggressive phrasing.", font=(Theme.current_font, 9, "italic"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], justify="left", wraplength=900).pack(anchor="w", padx=15, pady=(2, 10))

        self.tree_instigators = ttk.Treeview(inst_frame, columns=("Participant", "Hostile Terms"), show="headings", height=6)
        self.tree_instigators.heading("Participant", text="Participant Identity")
        self.tree_instigators.heading("Hostile Terms", text="Hostile Terms Used (Count)")
        self.tree_instigators.column("Participant", width=400, anchor='w')
        self.tree_instigators.column("Hostile Terms", width=200, anchor='center')
        self.tree_instigators.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Words Tree -> Now Full Width
        words_frame = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        words_frame.pack(fill="x", expand=True, padx=10, pady=(0, 15))
        tk.Label(words_frame, text="Common Triggers (Lexicon Analysis)", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(anchor="w", padx=15, pady=(10, 0))
        tk.Label(words_frame, text="Displays the specific trigger words from the NLP lexicon that appeared most frequently during the analyzed period.", font=(Theme.current_font, 9, "italic"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"], justify="left", wraplength=900).pack(anchor="w", padx=15, pady=(2, 10))

        self.tree_conf_words = ttk.Treeview(words_frame, columns=("Trigger Word", "Occurrences"), show="headings", height=6)
        self.tree_conf_words.heading("Trigger Word", text="Lexicon Trigger Word")
        self.tree_conf_words.heading("Occurrences", text="Total Occurrences")
        self.tree_conf_words.column("Trigger Word", width=400, anchor='w')
        self.tree_conf_words.column("Occurrences", width=200, anchor='center')
        self.tree_conf_words.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def _init_tab_trophies(self):
        self.scroll_accolades = ScrollableFrame(self.tabs["Accolades"], bg=Theme.current["BG_MAIN"])
        self.scroll_accolades.pack(fill='both', expand=True)
        scroll_container = self.scroll_accolades.scrollable_container
        
        tk.Label(scroll_container, text="Participant Accolades", font=(Theme.current_font, 16, "bold"), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_WHITE"]).pack(anchor='w', pady=(15, 5), padx=20)
        tk.Label(scroll_container, text="Algorithmic recognition of behavioral communication patterns.", font=(Theme.current_font, 9), bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"]).pack(anchor='w', padx=20, pady=(0, 20))
        
        self.frame_trophies_content = tk.Frame(scroll_container, bg=Theme.current["BG_MAIN"])
        self.frame_trophies_content.pack(fill='both', expand=True, padx=10)

    def _init_tab_words_media(self):
        # Convert base tab to scrollable layout to accommodate expansions
        self.scroll_lexicon = ScrollableFrame(self.tabs["Lexicon"], bg=Theme.current["BG_MAIN"])
        self.scroll_lexicon.pack(fill='both', expand=True)
        scroll_container = self.scroll_lexicon.scrollable_container

        # Top Row: Wordcloud (Full width)
        self.frame_wc = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_wc.pack(fill='x', expand=True, padx=10, pady=(10, 5))
        
        btn_frame = tk.Frame(self.frame_wc, bg=Theme.current["BG_SURFACE"])
        btn_frame.pack(fill='x', pady=5)
        self.var_sw = tk.BooleanVar(value=False)
        ttk.Checkbutton(btn_frame, text="Retain Stopwords", variable=self.var_sw, command=self.plot_wordcloud).pack(side='left', padx=15)
        
        self.frame_wc_plot = tk.Frame(self.frame_wc, bg=Theme.current["BG_SURFACE"])
        self.frame_wc_plot.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Domains (Stacked Vertically)
        self.frame_domains = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_domains.pack(fill='x', expand=True, padx=10, pady=(5, 5))
        tk.Label(self.frame_domains, text="Domain Dissemination", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(pady=10, anchor="w", padx=15)
        self.tree_domains = ttk.Treeview(self.frame_domains, columns=("Domain", "Count"), show="headings", height=6)
        self.tree_domains.heading("Domain", text="Root Domain")
        self.tree_domains.heading("Count", text="Freq")
        self.tree_domains.pack(fill='both', expand=True, padx=15, pady=(0,15))
        
        # Emojis (Stacked Vertically)
        self.frame_emojis = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_emojis.pack(fill='x', expand=True, padx=10, pady=5)
        tk.Label(self.frame_emojis, text="Emoji Frequency Matrix", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(pady=10, anchor="w", padx=15)
        self.tree_emojis = ttk.Treeview(self.frame_emojis, columns=("Emoji", "Meaning", "Count"), show="headings", height=6)
        self.tree_emojis.heading("Emoji", text="Glyph")
        self.tree_emojis.heading("Meaning", text="Definition")
        self.tree_emojis.heading("Count", text="Freq")
        self.tree_emojis.column("Emoji", width=50, anchor="center")
        self.tree_emojis.column("Meaning", width=150, anchor="w")
        self.tree_emojis.column("Count", width=50, anchor="center")
        self.tree_emojis.pack(fill='both', expand=True, padx=15, pady=(0,15))

        # Micro-expressions (Politeness & Laughter) (Stacked Vertically)
        self.frame_micro = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_micro.pack(fill='x', expand=True, padx=10, pady=5)
        tk.Label(self.frame_micro, text="Micro-Expressions (Lexicon)", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(pady=10, anchor="w", padx=15)
        self.tree_micro = ttk.Treeview(self.frame_micro, columns=("Expression", "Type", "Count"), show="headings", height=6)
        self.tree_micro.heading("Expression", text="Term")
        self.tree_micro.heading("Type", text="Category")
        self.tree_micro.heading("Count", text="Freq")
        self.tree_micro.column("Type", width=80, anchor="center")
        self.tree_micro.column("Count", width=50, anchor="center")
        self.tree_micro.pack(fill='both', expand=True, padx=15, pady=(0,15))

        # Bottom Row: Longest Messages Leaderboard
        self.frame_longest = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_longest.pack(fill='x', expand=True, padx=10, pady=(5, 15))
        tk.Label(self.frame_longest, text="Information Density: Longest Transmissions", font=(Theme.current_font, 10, "bold"), bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_WHITE"]).pack(pady=10, anchor="w", padx=15)
        self.tree_longest = ttk.Treeview(self.frame_longest, columns=("Date", "Sender", "Words", "Preview"), show="headings", height=5)
        self.tree_longest.heading("Date", text="Timestamp")
        self.tree_longest.heading("Sender", text="Participant")
        self.tree_longest.heading("Words", text="Word Count")
        self.tree_longest.heading("Preview", text="Payload Preview")
        self.tree_longest.column("Date", width=120)
        self.tree_longest.column("Sender", width=120)
        self.tree_longest.column("Words", width=80, anchor="center")
        self.tree_longest.column("Preview", width=600)
        self.tree_longest.pack(fill='both', expand=True, padx=15, pady=(0,15))

    def _init_tab_sentiment(self):
        # Convert base tab to scrollable layout
        self.scroll_sentiment = ScrollableFrame(self.tabs["Sentiment"], bg=Theme.current["BG_MAIN"])
        self.scroll_sentiment.pack(fill='both', expand=True)
        scroll_container = self.scroll_sentiment.scrollable_container

        # Top Row: KPIs
        kpi_row = tk.Frame(scroll_container, bg=Theme.current["BG_MAIN"])
        kpi_row.pack(fill="x", padx=10, pady=(10, 15))
        
        self.card_pos_sentiment = InfoCard(kpi_row, "Positive Lexicon Hits", "🟢", width=220)
        self.card_pos_sentiment.pack(side="left", padx=(0, 10))
        self.card_neg_sentiment = InfoCard(kpi_row, "Negative Lexicon Hits", "🔴", width=220)
        self.card_neg_sentiment.pack(side="left", padx=(0, 10))
        self.card_top_pos = InfoCard(kpi_row, "Primary Optimist", "⭐", width=220)
        self.card_top_pos.pack(side="left", padx=(0, 10))
        self.card_top_neg = InfoCard(kpi_row, "Primary Cynic", "🌧️", width=220)
        self.card_top_neg.pack(side="left", padx=(0, 10))

        # Radar Chart (Stacked Vertically)
        self.frame_radar = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_radar.pack(fill='x', expand=True, padx=10, pady=(0, 15))
        
        self.chart_type_radar = self._create_chart_controls(
            self.frame_radar, "Emotional State Mapping", "Bar Chart", 
            self.plot_emotion_radar
        )
        self.frame_radar_plot = tk.Frame(self.frame_radar, bg=Theme.current["BG_SURFACE"])
        self.frame_radar_plot.pack(fill='both', expand=True, padx=10, pady=10)

        # User Sentiment Breakdown Chart (Stacked Vertically)
        self.frame_user_sent = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_user_sent.pack(fill='x', expand=True, padx=10, pady=(0, 15))
        
        self.chart_type_user_sent = self._create_chart_controls(
            self.frame_user_sent, "Participant Sentiment Breakdown", "Bar Chart", 
            self.plot_sentiment_user_bar
        )
        self.frame_user_sent_plot = tk.Frame(self.frame_user_sent, bg=Theme.current["BG_SURFACE"])
        self.frame_user_sent_plot.pack(fill='both', expand=True, padx=10, pady=10)

        # Bottom Row: Sentiment Timeline (Stacked Vertically)
        self.frame_sent_timeline = tk.Frame(scroll_container, bg=Theme.current["BG_SURFACE"], highlightbackground=Theme.current["BORDER"], highlightthickness=1)
        self.frame_sent_timeline.pack(fill="x", expand=True, padx=10, pady=(0, 15))
        
        self.chart_type_sent_time = self._create_chart_controls(
            self.frame_sent_timeline, "Temporal Sentiment Timeline", "Area Chart", 
            self.plot_sentiment_timeline
        )
        self.frame_sent_time_plot = tk.Frame(self.frame_sent_timeline, bg=Theme.current["BG_SURFACE"])
        self.frame_sent_time_plot.pack(fill='both', expand=True, padx=10, pady=10)

    def _init_tab_text(self):
        header = tk.Frame(self.tabs["Log View"], bg=Theme.current["BG_MAIN"])
        header.pack(fill="x", pady=10)
        FlatNavButton(header, text="Initiate Deep Query", command=self.open_search_dialog).pack(side="left")

        frame = tk.Frame(self.tabs["Log View"], bg=Theme.current["BG_MAIN"])
        frame.pack(fill="both", expand=True, pady=(0,10))

        self.tree_msgs = ttk.Treeview(frame, columns=("Date", "Sender", "Message"), show="headings")
        self.tree_msgs.heading("Date", text="Timestamp")
        self.tree_msgs.heading("Sender", text="Participant")
        self.tree_msgs.heading("Message", text="Payload")

        self.tree_msgs.column("Date", width=160, anchor="w")
        self.tree_msgs.column("Sender", width=160, anchor="w")
        self.tree_msgs.column("Message", width=700, anchor="w")

        scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=self.tree_msgs.yview)
        self.tree_msgs.configure(yscrollcommand=scrollbar_y.set)
        self.tree_msgs.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

    # ==========================================
    # LOGIC HANDLING
    # ==========================================

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not filepath: return

        try:
            self.lbl_status.config(text="Processing dataset. Please stand by...")
            self.update_idletasks()

            df = ChatParser.parse_file(filepath)
            if df.empty: raise ValueError("Invalid dataset structure. Ensure uncompressed WhatsApp export.")

            self.df_full = df
            self.df = self.df_full.copy()
            self.analyzer = AdvancedAnalyzer(self.df)
            self.current_file_path = filepath
            
            bname = os.path.basename(filepath)
            bname = bname.replace("WhatsApp Chat with ", "").replace(".txt", "")
            self.lbl_filename.config(text=bname[:30]) 

            senders = sorted(self.df[self.df['sender'] != 'System Notification']['sender'].unique().tolist())
            self.combo_users['values'] = ["All Participants"] + senders
            self.combo_users.current(0)

            self.refresh_dashboard()
            self.lbl_status.config(text=f"Import complete. {len(self.df)} records established.")

        except Exception as e:
            messagebox.showerror("System Error", f"Import failed:\n{str(e)}")
            self.lbl_status.config(text="Status: Import failure.")

    def apply_filter(self):
        if self.df_full.empty: return

        user = self.combo_users.get()
        if user == "All Participants":
            self.df = self.df_full.copy()
        else:
            self.df = self.df_full[self.df_full['sender'] == user].copy()

        if not self.show_system_messages.get():
            self.df = self.df[self.df['sender'] != "System Notification"]

        self.analyzer = AdvancedAnalyzer(self.df)
        self.refresh_dashboard()
        self.lbl_status.config(text=f"Filters active. Analyzing {len(self.df)} records.")

    def export_csv(self):
        if self.df.empty:
            messagebox.showinfo("Action Required", "Load a dataset prior to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            self.df.to_csv(path, index=False)
            messagebox.showinfo("Success", "Dataset exported to local directory.")

    def export_pdf_report(self):
        if self.df_full.empty:
            messagebox.showinfo("Action Required", "Load a dataset to generate a PDF summary.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="enterprise_analytics_report.pdf", filetypes=[("PDF", "*.pdf")])
        if path:
            self.lbl_status.config(text="Compiling modern PDF document...")
            self.update()
            success = PDFReportGenerator.generate_report(self, path)
            if success:
                messagebox.showinfo("Success", "PDF Dashboard generated successfully.")
                if platform.system() == 'Darwin':       # macOS
                    os.system('open "{}"'.format(path))
                elif platform.system() == 'Windows':    # Windows
                    os.system('start "" "{}"'.format(path))
                else:                                   # linux variants
                    os.system('xdg-open "{}"'.format(path))
            else:
                messagebox.showerror("Error", "Filesystem write failed.")
            self.lbl_status.config(text="Status: Ready.")

    # ==========================================
    # DASHBOARD REFRESH & DYNAMIC PLOTTING
    # ==========================================

    def _clear_frame(self, frame):
        for widget in frame.winfo_children(): widget.destroy()

    def _draw_chart(self, ax, chart_type, x_data, y_data, color):
        """Unified method to draw charts with specific modern Pie Chart logic."""
        if chart_type == "Bar Chart":
            ax.bar(x_data, y_data, color=color, width=0.6)
        elif chart_type == "Line Chart":
            ax.plot(x_data, y_data, color=color, marker='o', linewidth=2, markersize=5)
        elif chart_type == "Area Chart":
            ax.plot(x_data, y_data, color=color, marker='o', linewidth=2, markersize=4)
            ax.fill_between(x_data, y_data, color=color, alpha=0.15)
        elif chart_type == "Pie Chart":
            # Modern Donut chart with exterior callout lines
            palette = sns.color_palette(Theme.current.get("PLOT_PALETTE", "Blues"), len(x_data))
            
            # Using wedgeprops to create Donut structure
            wedges, texts = ax.pie(y_data, colors=palette, startangle=140,
                                   wedgeprops=dict(width=0.5, edgecolor=Theme.current["BG_SURFACE"]))
            
            # Configurations for the connecting lines
            kw = dict(arrowprops=dict(arrowstyle="-", color=Theme.current["TEXT_GRAY"], lw=1),
                      zorder=0, va="center")
            
            total_sum = sum(y_data)
            
            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1) / 2. + p.theta1
                y = np.sin(np.deg2rad(ang))
                x = np.cos(np.deg2rad(ang))
                
                # Fetch value, handle list or pandas series gracefully
                val = y_data.iloc[i] if hasattr(y_data, 'iloc') else y_data[i]
                percent = (val / total_sum) * 100
                
                # Suppress labels for tiny slices to avoid clutter
                if percent < 2.0: continue
                
                # Dynamic alignment and line connection
                horizontalalignment = {-1: "right", 1: "left"}[1 if x >= 0 else -1]
                connectionstyle = f"angle,angleA=0,angleB={ang}"
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                
                # Place text slightly further out to ensure visibility
                x_scale = 1.35 if x >= 0 else -1.35
                
                label_val = x_data.iloc[i] if hasattr(x_data, 'iloc') else x_data[i]
                label_str = str(label_val)
                if len(label_str) > 15: label_str = label_str[:13] + ".."
                
                ax.annotate(f"{label_str}\n{percent:.1f}%", xy=(x, y), xytext=(x_scale, 1.2 * y),
                            horizontalalignment=horizontalalignment, 
                            color=Theme.current["TEXT_WHITE"], fontsize=9, **kw)

    def refresh_dashboard(self):
        if self.df.empty: return

        stats = self.analyzer.get_basic_stats()
        
        pos = self.df['message'].str.contains('haha|good|great|love|awesome|happy|lol|xd|excellent', case=False).sum()
        neg = self.df['message'].str.contains('bad|sad|hate|angry|worst|sorry|cry|terrible', case=False).sum()
        if pos > neg: sentiment = "Positive"
        elif neg > pos: sentiment = "Negative"
        else: sentiment = "Neutral"

        self.card_msgs.update_value(f"{stats.get('total_msgs', 0):,}", subtitle=f"~{stats.get('avg_per_day', 0)} / day")
        self.card_words.update_value(f"{stats.get('total_words', 0):,}")
        self.card_media.update_value(f"{stats.get('media_count', 0):,}")
        self.card_links.update_value(f"{stats.get('links_count', 0):,}")
        self.card_sentiment.update_value(sentiment)
        
        # Row 2 Updates
        self.card_participants.update_value(f"{stats.get('users', 0)}")
        self.card_avg_words.update_value(f"{stats.get('avg_words_overall', 0)}")
        self.card_peak_hour.update_value(f"{stats.get('peak_hour', 'N/A')}")

        start, end = stats.get('start_date'), stats.get('end_date')
        if start and end:
            self.lbl_date_range.config(text=f"Temporal Range: {start.strftime('%Y-%m-%d')} → {end.strftime('%Y-%m-%d')} ({stats['days']} Days)")

        # Regenerate Plots
        self.plot_user_distribution()
        self.plot_msg_types()
        self.plot_timeline()
        self.plot_heatmap()
        self.plot_hourly_activity()
        self.plot_weekday_activity()
        self.plot_engagement_chart()
        self.plot_conflict_chart()
        self.plot_topics()
        self.plot_emotion_radar()
        self.plot_wordcloud()
        self.plot_sentiment_user_bar()
        self.plot_sentiment_timeline()
        
        # Regenerate Tables & Lists
        self.refresh_tables()
        self.refresh_trophies()

    def plot_user_distribution(self):
        self._clear_frame(self.frame_user_plot)
        top_users = self.analyzer.fetch_top_users()
        plt.style.use(Theme.current["PLOT_STYLE"])
        self.fig_user, ax = plt.subplots(figsize=(6, 4))
        self.fig_user.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_user.get()
        self._draw_chart(ax, chart_type, top_users.index.str[:12], top_users.values, Theme.current["ACCENT"])

        if chart_type != "Pie Chart":
            apply_modern_plot_style(ax, "", ylabel="Count")
            ax.tick_params(axis='x', rotation=0)
        else:
            # Adjust spacing so Pie Chart text callouts don't clip bounds
            self.fig_user.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)
        
        canvas = FigureCanvasTkAgg(self.fig_user, master=self.frame_user_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def plot_msg_types(self):
        self._clear_frame(self.frame_msg_type_plot)
        dist = self.analyzer.fetch_message_type_distribution()
        if not dist: return
        
        labels = list(dist.keys())
        values = list(dist.values())
        
        plt.style.use(Theme.current["PLOT_STYLE"])
        self.fig_msg_types, ax = plt.subplots(figsize=(6, 4))
        self.fig_msg_types.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_msg_types.get()
        self._draw_chart(ax, chart_type, labels, values, Theme.current["ACCENT"])

        if chart_type != "Pie Chart":
            apply_modern_plot_style(ax, "", ylabel="Count")
        else:
            self.fig_msg_types.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)
        
        canvas = FigureCanvasTkAgg(self.fig_msg_types, master=self.frame_msg_type_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_timeline(self):
        self._clear_frame(self.frame_timeline_plot)
        timeline = self.analyzer.fetch_monthly_timeline()
        if timeline.empty: return
        plt.style.use(Theme.current["PLOT_STYLE"])
        self.fig_time, ax = plt.subplots(figsize=(10, 4))
        self.fig_time.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_timeline.get()
        self._draw_chart(ax, chart_type, timeline['time'], timeline['message'], Theme.current["ACCENT"])

        if chart_type != "Pie Chart":
            apply_modern_plot_style(ax, "", ylabel="Volume")
            ax.tick_params(axis='x', rotation=45)
        else:
            self.fig_time.subplots_adjust(left=0.15, right=0.85)

        canvas = FigureCanvasTkAgg(self.fig_time, master=self.frame_timeline_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_heatmap(self):
        self._clear_frame(self.frame_heat_plot)
        activity = self.analyzer.fetch_activity_heatmap()
        if activity.empty: return
        plt.style.use(Theme.current["PLOT_STYLE"])
        
        # Widened to span full container cleanly
        self.fig_heat, ax = plt.subplots(figsize=(10, 4.5))
        self.fig_heat.patch.set_facecolor(Theme.current["BG_SURFACE"])

        palette = Theme.current.get("PLOT_PALETTE", "Blues")
        
        # Enhanced Minimalist Density Matrix
        sns.heatmap(activity, cmap=palette, ax=ax, 
                    linewidths=2, linecolor=Theme.current["BG_SURFACE"], 
                    square=True, cbar=True,
                    cbar_kws={"shrink": 0.75, "pad": 0.02, "drawedges": False})
        
        apply_modern_plot_style(ax, "", xlabel="Hour of Day (0-23)", ylabel="")
        
        ax.tick_params(labelsize=10)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        
        # Modernize Colorbar
        if len(ax.collections) > 0:
            cbar = ax.collections[0].colorbar
            cbar.ax.tick_params(colors=Theme.current["TEXT_GRAY"], labelsize=9, length=0)
            cbar.outline.set_visible(False)

        # Prevent large labels from being clipped
        self.fig_heat.subplots_adjust(bottom=0.20, top=0.95, left=0.15, right=0.95)

        canvas = FigureCanvasTkAgg(self.fig_heat, master=self.frame_heat_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_hourly_activity(self):
        self._clear_frame(self.frame_hour_plot)
        hourly = self.analyzer.fetch_hourly_activity()
        if hourly.empty: return
        plt.style.use(Theme.current["PLOT_STYLE"])
        
        # Expanded to full width
        self.fig_hour, ax = plt.subplots(figsize=(10, 3.5))
        self.fig_hour.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_hourly.get()
        self._draw_chart(ax, chart_type, hourly['hour'], hourly['count'], Theme.current["ACCENT"])

        if chart_type != "Pie Chart":
            apply_modern_plot_style(ax, "", xlabel="24h Clock", ylabel="Volume")
            self.fig_hour.subplots_adjust(bottom=0.25, left=0.10, right=0.95, top=0.85)
        else:
            self.fig_hour.subplots_adjust(left=0.2, right=0.8)

        canvas = FigureCanvasTkAgg(self.fig_hour, master=self.frame_hour_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_weekday_activity(self):
        self._clear_frame(self.frame_week_plot)
        weekday = self.analyzer.fetch_weekday_activity()
        if weekday.empty: return
        plt.style.use(Theme.current["PLOT_STYLE"])
        
        # Expanded to full width
        self.fig_week, ax = plt.subplots(figsize=(10, 3.5))
        self.fig_week.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_weekday.get()
        self._draw_chart(ax, chart_type, weekday['day_name'].str[:3], weekday['count'], Theme.current["ACCENT"])

        if chart_type != "Pie Chart":
            apply_modern_plot_style(ax, "", ylabel="Volume")
            self.fig_week.subplots_adjust(bottom=0.20, left=0.10, right=0.95, top=0.90)
        else:
            self.fig_week.subplots_adjust(left=0.2, right=0.8)

        canvas = FigureCanvasTkAgg(self.fig_week, master=self.frame_week_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def plot_engagement_chart(self):
        self._clear_frame(self.frame_eng_plot)
        eng_stats = self.analyzer.fetch_engagement_stats()
        if eng_stats.empty: return
        
        # Plot only users with a valid response time
        valid_resp = eng_stats[eng_stats['Avg Response Time (min)'] > 0].sort_values("Avg Response Time (min)")
        if valid_resp.empty: return
        
        plt.style.use(Theme.current["PLOT_STYLE"])
        # Expanded to full width
        self.fig_eng, ax = plt.subplots(figsize=(10, 4))
        self.fig_eng.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_eng.get()
        self._draw_chart(ax, chart_type, valid_resp['Sender'].str[:12], valid_resp['Avg Response Time (min)'], Theme.current["ACCENT"])

        if chart_type != "Pie Chart":
            apply_modern_plot_style(ax, "", ylabel="Average Delay (min)")
            ax.tick_params(axis='x', rotation=0)
            self.fig_eng.subplots_adjust(bottom=0.20, left=0.10, right=0.95, top=0.90)
        else:
            self.fig_eng.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)
        
        canvas = FigureCanvasTkAgg(self.fig_eng, master=self.frame_eng_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_conflict_chart(self):
        self._clear_frame(self.frame_conf_plot)
        conf_data = self.analyzer.fetch_conflict_data()
        timeline = conf_data.get("timeline", [])
        
        if not timeline:
            tk.Label(self.frame_conf_plot, text="No conflict data detected.", bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(expand=True)
            return

        dates = [x[0][-5:] for x in timeline] # Use MM-DD for cleaner x-axis
        counts = [x[1] for x in timeline]

        plt.style.use(Theme.current["PLOT_STYLE"])
        
        # Expanded to full width for the new layout
        self.fig_conf, ax = plt.subplots(figsize=(10, 3.5))
        self.fig_conf.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_conf.get()
        
        # We explicitly use the ERROR theme color for conflicts
        self._draw_chart(ax, chart_type, dates, counts, Theme.current["ERROR"])

        if chart_type != "Pie Chart":
            apply_modern_plot_style(ax, "", ylabel="Hostile Terms Count")
            
            # Prevent overcrowding of X axis labels if there are too many dates
            ax.xaxis.set_major_locator(MaxNLocator(nbins=12))
            ax.tick_params(axis='x', rotation=45)
            self.fig_conf.subplots_adjust(bottom=0.25, top=0.9, left=0.10, right=0.95)
        else:
            self.fig_conf.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.1)

        canvas = FigureCanvasTkAgg(self.fig_conf, master=self.frame_conf_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_topics(self):
        self._clear_frame(self.frame_topics_plot)
        topics = self.analyzer.fetch_topic_distribution()
        
        labels = [k for k, v in topics.items() if v > 0]
        values = [v for k, v in topics.items() if v > 0]
        
        if not values:
            tk.Label(self.frame_topics_plot, text="Insufficient topic data.", bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(expand=True)
            return

        plt.style.use(Theme.current["PLOT_STYLE"])
        self.fig_topics, ax = plt.subplots(figsize=(8, 5))
        self.fig_topics.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_topics.get()
        self._draw_chart(ax, chart_type, labels, values, Theme.current["ACCENT"])

        if chart_type != "Pie Chart":
            apply_modern_plot_style(ax, "")
            ax.tick_params(axis='x', rotation=0)
        else:
            self.fig_topics.subplots_adjust(left=0.2, right=0.8)

        canvas = FigureCanvasTkAgg(self.fig_topics, master=self.frame_topics_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_emotion_radar(self):
        self._clear_frame(self.frame_radar_plot)
        emotions = self.analyzer.fetch_emotion_radar()
        
        labels = list(emotions.keys())
        values = list(emotions.values())
        
        if sum(values) == 0:
            tk.Label(self.frame_radar_plot, text="Insufficient emotional lexicon data.", bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(expand=True)
            return

        plt.style.use(Theme.current["PLOT_STYLE"])
        chart_type = self.chart_type_radar.get()
        
        if chart_type in ["Bar Chart", "Pie Chart"]:
            self.fig_radar, ax = plt.subplots(figsize=(8, 5))
            self.fig_radar.patch.set_facecolor(Theme.current["BG_SURFACE"])
            ax.set_facecolor(Theme.current["BG_SURFACE"])
            self._draw_chart(ax, chart_type, labels, values, Theme.current["ACCENT"])
            if chart_type != "Pie Chart": 
                apply_modern_plot_style(ax, "")
            else:
                self.fig_radar.subplots_adjust(left=0.2, right=0.8)
        else: # Minimal Radar
            self.fig_radar, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            self.fig_radar.patch.set_facecolor(Theme.current["BG_SURFACE"])
            ax.set_facecolor(Theme.current["BG_SURFACE"])
            
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            val_wrap = values + values[:1]
            ang_wrap = angles + angles[:1]
            
            ax.fill(ang_wrap, val_wrap, color=Theme.current["ACCENT"], alpha=0.2)
            ax.plot(ang_wrap, val_wrap, color=Theme.current["ACCENT"], linewidth=1.5)
            ax.set_xticks(angles)
            ax.set_xticklabels([l.title() for l in labels], color=Theme.current["TEXT_WHITE"], size=9)
            ax.set_yticklabels([])
            ax.spines['polar'].set_color(Theme.current["BORDER"])
            ax.grid(color=Theme.current["BORDER"], alpha=0.5)

        canvas = FigureCanvasTkAgg(self.fig_radar, master=self.frame_radar_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_sentiment_user_bar(self):
        self._clear_frame(self.frame_user_sent_plot)
        sent_data = self.analyzer.fetch_sentiment_detailed_stats()
        user_data = sent_data.get("user_data", {})
        
        if not user_data:
            tk.Label(self.frame_user_sent_plot, text="Insufficient sentiment data.", bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(expand=True)
            return

        users = list(user_data.keys())
        pos_vals = [d["pos"] for d in user_data.values()]
        neg_vals = [d["neg"] for d in user_data.values()]

        plt.style.use(Theme.current["PLOT_STYLE"])
        self.fig_user_sent, ax = plt.subplots(figsize=(6, 4))
        self.fig_user_sent.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_user_sent.get()
        
        if chart_type in ["Bar Chart", "Area Chart"]:
            x = np.arange(len(users))
            width = 0.35
            ax.bar(x - width/2, pos_vals, width, label='Positive', color=Theme.current["SUCCESS"])
            ax.bar(x + width/2, neg_vals, width, label='Negative', color=Theme.current["ERROR"])
            ax.set_xticks(x)
            ax.set_xticklabels([u[:8] for u in users], rotation=0)
            ax.legend(frameon=False, loc="upper right")
            apply_modern_plot_style(ax, "", ylabel="Lexicon Hits")
        elif chart_type == "Line Chart":
            ax.plot(users, pos_vals, marker='o', label='Positive', color=Theme.current["SUCCESS"])
            ax.plot(users, neg_vals, marker='o', label='Negative', color=Theme.current["ERROR"])
            apply_modern_plot_style(ax, "", ylabel="Lexicon Hits")
            ax.legend(frameon=False)
        else: # Pie chart fallback
            net = [max(0, p - n) for p, n in zip(pos_vals, neg_vals)]
            self._draw_chart(ax, "Pie Chart", [u[:8] for u in users], net, Theme.current["ACCENT"])
            self.fig_user_sent.subplots_adjust(left=0.2, right=0.8)

        canvas = FigureCanvasTkAgg(self.fig_user_sent, master=self.frame_user_sent_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_sentiment_timeline(self):
        self._clear_frame(self.frame_sent_time_plot)
        sent_data = self.analyzer.fetch_sentiment_detailed_stats()
        timeline = sent_data.get("timeline", [])
        
        if not timeline:
            tk.Label(self.frame_sent_time_plot, text="Insufficient timeline data.", bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(expand=True)
            return

        dates = [x[0] for x in timeline]
        pos_vals = [x[1]["pos"] for x in timeline]
        neg_vals = [x[1]["neg"] for x in timeline]

        plt.style.use(Theme.current["PLOT_STYLE"])
        self.fig_sent_time, ax = plt.subplots(figsize=(10, 3.5))
        self.fig_sent_time.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.set_facecolor(Theme.current["BG_SURFACE"])

        chart_type = self.chart_type_sent_time.get()
        
        if chart_type == "Area Chart":
            ax.plot(dates, pos_vals, marker='o', color=Theme.current["SUCCESS"], label="Positive")
            ax.fill_between(dates, pos_vals, color=Theme.current["SUCCESS"], alpha=0.15)
            ax.plot(dates, neg_vals, marker='o', color=Theme.current["ERROR"], label="Negative")
            ax.fill_between(dates, neg_vals, color=Theme.current["ERROR"], alpha=0.15)
            ax.legend(frameon=False)
            apply_modern_plot_style(ax, "", ylabel="Lexicon Hits")
            ax.tick_params(axis='x', rotation=45)
            self.fig_sent_time.subplots_adjust(bottom=0.25)
        elif chart_type == "Line Chart":
            ax.plot(dates, pos_vals, marker='o', color=Theme.current["SUCCESS"], label="Positive")
            ax.plot(dates, neg_vals, marker='o', color=Theme.current["ERROR"], label="Negative")
            ax.legend(frameon=False)
            apply_modern_plot_style(ax, "", ylabel="Lexicon Hits")
            ax.tick_params(axis='x', rotation=45)
            self.fig_sent_time.subplots_adjust(bottom=0.25)
        elif chart_type == "Bar Chart":
            x = np.arange(len(dates))
            width = 0.35
            ax.bar(x - width/2, pos_vals, width, label='Positive', color=Theme.current["SUCCESS"])
            ax.bar(x + width/2, neg_vals, width, label='Negative', color=Theme.current["ERROR"])
            ax.set_xticks(x)
            ax.set_xticklabels(dates, rotation=45)
            ax.legend(frameon=False)
            apply_modern_plot_style(ax, "", ylabel="Lexicon Hits")
            self.fig_sent_time.subplots_adjust(bottom=0.25)
        else:
            self._draw_chart(ax, "Pie Chart", dates, [p+n for p, n in zip(pos_vals, neg_vals)], Theme.current["ACCENT"])
            self.fig_sent_time.subplots_adjust(left=0.2, right=0.8)

        canvas = FigureCanvasTkAgg(self.fig_sent_time, master=self.frame_sent_time_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def plot_wordcloud(self):
        self._clear_frame(self.frame_wc_plot)
        if not WORDCLOUD_AVAILABLE:
            tk.Label(self.frame_wc_plot, text="WordCloud dependency missing.", bg=Theme.current["BG_SURFACE"], fg=Theme.current["TEXT_GRAY"]).pack(expand=True)
            return

        freq = self.analyzer.fetch_word_frequency(top_n=100, include_stopwords=self.var_sw.get())
        if not freq: return
        
        wc_data = {w: c for w, c in freq}
        wc = WordCloud(background_color=Theme.current["BG_SURFACE"], width=800, height=400, colormap=Theme.current.get("PLOT_PALETTE", "Blues")).generate_from_frequencies(wc_data)

        plt.style.use(Theme.current["PLOT_STYLE"])
        self.fig_wc, ax = plt.subplots(figsize=(8, 4))
        self.fig_wc.patch.set_facecolor(Theme.current["BG_SURFACE"])
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")

        canvas = FigureCanvasTkAgg(self.fig_wc, master=self.frame_wc_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def refresh_tables(self):
        # Emojis
        for i in self.tree_emojis.get_children(): self.tree_emojis.delete(i)
        for char, meaning, count in self.analyzer.fetch_emoji_stats(20):
            self.tree_emojis.insert("", "end", values=(char, meaning, count))
            
        # Domains
        for i in self.tree_domains.get_children(): self.tree_domains.delete(i)
        for dom, count in self.analyzer.fetch_top_domains(20):
            self.tree_domains.insert("", "end", values=(dom, count))
            
        # Engagement
        for i in self.tree_eng.get_children(): self.tree_eng.delete(i)
        eng_stats = self.analyzer.fetch_engagement_stats()
        if not eng_stats.empty:
            valid_resp = eng_stats[eng_stats['Avg Response Time (min)'] > 0]
            if not valid_resp.empty:
                fastest = valid_resp.loc[valid_resp['Avg Response Time (min)'].idxmin()]
                self.card_fastest.update_value(fastest['Sender'], f"{fastest['Avg Response Time (min)']} mins")
            
            top_init = eng_stats.loc[eng_stats['Conversation Starters'].idxmax()]
            self.card_initiator.update_value(top_init['Sender'], f"{top_init['Conversation Starters']} starters")
            
            top_double = eng_stats.loc[eng_stats['Avg Msgs/Turn'].idxmax()]
            self.card_double_text.update_value(top_double['Sender'], f"{top_double['Avg Msgs/Turn']} msgs/turn")

            for _, row in eng_stats.iterrows():
                self.tree_eng.insert("", "end", values=(row['Sender'], row['Avg Response Time (min)'], row['Conversation Starters'], row['Avg Msgs/Turn'], row['Max Silence Broken (hrs)']))

        # Conflicts Update
        conf_data = self.analyzer.fetch_conflict_data()
        
        self.card_total_conflicts.update_value(conf_data["total"], "Terms detected")
        
        top_instigator = conf_data["senders"][0] if conf_data["senders"] else ("N/A", 0)
        self.card_instigator.update_value(top_instigator[0][:12], f"{top_instigator[1]} terms used")
        
        top_day = sorted(conf_data["timeline"], key=lambda x: x[1], reverse=True)[0] if conf_data["timeline"] else ("N/A", 0)
        self.card_tense_day.update_value(top_day[0], f"{top_day[1]} terms detected")

        for i in self.tree_instigators.get_children(): self.tree_instigators.delete(i)
        for sender, count in conf_data["senders"]:
            self.tree_instigators.insert("", "end", values=(sender, count))

        for i in self.tree_conf_words.get_children(): self.tree_conf_words.delete(i)
        for word, count in conf_data["words"]:
            self.tree_conf_words.insert("", "end", values=(word.title(), count))

        # Lexicon Extras Update
        lex_extras = self.analyzer.fetch_lexicon_extras()
        for i in self.tree_micro.get_children(): self.tree_micro.delete(i)
        for exp, count in lex_extras["polite"]:
            self.tree_micro.insert("", "end", values=(exp, "Politeness", count))
        for exp, count in lex_extras["laughs"]:
            self.tree_micro.insert("", "end", values=(exp, "Laughter", count))
            
        longest = self.analyzer.fetch_longest_messages()
        for i in self.tree_longest.get_children(): self.tree_longest.delete(i)
        for msg_row in longest:
            dt_str = msg_row[0].strftime("%Y-%m-%d %H:%M")
            preview = str(msg_row[3]).replace("\n", " ")[:150] + "..."
            self.tree_longest.insert("", "end", values=(dt_str, msg_row[1], msg_row[2], preview))

        # Sentiment Update
        sent_data = self.analyzer.fetch_sentiment_detailed_stats()
        if sent_data:
            self.card_pos_sentiment.update_value(f"{sent_data.get('total_pos', 0):,}", "Joy/Affection")
            self.card_neg_sentiment.update_value(f"{sent_data.get('total_neg', 0):,}", "Anger/Sad/Fear")
            self.card_top_pos.update_value(str(sent_data.get('most_pos_user', 'N/A'))[:12])
            self.card_top_neg.update_value(str(sent_data.get('most_neg_user', 'N/A'))[:12])

        self.refresh_message_log()

    def refresh_trophies(self):
        self._clear_frame(self.frame_trophies_content)
        trophies = self.analyzer.fetch_user_trophies()
        
        if not trophies:
            tk.Label(self.frame_trophies_content, text="Insufficient data to compute accolades.", bg=Theme.current["BG_MAIN"], fg=Theme.current["TEXT_GRAY"]).pack(pady=50)
            return
            
        COLUMNS = 3
        for idx, t in enumerate(trophies):
            row = idx // COLUMNS
            col = idx % COLUMNS
            
            # Configure columns to distribute equally
            self.frame_trophies_content.columnconfigure(col, weight=1)
            
            # Instantiate custom AccoladeCard widget
            card = AccoladeCard(self.frame_trophies_content, icon=t["icon"], title=t["title"], winner=t["winner"], desc=t["desc"])
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

    def refresh_message_log(self):
        for i in self.tree_msgs.get_children(): self.tree_msgs.delete(i)
        if self.df.empty: return

        last_msgs = self.df.tail(200).sort_values(by="datetime", ascending=False)
        for _, row in last_msgs.iterrows():
            t = row['datetime'].strftime("%Y-%m-%d %H:%M")
            msg_text = row['message']
            if self.wrap_messages.get():
                msg_text = wrap_text(msg_text, width=90)
            self.tree_msgs.insert("", "end", values=(t, row['sender'], msg_text))

    def open_search_dialog(self):
        if self.df_full.empty:
            messagebox.showinfo("Action Required", "Load a dataset prior to querying.")
            return
        SearchGUI(self)


# ==============================================================================
# ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    try:
        # Load persisted config from disk before rendering UI
        Theme.load_config()
        
        app = WhatsAppAnalyzerPro()
        app.mainloop()
    except Exception as e:
        print(f"System Failure: {e}")
        traceback.print_exc()
