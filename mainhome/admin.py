from io import BytesIO
from PIL import Image
from django.contrib import admin
from django.core.files import File
from modeltranslation.admin import TranslationAdmin
from mainhome.models import CarouselItem


def resize_image(image_field, max_width=1366, max_height=800, ):
    if image_field:
        img = Image.open(image_field)
        # img = img.resize((width, height), Image.Resampling.LANCZOS)
        width, height = img.size
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        temp_buffer = BytesIO()
        img.save(temp_buffer, format='JPEG')
        temp_buffer.seek(0)
        resized_image = File(temp_buffer)
        return resized_image


@admin.register(CarouselItem)
class CarouselAdmin(TranslationAdmin):
    list_display = ['title', 'carousel_img', 'priority', 'status']
    list_filter = ['title', 'status']
    list_per_page = 50
    search_fields = ['title']

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    def save_model(self, request, obj, form, change):
        resized_image = resize_image(obj.image)
        obj.image.save(f'{obj.title}.jpg', resized_image)
        super().save_model(request, obj, form, change)



