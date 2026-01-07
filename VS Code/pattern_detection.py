"""
Pattern Detection Module
Detects patterns and repetitions in passwords for analysis.
"""

import re


class PatternDetector:
    """
    Analyzes passwords for common patterns and repetitions.
    Provides detailed feedback on security weaknesses related to patterns.
    """
    
    def __init__(self):
        """Initialize the PatternDetector."""
        pass
    
    def detect_repetitions(self, password):
        """
        Detect character repetitions in the password.
        
        Args:
            password (str): The password to analyze
            
        Returns:
            dict: Contains 'has_repetitions' (bool) and 'details' (list of found patterns)
        """
        details = []
        
        # Check for consecutive identical characters (e.g., 'aaa', '111')
        consecutive_pattern = r'(.)\1{2,}'
        matches = re.finditer(consecutive_pattern, password)
        for match in matches:
            details.append({
                'type': 'consecutive',
                'pattern': match.group(),
                'position': match.start(),
                'severity': 'high'
            })
        
        # Check for repeated sequences (e.g., 'abab', '123123')
        two_char_repeat = r'(.{2,})\1'
        matches = re.finditer(two_char_repeat, password)
        for match in matches:
            details.append({
                'type': 'sequence_repeat',
                'pattern': match.group(),
                'position': match.start(),
                'severity': 'medium'
            })
        
        return {
            'has_repetitions': len(details) > 0,
            'details': details,
            'count': len(details)
        }
    
    def detect_sequential_patterns(self, password):
        """
        Detect sequential character patterns (e.g., 'abc', '123', 'qwerty').
        
        Args:
            password (str): The password to analyze
            
        Returns:
            dict: Contains 'has_sequential' (bool) and 'patterns' (list)
        """
        details = []
        
        # Lowercase sequential (abc, bcd, etc.)
        lower_seq = r'[a-z]{3,}'
        for match in re.finditer(lower_seq, password):
            substr = match.group()
            if self._is_sequential(substr):
                details.append({
                    'type': 'lowercase_sequential',
                    'pattern': substr,
                    'position': match.start(),
                    'severity': 'medium'
                })
        
        # Uppercase sequential (ABC, BCD, etc.)
        upper_seq = r'[A-Z]{3,}'
        for match in re.finditer(upper_seq, password):
            substr = match.group()
            if self._is_sequential(substr):
                details.append({
                    'type': 'uppercase_sequential',
                    'pattern': substr,
                    'position': match.start(),
                    'severity': 'medium'
                })
        
        # Digit sequential (123, 234, etc.)
        digit_seq = r'\d{3,}'
        for match in re.finditer(digit_seq, password):
            substr = match.group()
            if self._is_sequential(substr):
                details.append({
                    'type': 'digit_sequential',
                    'pattern': substr,
                    'position': match.start(),
                    'severity': 'medium'
                })
        
        # Common keyboard patterns
        keyboard_patterns = [
            'qwerty', 'asdfgh', 'zxcvbn', 'qazwsx', '123456', '654321'
        ]
        lower_pass = password.lower()
        for kp in keyboard_patterns:
            if kp in lower_pass:
                details.append({
                    'type': 'keyboard_pattern',
                    'pattern': kp,
                    'position': lower_pass.index(kp),
                    'severity': 'high'
                })
        
        return {
            'has_sequential': len(details) > 0,
            'patterns': details,
            'count': len(details)
        }
    
    def _is_sequential(self, text):
        """
        Check if text contains sequential characters.
        Helper method for detect_sequential_patterns.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if characters are sequential
        """
        if len(text) < 3:
            return False
        
        for i in range(len(text) - 1):
            if ord(text[i+1]) - ord(text[i]) != 1:
                return False
        return True
    
    def detect_dictionary_words(self, password):
        """
        Detect common dictionary words in the password.
        Uses a simple approach with common weak passwords.
        
        Args:
            password (str): The password to analyze
            
        Returns:
            dict: Contains 'has_dictionary_words' (bool) and 'words' (list)
        """
        # Common weak password patterns
        common_words = [
            'password', 'admin', 'user', 'login', 'guest', 'welcome',
            'monkey', 'dragon', 'master', 'shadow', 'qwerty', 'letmein',
            'trustno1', 'starwars', 'baseball', 'princess', 'football'
        ]
        
        details = []
        lower_pass = password.lower()
        
        for word in common_words:
            if word in lower_pass:
                details.append({
                    'type': 'dictionary_word',
                    'word': word,
                    'position': lower_pass.index(word),
                    'severity': 'high'
                })
        
        return {
            'has_dictionary_words': len(details) > 0,
            'words': details,
            'count': len(details)
        }
    
    def get_pattern_report(self, password):
        """
        Generate a comprehensive pattern analysis report.
        
        Args:
            password (str): The password to analyze
            
        Returns:
            dict: Comprehensive report with all pattern analyses
        """
        return {
            'repetitions': self.detect_repetitions(password),
            'sequential': self.detect_sequential_patterns(password),
            'dictionary': self.detect_dictionary_words(password),
            'overall_risk': self._calculate_risk_score(password)
        }
    
    def _calculate_risk_score(self, password):
        """
        Calculate overall pattern risk score (0-100).
        
        Args:
            password (str): The password to analyze
            
        Returns:
            dict: Contains risk_score and risk_level
        """
        risk_score = 0
        
        # Check repetitions
        reps = self.detect_repetitions(password)
        for detail in reps['details']:
            if detail['severity'] == 'high':
                risk_score += 25
            else:
                risk_score += 15
        
        # Check sequential patterns
        seq = self.detect_sequential_patterns(password)
        for detail in seq['patterns']:
            if detail['severity'] == 'high':
                risk_score += 20
            else:
                risk_score += 12
        
        # Check dictionary words
        dict_check = self.detect_dictionary_words(password)
        risk_score += len(dict_check['words']) * 30
        
        # Cap the score at 100
        risk_score = min(100, risk_score)
        
        # Determine risk level
        if risk_score >= 70:
            risk_level = 'critical'
        elif risk_score >= 50:
            risk_level = 'high'
        elif risk_score >= 30:
            risk_level = 'medium'
        elif risk_score > 0:
            risk_level = 'low'
        else:
            risk_level = 'none'
        
        return {
            'score': risk_score,
            'level': risk_level
        }
    
    def get_risk_level(self, password):
        """
        Get the risk level of a password based on patterns.
        
        Args:
            password (str): The password to analyze
            
        Returns:
            str: Risk level ('none', 'low', 'medium', 'high', 'critical')
        """
        return self._calculate_risk_score(password)['level']
