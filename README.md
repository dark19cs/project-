"""
SecurePass Pro - Password Generator Application
===============================================

A modern, secure password generator with advanced features including pattern detection,
password history management, and multi-language support.

PROJECT STRUCTURE
=================

The application follows Object-Oriented Programming (OOP) principles with separate,
well-organized modules for different functionality:

1. config.py
   - Centralized configuration for all application settings
   - Theme colors (Spartan palette)
   - Window dimensions and UI constants
   - Font definitions
   - Password generation settings

2. password_generator.py (PasswordGenerator class)
   - generate(): Basic 14-character password generation
   - generate_from_pattern(): Create passwords using pattern codes (L/U/N/S)
   - generate_with_requirements(): Generate with specific character type requirements
   - generate_memorable(): Create more readable passwords
   - validate_pattern(): Validate pattern syntax
   - set_length() / get_length(): Manage default password length

3. password_strength.py (PasswordStrength class)
   - check_strength(): Comprehensive strength evaluation (0-5 score)
   - get_strength_level(): Classify as weak/medium/strong
   - get_strength_color(): Get appropriate UI color for strength level
   - is_strong() / is_weak() / is_medium(): Quick checks
   - get_detailed_analysis(): Detailed password composition analysis
   - compare_passwords(): Compare two passwords by strength

4. pattern_detection.py (PatternDetector class)
   - detect_repetitions(): Find consecutive and repeated characters
   - detect_sequential_patterns(): Identify sequential characters (abc, 123, qwerty)
   - detect_dictionary_words(): Check for common weak passwords
   - get_pattern_report(): Complete analysis with risk score
   - get_risk_level(): Quick risk assessment

5. password_history.py (PasswordHistory class)
   - Persistent storage using JSON file (password_history.json)
   - add_password(): Add unique passwords to history
   - add_password_with_strength(): Store with strength metadata
   - get_all() / get_recent(): Retrieve history
   - get_all_with_metadata(): Get full entry information
   - clear_history() / remove_password(): History management
   - is_empty() / count(): Status checks

6. translations.py
   - Multi-language support
   - Translations for: English (EN), Farsi (FA), Kurdish Sorani (KU), Arabic (AR)
   - Simple dictionary-based translation system

7. pass_project.py (Main Application)
   - Tkinter-based GUI application
   - Integrates all OOP modules
   - Real-time password strength checking
   - Pattern detection analysis
   - Password history management
   - Multi-language UI switching


FEATURES
========

1. PASSWORD GENERATION
   - Standard generation (14-character with all character types)
   - Pattern-based generation (specify character types with L/U/N/S codes)
   - Memorable password generation
   - Customizable length and character requirements

2. STRENGTH CHECKING
   - Real-time evaluation as user types
   - 5-rule scoring system:
     * Minimum 8 characters
     * Lowercase letters
     * Uppercase letters
     * Numbers
     * Special symbols (@$!%*?&#)
   - Visual progress bar
   - Improvement suggestions

3. PATTERN DETECTION
   - Detects character repetitions
   - Identifies sequential patterns
   - Finds common dictionary words
   - Calculates overall risk score (0-100)
   - Color-coded risk levels: none/low/medium/high/critical

4. PASSWORD HISTORY
   - Persistent storage with timestamps
   - Stores up to 10 passwords (configurable)
   - Records password strength for each entry
   - JSON-based for easy data management
   - View recent passwords with metadata

5. MULTI-LANGUAGE SUPPORT
   - English (EN)
   - Farsi/Persian (FA)
   - Kurdish Sorani (KU)
   - Arabic (AR)
   - Real-time UI language switching

6. USER INTERFACE
   - Spartan minimalist design
   - Dark theme with gold accents
   - Show/hide password toggle
   - Copy to clipboard functionality
   - Pattern-based generation interface
   - History viewer
   - Responsive and intuitive


PATTERN CODES FOR PASSWORD GENERATION
======================================

When using pattern-based generation:
  L = Lowercase letter (a-z)
  U = Uppercase letter (A-Z)
  N = Number (0-9)
  S = Special symbol (@$!%*?&#)

Examples:
  "LUNS" → Generates: 1 lowercase, 1 uppercase, 1 number, 1 symbol
  "LLUU" → Generates: 2 lowercase, 2 uppercase
  "LLLNNS" → Generates: 3 lowercase, 2 numbers, 1 symbol


RISK LEVELS (from Pattern Detection)
====================================

NONE (0%)
  - No patterns or weak patterns detected
  - Password is pattern-safe

LOW (1-30%)
  - Minor pattern issues
  - Password is generally safe

MEDIUM (31-50%)
  - Some pattern weaknesses
  - Consider revising password

HIGH (51-70%)
  - Multiple pattern issues
  - Weak password detected

CRITICAL (71-100%)
  - Severe patterns or dictionary words
  - Very weak password - avoid using


OOP ARCHITECTURE BENEFITS
=========================

1. SEPARATION OF CONCERNS
   - Each module handles one responsibility
   - Password generation, strength checking, and pattern detection are isolated
   - Easy to test individual components

2. REUSABILITY
   - Classes can be used in other projects
   - Import and use the modules independently

3. MAINTAINABILITY
   - Clear organization makes code easier to update
   - Comments explain each method's purpose
   - Configuration centralized in config.py

4. EXTENSIBILITY
   - Easy to add new password generation methods
   - Can implement additional pattern detections
   - Simple to add more languages

5. SCALABILITY
   - Structure supports future enhancements
   - Cloud storage integration possible
   - API wrapper can be created easily


INSTALLATION & USAGE
====================

Requirements:
  - Python 3.6+
  - tkinter (usually included with Python)

Run the application:
  python3 pass_project.py

Features available:
  1. Generate random passwords
  2. Generate from patterns
  3. Check password strength (real-time)
  4. View pattern analysis
  5. Browse password history
  6. Switch language (EN/FA/KU/AR)
  7. Copy passwords to clipboard
  8. Clear/reset interface


DATA STORAGE
============

Password history is stored in: password_history.json

Format:
[
  {
    "password": "Abc123@$!",
    "timestamp": "2026-01-08T12:34:56.789012",
    "strength": "strong"
  },
  ...
]

The file is automatically created and updated when strong passwords are generated.


CONFIGURATION
=============

Edit config.py to customize:
  - Window size and appearance
  - Theme colors
  - Font sizes
  - Password length defaults
  - History limit
  - Progress bar styling


API EXAMPLES
============

Using PasswordGenerator:
    from password_generator import PasswordGenerator
    gen = PasswordGenerator()
    pwd = gen.generate()  # 14-character password
    pwd = gen.generate_from_pattern("LUNS")  # Custom pattern

Using PasswordStrength:
    from password_strength import PasswordStrength
    checker = PasswordStrength()
    result = checker.check_strength("Abc123@$!")
    print(result['level'])  # 'strong', 'medium', or 'weak'

Using PatternDetector:
    from pattern_detection import PatternDetector
    detector = PatternDetector()
    report = detector.get_pattern_report("password123")
    print(report['overall_risk']['level'])  # Risk level

Using PasswordHistory:
    from password_history import PasswordHistory
    history = PasswordHistory()
    history.add_password_with_strength("Abc123@$!", "strong")
    recent = history.get_recent(5)  # Last 5 passwords


LICENSE
=======

SecurePass Pro - Open Source Project
Educational and personal use


VERSION
=======

Version: 2.0 (OOP Refactor)
Release Date: January 2026
"""
