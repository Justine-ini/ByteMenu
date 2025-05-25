"""
QR Code Generator Module

This module handles QR code creation for restaurant URLs in a Django web application.
It provides a Django view function that takes user input through a form, generates
a QR code with the specified URL, and saves the QR code as an image in the project's
media directory.

Functions:
- generate_qr_code(request): Handles QR code generation from user input and 
  saves the generated QR code image in 'media/qrcodes/'.

Usage:
- Users enter a restaurant name and URL in a form.
- The system generates a QR code and saves it under 'media/qrcodes/'.
- Errors during QR code generation are handled gracefully using Django's messages framework.

"""
from pathlib import Path
from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
import qrcode
from .forms import QRCodeForm

def generate_qr_code(request):
    """Generate and save QR code for restaurant URL to media directory."""
    form = QRCodeForm(request.POST or None)
    context = {'form': form}

    if request.method == "POST" and form.is_valid():
        try:
            cleaned_data = form.cleaned_data
            restaurant_name = f"{cleaned_data['restaurant_name'].replace(' ', '_')}_Menu"
            url = cleaned_data['url']

            # Define the path for saving the QR code image
            img_path = Path(f"qrcodes/{restaurant_name}.png")
            full_path = settings.MEDIA_ROOT / img_path

            # Ensure directory exists
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Generate and Save QR code
            qr = qrcode.QRCode(version=1, box_size=5, border=5)
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color='green', back_color='white')
            img.save(str(full_path))

            # Store in session for redirect
            request.session['generated_qr'] = {
                'path': str(img_path),
                'restaurant': restaurant_name,
                'url': url
            }
            messages.success(request, f"QR code generated successfully for {restaurant_name}.")
            return redirect('generate_qr_code')

        except (OSError, qrcode.exceptions.DataOverflowError) as e:
            messages.error(request, f"Error generating QR code: {str(e)}")

    # Handle QR data after redirect
    if 'generated_qr' in request.session:
        qr_data = request.session.pop('generated_qr')
        context.update({
            'qr_code_path': f"{settings.MEDIA_URL}{qr_data['path']}",
            'restaurant_name': qr_data['restaurant'],
            'url': qr_data['url']
        })

    return render(request, 'generate_qr_code.html', context)
