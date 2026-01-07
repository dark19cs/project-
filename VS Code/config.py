"""
Configuration Module
Centralized configuration for theme colors, constants, and application settings.
"""

# ===================== SPARTAN THEME COLORS =====================
# Define a compact "Spartan" palette used across the minimal UI.
# Adjust these values to change the app look & feel in one place.
SPARTAN_BG = "#0b1220"          # Main window background (very dark navy)
SPARTAN_FRAME = "#0f1724"       # Inner frame background (slightly lighter)
SPARTAN_ACCENT = "#D4AF37"      # Accent / header color (gold)
SPARTAN_TEXT = "#EBE5E5"        # Muted secondary text color (light gray)
SPARTAN_BTN_BG = "#0a0a0a"      # Button background neutral

# ===================== WINDOW SETTINGS =====================
WINDOW_WIDTH = 720
WINDOW_HEIGHT = 680
WINDOW_RESIZABLE = False

# ===================== PASSWORD GENERATION SETTINGS =====================
DEFAULT_PASSWORD_LENGTH = 14
PASSWORD_CHARSET = "@$!%*?&#"
PASSWORD_HISTORY_LIMIT = 10

# ===================== UI FONT SETTINGS =====================
FONT_TITLE = ("Helvetica Neue", 28, "bold")
FONT_LABEL = ("Helvetica Neue", 20, "bold")
FONT_BUTTON = ("Helvetica Neue", 14, "bold")
FONT_ENTRY = ("Helvetica Neue", 18)
FONT_SMALL = ("Helvetica Neue", 14)
FONT_FOOTER = ("Helvetica Neue", 12)

# ===================== COLOR CODES FOR STRENGTH =====================
COLOR_WEAK = "#dc2626"          # Red
COLOR_MEDIUM = "#f59e0b"        # Orange/Amber
COLOR_STRONG = "#16a34a"        # Green

# ===================== PROGRESS BAR SETTINGS =====================
PROGRESS_COLOR_TROUGH = "#111827"
PROGRESS_COLOR_FILLED = "#16a34a"
PROGRESS_THICKNESS = 18
