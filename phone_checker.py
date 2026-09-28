"""
Phone Checker - Utility to validate phone numbers

This module provides functions to validate and check phone numbers
for correctness, format, and authenticity.

Author: runethack
License: MIT
"""

import re
from typing import Dict, Tuple


class PhoneChecker:
    """
    A class to validate phone numbers based on various criteria.
    
    Supports:
    - International phone numbers (E.164 format)
    - Russian phone numbers
    - US/Canada phone numbers
    - Basic format validation
    """
    
    # Regular expressions for different formats
    PATTERNS = {
        'international': r'^\+?[1-9]\d{1,14}$',  # E.164 format
        'russian': r'^(\+7|8)?[-\s]?\(?[0-9]{3}\)?[-\s]?[0-9]{3}[-\s]?[0-9]{2}[-\s]?[0-9]{2}$',
        'us_canada': r'^(\+1)?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$',
        'simple': r'^[+\d\-\s()]+$',
    }
    
    @staticmethod
    def is_valid_format(phone: str) -> bool:
        """
        Check if phone number has valid format.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if format is valid, False otherwise
        """
        if not phone or not isinstance(phone, str):
            return False
        
        # Remove spaces for basic check
        cleaned = phone.replace(' ', '')
        
        # Must contain at least digits and optional + sign
        if not re.match(PhoneChecker.PATTERNS['simple'], cleaned):
            return False
        
        # Extract only digits
        digits_only = re.sub(r'\D', '', cleaned)
        
        # Valid phone should have 10-15 digits
        return 10 <= len(digits_only) <= 15
    
    @staticmethod
    def is_russian_phone(phone: str) -> bool:
        """
        Check if phone number is valid Russian format.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if Russian format, False otherwise
        """
        if not phone:
            return False
        
        return bool(re.match(PhoneChecker.PATTERNS['russian'], phone))
    
    @staticmethod
    def is_us_canada_phone(phone: str) -> bool:
        """
        Check if phone number is valid US/Canada format.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if US/Canada format, False otherwise
        """
        if not phone:
            return False
        
        return bool(re.match(PhoneChecker.PATTERNS['us_canada'], phone))
    
    @staticmethod
    def is_international_e164(phone: str) -> bool:
        """
        Check if phone number matches E.164 international format.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if E.164 format, False otherwise
        """
        if not phone:
            return False
        
        return bool(re.match(PhoneChecker.PATTERNS['international'], phone))
    
    @staticmethod
    def validate(phone: str) -> Dict[str, any]:
        """
        Comprehensive phone validation with detailed results.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            dict: Validation results including:
                - is_valid (bool): Overall validity
                - is_format_valid (bool): Format check
                - is_russian (bool): Russian format
                - is_us_canada (bool): US/Canada format
                - is_e164 (bool): E.164 format
                - digits_only (str): Phone digits without formatting
                - digit_count (int): Number of digits
                - length_valid (bool): Digit count in valid range
        """
        digits_only = re.sub(r'\D', '', phone) if phone else ''
        digit_count = len(digits_only)
        
        results = {
            'input': phone,
            'is_format_valid': PhoneChecker.is_valid_format(phone),
            'is_russian': PhoneChecker.is_russian_phone(phone),
            'is_us_canada': PhoneChecker.is_us_canada_phone(phone),
            'is_e164': PhoneChecker.is_international_e164(phone),
            'digits_only': digits_only,
            'digit_count': digit_count,
            'length_valid': 10 <= digit_count <= 15,
        }
        
        # Overall validation: format valid AND (Russian OR US/Canada OR E.164)
        results['is_valid'] = (
            results['is_format_valid'] and 
            results['length_valid'] and
            (results['is_russian'] or results['is_us_canada'] or results['is_e164'])
        )
        
        return results
    
    @staticmethod
    def get_country_code(phone: str) -> str:
        """
        Attempt to determine country code from phone number.
        
        Args:
            phone (str): Phone number to analyze
            
        Returns:
            str: Country code or 'UNKNOWN'
        """
        digits = re.sub(r'\D', '', phone) if phone else ''
        
        if digits.startswith('7'):
            return 'RU (Russia)'
        elif digits.startswith('1'):
            return 'US/CA (USA/Canada)'
        elif len(digits) > 2:
            return digits[:3]  # Return first 3 digits as potential country code
        
        return 'UNKNOWN'


def main():
    """Example usage of PhoneChecker"""
    print("=" * 60)
    print("PHONE CHECKER - Phone Number Validator")
    print("=" * 60)
    
    test_numbers = [
        '+7 (495) 123-45-67',      # Russian
        '8-800-555-35-35',         # Russian
        '+1 (555) 123-4567',       # US
        '555-123-4567',            # US
        '+48123456789',            # International (Poland)
        '123',                     # Too short
        'invalid',                 # Not a number
        '+79991234567',            # Russian E.164
        '+12025551234',            # US E.164
    ]
    
    for number in test_numbers:
        print(f"\nTesting: {number}")
        result = PhoneChecker.validate(number)
        print(f"  Valid: {result['is_valid']}")
        print(f"  Format: {result['is_format_valid']}")
        print(f"  Russian: {result['is_russian']}")
        print(f"  US/Canada: {result['is_us_canada']}")
        print(f"  E.164: {result['is_e164']}")
        print(f"  Digits: {result['digits_only']} ({result['digit_count']} digits)")
        print(f"  Country: {PhoneChecker.get_country_code(number)}")


if __name__ == '__main__':
    main()
