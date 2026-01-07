"""
Password Generator Module
Handles password generation with various options and patterns.
"""

import random
import string
from config import DEFAULT_PASSWORD_LENGTH, PASSWORD_CHARSET


class PasswordGenerator:
    """
    Generates secure passwords with multiple generation methods.
    Supports standard generation, pattern-based generation, and custom character sets.
    """
    
    def __init__(self, length=DEFAULT_PASSWORD_LENGTH):
        """
        Initialize the PasswordGenerator.
        
        Args:
            length (int): Default password length. Defaults to DEFAULT_PASSWORD_LENGTH (14)
        """
        self.length = length
        self.charset_letters = string.ascii_letters
        self.charset_digits = string.digits
        self.charset_symbols = PASSWORD_CHARSET
        self.full_charset = self.charset_letters + self.charset_digits + self.charset_symbols
    
    def generate(self, length=None):
        """
        Generate a random secure password.
        Includes uppercase, lowercase, digits, and special characters.
        
        Args:
            length (int): Password length. If None, uses the instance length. Defaults to None
            
        Returns:
            str: The generated password
        """
        pwd_length = length if length is not None else self.length
        
        # Generate random password from full character set
        password = ''.join(random.choice(self.full_charset) for _ in range(pwd_length))
        
        return password
    
    def generate_from_pattern(self, pattern):
        """
        Generate a password from a pattern specification.
        Pattern codes: L=lowercase, U=uppercase, N=number, S=symbol
        Example: "LUNS" generates: lowercase, uppercase, number, symbol
        
        Args:
            pattern (str): Pattern string (e.g., 'LLNNSSS')
            
        Returns:
            str: Generated password, or empty string if pattern is invalid
        """
        if not pattern:
            return ""
        
        password = []
        valid_codes = {'L', 'U', 'N', 'S'}
        
        for code in pattern.upper():
            if code == 'L':
                password.append(random.choice(string.ascii_lowercase))
            elif code == 'U':
                password.append(random.choice(string.ascii_uppercase))
            elif code == 'N':
                password.append(random.choice(string.digits))
            elif code == 'S':
                password.append(random.choice(self.charset_symbols))
            else:
                # Invalid code in pattern
                return ""
        
        # Shuffle the password to avoid predictable ordering
        random.shuffle(password)
        
        return ''.join(password)
    
    def generate_with_requirements(self, length=None, use_lower=True, use_upper=True,
                                   use_digits=True, use_symbols=True):
        """
        Generate a password with specific character type requirements.
        Ensures at least one character from each enabled character type.
        
        Args:
            length (int): Password length. Defaults to None (uses instance length)
            use_lower (bool): Include lowercase letters. Defaults to True
            use_upper (bool): Include uppercase letters. Defaults to True
            use_digits (bool): Include digits. Defaults to True
            use_symbols (bool): Include special symbols. Defaults to True
            
        Returns:
            str: Generated password with specified requirements
        """
        pwd_length = length if length is not None else self.length
        
        # Build character set based on requirements
        charset = ""
        password = []
        
        if use_lower:
            charset += string.ascii_lowercase
            password.append(random.choice(string.ascii_lowercase))
        
        if use_upper:
            charset += string.ascii_uppercase
            password.append(random.choice(string.ascii_uppercase))
        
        if use_digits:
            charset += string.digits
            password.append(random.choice(string.digits))
        
        if use_symbols:
            charset += self.charset_symbols
            password.append(random.choice(self.charset_symbols))
        
        # Fill remaining positions with random characters from charset
        remaining_length = pwd_length - len(password)
        if remaining_length > 0 and charset:
            password.extend(random.choice(charset) for _ in range(remaining_length))
        
        # Shuffle to randomize position
        random.shuffle(password)
        
        return ''.join(password)
    
    def validate_pattern(self, pattern):
        """
        Validate if a pattern string is valid.
        
        Args:
            pattern (str): Pattern to validate
            
        Returns:
            bool: True if pattern is valid (contains only L, U, N, S)
        """
        if not pattern:
            return False
        
        valid_codes = set('LUNS')
        return all(code.upper() in valid_codes for code in pattern)
    
    def set_length(self, length):
        """
        Set the default password length.
        
        Args:
            length (int): New default length
        """
        if length > 0:
            self.length = length
    
    def get_length(self):
        """
        Get the current default password length.
        
        Returns:
            int: Current default length
        """
        return self.length
    
    def generate_memorable(self, length=None):
        """
        Generate a more memorable password using readable patterns.
        Uses alternating consonants and vowels with numbers.
        
        Args:
            length (int): Password length. Defaults to None (uses instance length)
            
        Returns:
            str: Generated memorable password
        """
        pwd_length = length if length is not None else self.length
        
        consonants = 'bcdfghjklmnprstvwxyz'
        vowels = 'aeiou'
        digits = string.digits
        
        password = []
        
        # Alternate between consonants and vowels with occasional digits
        for i in range(pwd_length):
            if i % 3 == 0:
                password.append(random.choice(consonants))
            elif i % 3 == 1:
                password.append(random.choice(vowels))
            else:
                password.append(random.choice(digits))
        
        # Add at least one uppercase letter
        if password:
            idx = random.randint(0, len(password) - 1)
            password[idx] = password[idx].upper()
        
        # Add at least one symbol
        if len(password) > 1:
            idx = random.randint(0, len(password) - 1)
            password[idx] = random.choice(self.charset_symbols)
        
        return ''.join(password)
