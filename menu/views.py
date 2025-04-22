from django.shortcuts import render
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
from PIL import Image
import io
from django.core.files.base import ContentFile

def index(request):
    return render(request, 'base.html')


def generate_qr_code(qr_customization):
    qr = qrcode.QRCode(
        version=1,
        error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{qr_customization.error_correction}'),
        box_size=10,
        border=4,
    )

    if qr_customization.use_custom_url and qr_customization.custom_url:
        url = qr_customization.custom_url
    else:
        url = f"https://yourdomain.com/menu/{qr_customization.restaurant.id}/"

    qr.add_data(url)
    qr.make(fit=True)

    module_drawer = None
    if qr_customization.corner_style == 'rounded':
        module_drawer = RoundedModuleDrawer()
    elif qr_customization.corner_style == 'dot':
        module_drawer = CircleModuleDrawer()

    img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=module_drawer,
        color_mask=RadialGradiantColorMask(
            back_color=qr_customization.background_color,
            center_color=qr_customization.foreground_color,
            edge_color=qr_customization.foreground_color
        )
    )

    if qr_customization.include_logo and qr_customization.restaurant.image:
        logo = Image.open(qr_customization.restaurant.image.path)

        logo_size = int(img.size[0] * (qr_customization.logo_size_percentage / 100))
        logo = logo.resize((logo_size, logo_size))

        pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)

        logo_bg = Image.new('RGBA', logo.size, qr_customization.background_color)
        img.paste(logo_bg, pos)
        img.paste(logo, pos)

    img = img.resize((qr_customization.size_pixels, qr_customization.size_pixels))

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    file_name = f"qr_{qr_customization.restaurant.id}.png"
    qr_customization.generated_qr_image.save(file_name, ContentFile(buffer.read()), save=True)

    return qr_customization.generated_qr_image.url
