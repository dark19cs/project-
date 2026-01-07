#!/usr/bin/env python3
"""
SecurePass Pro - Password Generator Application
A secure password generator with strength checking, pattern detection, and multi-language support.

Features:
- Password generation with multiple methods
- Real-time strength checking with pattern detection
- Password history with persistent storage
- Multi-language support (English, Farsi, Kurdish Sorani, Arabic)
- Repetition and sequential pattern detection
- Dictionary word detection

Supports: EN (English), FA (Farsi), KU (Kurdish Sorani), AR (Arabic)
"""

# ===================== IMPORTS =====================
import tkinter as tk
from tkinter import ttk, messagebox
from translations import get as tr_get
from config import *
from password_generator import PasswordGenerator
from password_strength import PasswordStrength
from password_history import PasswordHistory
from pattern_detection import PatternDetector


# ===================== GLOBAL VARIABLES =====================
# Global variable to store the current language setting
current_lang = "en"

# Initialize OOP instances for password management
generator = PasswordGenerator()
strength_checker = PasswordStrength()
history_manager = PasswordHistory()
pattern_detector = PatternDetector()


# ===================== TRANSLATION HELPER =====================
def tr(key):
    """
    Helper function to get translated text based on current language.
    
    Args:
        key (str): The translation key
        
    Returns:
        str: The translated text or the key if translation not found
    """
    return tr_get(current_lang, key)

# ===================== PASSWORD MANAGEMENT FUNCTIONS =====================
def generate_password():
    """
    Generate a random secure password using the PasswordGenerator.
    Updates the password entry field and checks strength.
    Includes pattern detection analysis.
    """
    # Generate password using OOP generator
    pwd = generator.generate()
    
    # Replace entry text with the generated password
    entry.delete(0, tk.END)
    entry.insert(0, pwd)
    
    # Immediately show the generated password
    entry.config(show="")
    toggle_btn.config(text=tr("hide"))
    
    # Evaluate and visualize strength after generation
    check_strength()
    
    # Analyze patterns in the generated password
    analyze_patterns()
    
    # Add strong password to history (only on generation, not on typing)
    strength_result = strength_checker.check_strength(pwd)
    if strength_result['level'] == 'strong':
        history_manager.add_password_with_strength(pwd, strength_result['level'])


def copy_password():
    """
    Copy the current password to the system clipboard.
    Shows a confirmation message or warning if password field is empty.
    """
    pwd = entry.get()
    
    if pwd:
        root.clipboard_clear()
        root.clipboard_append(pwd)
        root.update()
        messagebox.showinfo(tr("copied_title"), tr("copied_msg"))
    else:
        messagebox.showwarning(tr("empty_title"), tr("empty_msg"))


def clear_all():
    """
    Clear all fields and reset the password generator.
    Clears the password entry, progress bar, and tips/results labels.
    """
    entry.delete(0, tk.END)
    entry.config(show="*")
    toggle_btn.config(text=tr("show"))
    progress["value"] = 0
    result_lbl.config(text="")
    tips_lbl.config(text="")
    pattern_lbl.config(text="")


def toggle_password():
    """
    Toggle between showing and hiding the password in the entry field.
    Updates the button text based on current visibility state.
    """
    if entry.cget("show") == "*":
        entry.config(show="")
        toggle_btn.config(text=tr("hide"))
    else:
        entry.config(show="*")
        toggle_btn.config(text=tr("show"))


def show_history():
    """
    Display the password history from persistent storage.
    Shows the recent passwords with timestamps in a custom dialog with black text.
    """
    if history_manager.is_empty():
        messagebox.showinfo(tr("history_title"), tr("no_history"))
        return
    
    # Get recent passwords
    recent = history_manager.get_recent_with_metadata(5)
    
    # Create custom history dialog window
    history_window = tk.Toplevel(root)
    history_window.title(tr("history_title"))
    history_window.geometry("400x250")
    history_window.resizable(False, False)
    history_window.configure(bg=SPARTAN_BG)
    
    # Create frame for content
    hist_frame = tk.Frame(history_window, bg=SPARTAN_FRAME)
    hist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create text widget with black text
    text_widget = tk.Text(
        hist_frame,
        height=12,
        width=45,
        bg="white",
        fg="black",
        font=("Helvetica Neue", 11),
        relief="flat",
        wrap=tk.WORD
    )
    text_widget.pack(fill=tk.BOTH, expand=True, pady=5)
    
    # Insert history into text widget
    for entry_data in recent:
        pwd = entry_data['password']
        strength = entry_data['strength']
        text_widget.insert(tk.END, f"• {pwd} ({strength})\n")
    
    # Make text read-only
    text_widget.config(state=tk.DISABLED)
    
    # Close button
    close_btn = tk.Button(
        hist_frame,
        text=tr("clear"),
        command=history_window.destroy,
        bg=SPARTAN_BTN_BG,
        fg="black",
        relief="flat",
        font=("Helvetica Neue", 10, "bold"),
        width=15
    )
    close_btn.pack(pady=5)


def check_strength(event=None):
    """
    Check and display the strength of the password.
    Uses PasswordStrength class for evaluation.
    Updates progress bar and displays improvement tips.
    
    Args:
        event (tk.Event, optional): Event object (used for key binding).
    """
    pwd = entry.get()
    
    # Use OOP strength checker
    strength_result = strength_checker.check_strength(pwd)
    
    # Update progress bar with percentage
    progress["value"] = strength_result['percentage']
    
    # Show improvement tips
    if strength_result['tips']:
        tips_lbl.config(text=" • ".join(strength_result['tips']))
    else:
        tips_lbl.config(text="Strong password!")
    
    # Update strength level label with appropriate color
    result_lbl.config(
        text=strength_result['level'].capitalize() + " Password",
        fg=strength_result['color']
    )


def analyze_patterns():
    """
    Analyze the password for patterns, repetitions, and dictionary words.
    Displays pattern detection results to the user.
    """
    pwd = entry.get()
    
    if not pwd:
        pattern_lbl.config(text="")
        return
    
    # Get pattern analysis
    pattern_report = pattern_detector.get_pattern_report(pwd)
    risk = pattern_report['overall_risk']
    
    # Format pattern message
    pattern_msg = f"Pattern Risk: {risk['level'].upper()} ({risk['score']}%)"
    
    # Add details if issues found
    if pattern_report['repetitions']['has_repetitions']:
        pattern_msg += f" | Repetitions: {pattern_report['repetitions']['count']}"
    
    if pattern_report['sequential']['has_sequential']:
        pattern_msg += f" | Sequential: {pattern_report['sequential']['count']}"
    
    if pattern_report['dictionary']['has_dictionary_words']:
        pattern_msg += f" | Dictionary words: {pattern_report['dictionary']['count']}"
    
    # Set color based on risk level
    if risk['level'] == 'critical':
        color = "#dc2626"  # Red
    elif risk['level'] == 'high':
        color = "#f59e0b"  # Orange
    elif risk['level'] == 'medium':
        color = "#eab308"  # Yellow
    else:
        color = "#16a34a"  # Green
    
    pattern_lbl.config(text=pattern_msg, fg=color)


def generate_from_pattern():
    """
    Generate a password from user-specified pattern.
    Pattern codes: L=lowercase, U=uppercase, N=number, S=symbol
    """
    pattern = pattern_entry.get()
    
    # Validate pattern
    if not generator.validate_pattern(pattern):
        messagebox.showerror(tr("pattern_invalid"), 
                            "Use only L, U, N, S characters in pattern")
        return
    
    # Generate password from pattern
    pwd = generator.generate_from_pattern(pattern)
    
    # Update entry field
    entry.delete(0, tk.END)
    entry.insert(0, pwd)
    entry.config(show="")
    toggle_btn.config(text=tr("hide"))
    
    # Check strength and patterns
    check_strength()
    analyze_patterns()



# ===================== WINDOW SETUP =====================
root = tk.Tk()
root.title(tr("title"))
root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(WINDOW_RESIZABLE, WINDOW_RESIZABLE)
root.configure(bg=SPARTAN_BG)


# ===================== STYLE CONFIGURATION =====================
style = ttk.Style()
style.theme_use("default")

style.configure(
    "Mac.Horizontal.TProgressbar",
    troughcolor=PROGRESS_COLOR_TROUGH,
    background=PROGRESS_COLOR_FILLED,
    thickness=PROGRESS_THICKNESS
)


# ===================== LANGUAGE SELECTION FRAME =====================
lang_frame = tk.Frame(root, bg=SPARTAN_BG)
lang_frame.place(relx=0.98, rely=0.02, anchor="ne")


def set_language(lang):
    """
    Change the application language and update all UI text.
    
    Args:
        lang (str): Language code ("en", "fa", "ku", "ar")
    """
    global current_lang
    current_lang = lang
    update_ui_texts()


lang_label = tk.Label(
    lang_frame,
    text="Language:",
    font=("Helvetica Neue", 10),
    fg=SPARTAN_TEXT,
    bg=SPARTAN_BG
)
lang_label.pack(side="left", padx=5)

en_btn = tk.Button(
    lang_frame,
    text="EN",
    command=lambda: set_language("en"),
    bg="#111827",
    fg="#38bdf8",
    activebackground="#1f2937",
    activeforeground="#38bdf8",
    relief="flat",
    font=("Helvetica Neue", 10, "bold"),
    width=3
)
en_btn.pack(side="right", padx=2)

fa_btn = tk.Button(
    lang_frame,
    text="FA",
    command=lambda: set_language("fa"),
    bg="#111827",
    fg="#38bdf8",
    activebackground="#1f2937",
    activeforeground="#38bdf8",
    relief="flat",
    font=("Helvetica Neue", 10, "bold"),
    width=3
)
fa_btn.pack(side="right", padx=2)

ku_btn = tk.Button(
    lang_frame,
    text="KU",
    command=lambda: set_language("ku"),
    bg="#111827",
    fg="#38bdf8",
    activebackground="#1f2937",
    activeforeground="#38bdf8",
    relief="flat",
    font=("Helvetica Neue", 10, "bold"),
    width=3
)
ku_btn.pack(side="right", padx=2)

ar_btn = tk.Button(
    lang_frame,
    text="AR",
    command=lambda: set_language("ar"),
    bg="#111827",
    fg="#38bdf8",
    activebackground="#1f2937",
    activeforeground="#38bdf8",
    relief="flat",
    font=("Helvetica Neue", 10, "bold"),
    width=3
)
ar_btn.pack(side="right", padx=2)


# ===================== MAIN CONTENT FRAME =====================
frame = tk.Frame(root, bg=SPARTAN_FRAME)
frame.place(relx=0.5, rely=0.5, anchor="center", width=620, height=600)


# ===================== TITLE LABEL =====================
title_lbl = tk.Label(
    frame,
    text=tr("title"),
    font=FONT_TITLE,
    fg=SPARTAN_ACCENT,
    bg=SPARTAN_FRAME
)
title_lbl.pack(pady=20)


# ===================== PASSWORD ENTRY FIELD =====================
entry = tk.Entry(
    frame,
    show="*",
    font=FONT_ENTRY,
    width=30,
    bg="white",
    fg="black",
    insertbackground="black",
    relief="flat"
)
entry.pack(pady=12)
entry.bind("<KeyRelease>", check_strength)


# ===================== TOGGLE PASSWORD BUTTON =====================
toggle_btn = tk.Button(
    frame,
    text=tr("show"),
    command=toggle_password,
    bg=SPARTAN_BTN_BG,
    fg="black",
    activebackground="#d1d5db",
    activeforeground="black",
    font=FONT_BUTTON,
    relief="flat",
    width=18,
    height=1
)
toggle_btn.pack(pady=8)


# ===================== ACTION BUTTONS FRAME =====================
btn_frame = tk.Frame(frame, bg=SPARTAN_FRAME)
btn_frame.pack(pady=15)

generate_btn = tk.Button(
    btn_frame,
    text=tr("generate"),
    command=generate_password,
    bg=SPARTAN_BTN_BG,
    fg="black",
    activebackground="#d1d5db",
    font=FONT_BUTTON,
    relief="flat",
    width=15,
    height=1
)
generate_btn.grid(row=0, column=0, padx=5)

copy_btn = tk.Button(
    btn_frame,
    text=tr("copy"),
    command=copy_password,
    bg=SPARTAN_BTN_BG,
    fg="black",
    activebackground="#d1d5db",
    font=FONT_BUTTON,
    relief="flat",
    width=15,
    height=1
)
copy_btn.grid(row=0, column=1, padx=5)

clear_btn = tk.Button(
    btn_frame,
    text=tr("clear"),
    command=clear_all,
    bg=SPARTAN_BTN_BG,
    fg="black",
    activebackground="#d1d5db",
    font=FONT_BUTTON,
    relief="flat",
    width=15,
    height=1
)
clear_btn.grid(row=0, column=2, padx=5)


# ===================== PATTERN ENTRY FRAME =====================
pattern_frame = tk.Frame(frame, bg=SPARTAN_FRAME)
pattern_frame.pack(pady=10)

pattern_label = tk.Label(
    pattern_frame,
    text="Pattern (L/U/N/S):",
    font=FONT_SMALL,
    fg=SPARTAN_TEXT,
    bg=SPARTAN_FRAME
)
pattern_label.pack(side="left", padx=5)

pattern_entry = tk.Entry(
    pattern_frame,
    font=FONT_SMALL,
    width=12,
    bg="white",
    fg="black"
)
pattern_entry.pack(side="left", padx=5)

pattern_gen_btn = tk.Button(
    pattern_frame,
    text="Generate",
    command=generate_from_pattern,
    bg="#3b82f6",
    fg="white",
    activebackground="#1d4ed8",
    font=("Helvetica Neue", 10, "bold"),
    relief="flat",
    width=12
)
pattern_gen_btn.pack(side="left", padx=5)


# ===================== CHECK STRENGTH BUTTON =====================
check_btn = tk.Button(
    frame,
    text=tr("check_strength"),
    command=check_strength,
    bg="#22c55e",
    fg="black",
    activebackground="#16a34a",
    font=FONT_BUTTON,
    relief="flat",
    width=20,
    height=1
)
check_btn.pack(pady=12)


# ===================== PROGRESS BAR =====================
progress = ttk.Progressbar(
    frame,
    style="Mac.Horizontal.TProgressbar",
    length=420
)
progress.pack(pady=10)


# ===================== RESULT LABEL =====================
result_lbl = tk.Label(
    frame,
    text="",
    font=FONT_LABEL,
    bg=SPARTAN_FRAME
)
result_lbl.pack(pady=8)


# ===================== TIPS LABEL =====================
tips_lbl = tk.Label(
    frame,
    text="",
    wraplength=520,
    bg=SPARTAN_FRAME,
    fg=SPARTAN_TEXT,
    font=FONT_SMALL
)
tips_lbl.pack(pady=5)


# ===================== PATTERN ANALYSIS LABEL =====================
pattern_lbl = tk.Label(
    frame,
    text="",
    wraplength=520,
    bg=SPARTAN_FRAME,
    fg=SPARTAN_TEXT,
    font=FONT_SMALL
)
pattern_lbl.pack(pady=5)


# ===================== HISTORY BUTTON =====================
history_btn = tk.Button(
    frame,
    text=tr("history_title"),
    command=show_history,
    bg="#8b5cf6",
    fg="white",
    activebackground="#6d28d9",
    font=FONT_BUTTON,
    relief="flat",
    width=20,
    height=1
)
history_btn.pack(pady=10)


# ===================== FOOTER LABEL =====================
footer_lbl = tk.Label(
    root,
    text=tr("footer"),
    fg=SPARTAN_ACCENT,
    bg=SPARTAN_BG,
    font=FONT_FOOTER
)
footer_lbl.place(relx=0.5, rely=0.97, anchor="center")


# ===================== UI UPDATE FUNCTION =====================
def update_ui_texts():
    """
    Update all UI text elements when language changes.
    Called whenever the user selects a different language.
    """
    root.title(tr("title"))
    title_lbl.config(text=tr("title"))
    
    generate_btn.config(text=tr("generate"))
    copy_btn.config(text=tr("copy"))
    clear_btn.config(text=tr("clear"))
    check_btn.config(text=tr("check_strength"))
    history_btn.config(text=tr("history_title"))
    
    if entry.cget("show") == "*":
        toggle_btn.config(text=tr("show"))
    else:
        toggle_btn.config(text=tr("hide"))
    
    footer_lbl.config(text=tr("footer"))
    
    # Refresh password strength display with new language
    check_strength()


# ===================== INITIALIZATION =====================
update_ui_texts()


# ===================== MAIN APPLICATION LOOP =====================
root.mainloop()
