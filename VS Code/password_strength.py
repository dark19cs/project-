"""
Password Strength Module
Evaluates password strength and provides improvement suggestions.
"""

import re
from config import COLOR_WEAK, COLOR_MEDIUM, COLOR_STRONG


class PasswordStrength:
    """
    Evaluates password strength based on multiple criteria.
    Provides detailed feedback and improvement suggestions.
    """
    
    def __init__(self):
        """Initialize the PasswordStrength evaluator."""
        # Strength thresholds
        self.weak_threshold = 2
        self.medium_threshold = 4
        self.strong_threshold = 5
    
    def check_strength(self, password):
        """
        Check the strength of a password.
        Evaluates based on: length, lowercase, uppercase, digits, symbols.
        
        Args:
            password (str): The password to evaluate
            
        Returns:
            dict: Contains strength score, level, percentage, color, and tips
        """
        score = 0
        tips = []
        
        # Rule 1: Minimum length (8 characters)
        if len(password) >= 8:
            score += 1
        else:
            tips.append("Minimum 8 characters")
        
        # Rule 2: Contains lowercase letters
        if re.search(r"[a-z]", password):
            score += 1
        else:
            tips.append("Add lowercase letters")
        
        # Rule 3: Contains uppercase letters
        if re.search(r"[A-Z]", password):
            score += 1
        else:
            tips.append("Add uppercase letters")
        
        # Rule 4: Contains digits
        if re.search(r"[0-9]", password):
            score += 1
        else:
            tips.append("Add numbers")
        
        # Rule 5: Contains special symbols
        if re.search(r"[@$!%*?&#]", password):
            score += 1
        else:
            tips.append("Add symbols")
        
        return {
            'score': score,
            'level': self.get_strength_level(score),
            'percentage': (score / 5) * 100,
            'color': self.get_strength_color(score),
            'tips': tips,
            'passed_rules': score,
            'total_rules': 5
        }
    
    def get_strength_level(self, score):
        """
        Get the strength level name based on score.
        
        Args:
            score (int): Strength score (0-5)
            
        Returns:
            str: Strength level ('weak', 'medium', 'strong')
        """
        if score <= self.weak_threshold:
            return 'weak'
        elif score <= self.medium_threshold:
            return 'medium'
        else:
            return 'strong'
    
    def get_strength_color(self, score):
        """
        Get the display color for strength level.
        
        Args:
            score (int): Strength score (0-5)
            
        Returns:
            str: Hex color code for the strength level
        """
        if score <= self.weak_threshold:
            return COLOR_WEAK
        elif score <= self.medium_threshold:
            return COLOR_MEDIUM
        else:
            return COLOR_STRONG
    
    def is_strong(self, password):
        """
        Check if a password is considered strong.
        
        Args:
            password (str): The password to check
            
        Returns:
            bool: True if password strength is 'strong'
        """
        result = self.check_strength(password)
        return result['level'] == 'strong'
    
    def is_weak(self, password):
        """
        Check if a password is considered weak.
        
        Args:
            password (str): The password to check
            
        Returns:
            bool: True if password strength is 'weak'
        """
        result = self.check_strength(password)
        return result['level'] == 'weak'
    
    def is_medium(self, password):
        """
        Check if a password is considered medium strength.
        
        Args:
            password (str): The password to check
            
        Returns:
            bool: True if password strength is 'medium'
        """
        result = self.check_strength(password)
        return result['level'] == 'medium'
    
    def get_detailed_analysis(self, password):
        """
        Get a detailed analysis of password characteristics.
        
        Args:
            password (str): The password to analyze
            
        Returns:
            dict: Detailed information about password composition
        """
        return {
            'length': len(password),
            'has_lowercase': bool(re.search(r"[a-z]", password)),
            'has_uppercase': bool(re.search(r"[A-Z]", password)),
            'has_digits': bool(re.search(r"[0-9]", password)),
            'has_symbols': bool(re.search(r"[@$!%*?&#]", password)),
            'has_spaces': bool(re.search(r"\s", password)),
            'unique_chars': len(set(password)),
            'lowercase_count': len(re.findall(r"[a-z]", password)),
            'uppercase_count': len(re.findall(r"[A-Z]", password)),
            'digit_count': len(re.findall(r"[0-9]", password)),
            'symbol_count': len(re.findall(r"[@$!%*?&#]", password))
        }
    
    def compare_passwords(self, pwd1, pwd2):
        """
        Compare two passwords by strength.
        
        Args:
            pwd1 (str): First password
            pwd2 (str): Second password
            
        Returns:
            dict: Comparison results
        """
        strength1 = self.check_strength(pwd1)
        strength2 = self.check_strength(pwd2)
        
        if strength1['score'] > strength2['score']:
            winner = 'password1'
        elif strength2['score'] > strength1['score']:
            winner = 'password2'
        else:
            winner = 'tie'
        
        return {
            'password1_strength': strength1['level'],
            'password1_score': strength1['score'],
            'password2_strength': strength2['level'],
            'password2_score': strength2['score'],
            'winner': winner
        }
