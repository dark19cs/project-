"""
Password History Module
Manages password history with file persistence and history operations.
"""

import json
import os
from datetime import datetime
from config import PASSWORD_HISTORY_LIMIT


class PasswordHistory:
    """
    Manages password history with persistent storage to JSON file.
    Tracks generated passwords with timestamps and metadata.
    """
    
    def __init__(self, history_file="password_history.json"):
        """
        Initialize the PasswordHistory manager.
        
        Args:
            history_file (str): Path to the JSON file for storing history.
                               Defaults to 'password_history.json'
        """
        self.history_file = history_file
        self.history = []
        self._load_from_file()
    
    def _load_from_file(self):
        """
        Load password history from the JSON file if it exists.
        If file doesn't exist, initialize with empty history.
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or unreadable, start fresh
                self.history = []
        else:
            self.history = []
    
    def _save_to_file(self):
        """
        Save the current history to the JSON file.
        Maintains the history state across application restarts.
        """
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError as e:
            print(f"Error saving history: {e}")
    
    def add_password(self, password):
        """
        Add a password to history if it's unique and within limit.
        Automatically maintains the history limit by removing oldest entries.
        
        Args:
            password (str): The password to add to history
            
        Returns:
            bool: True if password was added, False if it already exists or is empty
        """
        # Reject empty passwords
        if not password:
            return False
        
        # Check if password already exists in history
        for entry in self.history:
            if entry.get('password') == password:
                return False  # Password already in history
        
        # Create new history entry with timestamp
        entry = {
            'password': password,
            'timestamp': datetime.now().isoformat(),
            'strength': 'unknown'
        }
        
        self.history.append(entry)
        
        # Enforce history limit by removing oldest entries
        if len(self.history) > PASSWORD_HISTORY_LIMIT:
            self.history.pop(0)
        
        # Persist changes to file
        self._save_to_file()
        return True
    
    def add_password_with_strength(self, password, strength_level):
        """
        Add a password to history with strength information.
        
        Args:
            password (str): The password to add
            strength_level (str): Strength level ('weak', 'medium', 'strong')
            
        Returns:
            bool: True if password was added
        """
        if not password:
            return False
        
        # Check if password already exists
        for entry in self.history:
            if entry.get('password') == password:
                return False
        
        entry = {
            'password': password,
            'timestamp': datetime.now().isoformat(),
            'strength': strength_level
        }
        
        self.history.append(entry)
        
        if len(self.history) > PASSWORD_HISTORY_LIMIT:
            self.history.pop(0)
        
        self._save_to_file()
        return True
    
    def get_all(self):
        """
        Get all passwords in history (without metadata).
        
        Returns:
            list: List of all password strings in history
        """
        return [entry['password'] for entry in self.history]
    
    def get_all_with_metadata(self):
        """
        Get all history entries with full metadata.
        
        Returns:
            list: List of dictionaries containing password, timestamp, and strength
        """
        return self.history.copy()
    
    def get_recent(self, count=5):
        """
        Get the most recent passwords from history.
        
        Args:
            count (int): Number of recent passwords to retrieve. Defaults to 5
            
        Returns:
            list: List of the most recent password strings
        """
        return [entry['password'] for entry in self.history[-count:]]
    
    def get_recent_with_metadata(self, count=5):
        """
        Get the most recent passwords with metadata.
        
        Args:
            count (int): Number of recent entries to retrieve
            
        Returns:
            list: List of recent history entries with full metadata
        """
        return self.history[-count:]
    
    def clear_history(self):
        """
        Clear all password history.
        Useful for privacy or when starting fresh.
        """
        self.history = []
        self._save_to_file()
    
    def remove_password(self, password):
        """
        Remove a specific password from history.
        
        Args:
            password (str): The password to remove
            
        Returns:
            bool: True if password was found and removed
        """
        for i, entry in enumerate(self.history):
            if entry['password'] == password:
                self.history.pop(i)
                self._save_to_file()
                return True
        return False
    
    def is_empty(self):
        """
        Check if history is empty.
        
        Returns:
            bool: True if no passwords in history
        """
        return len(self.history) == 0
    
    def count(self):
        """
        Get the total number of passwords in history.
        
        Returns:
            int: Number of passwords in history
        """
        return len(self.history)
