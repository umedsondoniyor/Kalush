from io import BytesIO
from django.contrib import admin
from .models import Product, ProductImage, ProductVariant, ProductReview, Category, Inventory,\
    Size, Color, ProductCombination, ProductVariantImage
from PIL import Image
from django.core.files import File
from modeltranslation.admin import TranslationAdmin


def resize_image(image_field, target_ratio=(333, 500)):
    if image_field:
        img = Image.open(image_field)
        if img.mode not in ['RGB', 'CMYK']:
            # Convert the image to RGB mode before saving as JPEG
            img = img.convert('RGB')
        width, height = img.size
        current_ratio = width / height

        if current_ratio != target_ratio[0] / target_ratio[1]:
            # Calculate new dimensions to maintain the target ratio
            if current_ratio > target_ratio[0] / target_ratio[1]:
                new_width = int(height * target_ratio[0] / target_ratio[1])
                left = (width - new_width) // 2
                right = left + new_width
                top = 0
                bottom = height
            else:
                new_height = int(width * target_ratio[1] / target_ratio[0])
                top = (height - new_height) // 2
                bottom = top + new_height
                left = 0
                right = width

            # Crop the image
            img = img.crop((left, top, right, bottom))

        thumb_img = img.resize(target_ratio, Image.Resampling.LANCZOS)

        # Save the cropped image
        cropped_buffer = BytesIO()
        img.save(cropped_buffer, format='JPEG')
        cropped_buffer.seek(0)
        cropped_image = File(cropped_buffer)

        # Save the thumbnail image
        thumb_buffer = BytesIO()
        thumb_img.save(thumb_buffer, format='JPEG')
        thumb_buffer.seek(0)
        thumb_image = File(thumb_buffer)

        return cropped_image, thumb_image


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImage


class InventoryAdmin(admin.TabularInline):
    model = Inventory


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [ProductImagesAdmin, InventoryAdmin]
    list_display = ['title', 'user', 'product_image', 'price', 'featured', 'product_status']
    list_filter = ['title']
    list_editable = ['product_status', ]
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['title']
    exclude = ('created_at', 'updated_at', 'thumbnail')

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
        old_product = None
        if change:
            try:
                old_product = Product.objects.get(pk=obj.id)
                if old_product.image != obj.image:
                    old_product.image.delete()  # Delete the old image file
            except Product.DoesNotExist:
                pass

            if obj.image and obj.image != old_product.image:  # Check if new image is selected and it's different
                cropped_image, thumb_image = resize_image(obj.image)
                obj.image.save(f'{obj.title}.jpg', cropped_image)
                obj.thumbnail.save(f'{obj.title}_thumb.jpg', thumb_image)
        elif not change and obj.image:
            cropped_image, thumb_image = resize_image(obj.image)
            obj.image.save(f'{obj.title}.jpg', cropped_image)
            obj.thumbnail.save(f'{obj.title}_thumb.jpg', thumb_image)

        super().save_model(request, obj, form, change)


class ProductCombinationAdmin(admin.TabularInline):
    model = ProductCombination


class ProductVariantImageAdmin(admin.TabularInline):
    model = ProductVariantImage


@admin.register(ProductVariant)
class ProductVariantAdmin(TranslationAdmin):
    inlines = [ProductCombinationAdmin, ProductVariantImageAdmin]
    list_display = ['product', 'price', 'product_image', 'product_status', 'created_at']
    list_filter = ['created_at']
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['sku']

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
        old_product = None
        if change:
            try:
                old_product = ProductVariant.objects.get(pk=obj.id)
                if old_product.image != obj.image:
                    old_product.image.delete()  # Delete the old image file
            except Product.DoesNotExist:
                pass

            if obj.image and obj.image != old_product.image:  # Check if new image is selected and it's different
                cropped_image, thumb_image = resize_image(obj.image)
                obj.image.save(f'{obj.title}.jpg', cropped_image)
                obj.thumbnail.save(f'{obj.title}_thumb.jpg', thumb_image)
        elif not change and obj.image:
            cropped_image, thumb_image = resize_image(obj.image)
            obj.image.save(f'{obj.title}.jpg', cropped_image)
            obj.thumbnail.save(f'{obj.title}_thumb.jpg', thumb_image)

        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ['title', 'category_img', 'parent']
    list_filter = ['title']
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
        resized_image, thumb = resize_image(obj.image, target_ratio=(500, 500))
        obj.image.save(f'{obj.title}.jpg', resized_image)
        super().save_model(request, obj, form, change)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'title', 'review', 'rating', 'verified_purchase', 'user_location', 'created_at']
    list_filter = ['created_at']
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['user', 'product']


@admin.register(Color)
class ColorAdmin(TranslationAdmin):
    list_display = ['name', "code"]
    list_filter = ['name']
    list_per_page = 50
    search_fields = ['name']

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Size)
class ColorAdmin(TranslationAdmin):
    list_display = ['name', ]
    list_filter = ['name']
    list_per_page = 50
    search_fields = ['name']

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


admin.site.register(ProductReview, ProductReviewAdmin)







