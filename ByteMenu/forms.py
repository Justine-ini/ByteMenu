"""
QR Code Form Module

Handles user input validation for generating restaurant QR codes in Django. 
Includes fields for restaurant name and digital menu URL, ensuring proper formatting.
"""

from django import forms
from django.utils.html import format_html
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import URLValidator

class QRCodeForm(forms.Form):
    """
    Form for generating restaurant QR codes.

    Includes fields for restaurant name and digital menu URL, ensuring proper validation 
    for input formatting and URL structure.
    """
    restaurant_name = forms.CharField(
        label='Restaurant Name',
        max_length=100,
        min_length=2,
        strip=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., The Gourmet House',
            'autofocus': True
        }),
        help_text='Enter the official restaurant name (2-100 characters)'
    )

    url = forms.URLField(
        label='Digital Menu URL',
        max_length=200,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://example.com/digital-menu',
            'pattern': 'https?://.+',
            'inputmode': 'url'
        }),
        help_text=format_html(
            'Valid URL starting with <code>http://</code> or <code>https://</code>'
            )
    )

    def clean_restaurant_name(self):
        """
        Cleans and validates the restaurant name input.

        - Strips leading and trailing whitespace.
        - Ensures the name only contains letters, numbers, spaces, apostrophes, and hyphens.
        - Raises a validation error if the name contains invalid characters.

        Returns:
            str: The cleaned and validated restaurant name.
        """
        name = self.cleaned_data['restaurant_name'].strip()
        validator = RegexValidator(
            regex=r"^[A-Za-z0-9\s'-]+$",
            message="Name can only contain letters, numbers, spaces, apostrophes, and hyphens."
        )
        validator(name)
        return name

    def clean_url(self):
        """
        Cleans and validates the URL input.

        - Strips leading and trailing whitespace.
        - Ensures the URL starts with 'http://' or 'https://'.
        - Raises a validation error if the URL format is invalid.

        Returns:
            str: The cleaned and validated URL.
        """
        url = self.cleaned_data['url'].strip()
        validator = URLValidator(schemes=['http', 'https'])
        try:
            validator(url)
        except ValidationError as exc:
            raise ValidationError('URL must start with http:// or https://') from exc
        return url
