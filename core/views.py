from django.shortcuts import render
from .forms import QRCodeForm
import segno
from django.conf import settings
import os

def generate_qr_code(request):
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            res_name = form.cleaned_data['restaurant_name']
            url = form.cleaned_data['url']
            qrcode = segno.make(url, error='h')
            file_name = res_name.replace(" ", "_").lower() + "_menu.png"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            qrcode.save(file_path, scale=4, dark='yellow', data_dark='pink', data_light='skyblue')

            qr_url = os.path.join(settings.MEDIA_URL, file_name)
            return render(request, 'qr_code_generated.html', {'res_name': res_name, 'qr_url': qr_url, 'file_name': file_name})
    else:
        form = QRCodeForm(request.POST or None)
        context = {
        'form': form,
        }
        return render(request, 'generate_qr_code.html', context=context)
