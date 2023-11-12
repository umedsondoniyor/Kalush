from io import BytesIO
from PIL import Image
from django.core.files import File
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


status = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('published', 'Published'),
)

rating = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=15, max_length=20, prefix='cat')
    title = models.CharField(max_length=100, verbose_name=_("Category Name"))
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories',
                               on_delete=models.CASCADE, verbose_name=_("Parent Category"))
    image = models.ImageField(upload_to="category", default="category.jpg", verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title

    def category_img(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % self.image.url)

    category_img.short_description = _("Category Image")


class Tags(models.Model):
    pass


class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Brand Name"))
    description = models.TextField(verbose_name=_("Description"))
    logo = models.ImageField(upload_to='brand_logos/', null=True, blank=True, verbose_name=_('logo'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name


class Product(models.Model):
    def upload_file_name(self, filename):
        p_pid = self.pid
        return f'products/{p_pid}/image/{filename}'

    def upload_thumb(self, filename):
        p_pid = self.pid
        return f'products/{p_pid}/thumbnail/{filename}'
    pid = ShortUUIDField(unique=True, length=15, max_length=20, prefix='prd')
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    image = models.ImageField(upload_to=upload_file_name, default="product.jpg", verbose_name=_('image'))
    thumbnail = models.ImageField(upload_to=upload_thumb, default="thumb.jpg", null=True, blank=True,
                                  verbose_name=_('thumbnail'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("User"))
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Brand'))
    category = models.ManyToManyField(Category, verbose_name=_('Category'))
    description = models.TextField(verbose_name=_('description'))
    price = models.DecimalField(max_digits=99, decimal_places=2, default=1.50, verbose_name=_('price'))
    old_price = models.DecimalField(max_digits=99, decimal_places=2, default=2.50, verbose_name=_('old_price'))
    specification = models.TextField(null=True, blank=True, verbose_name=_('specification'))
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices=status, max_length=10, default="in_review",
                                      verbose_name=_('Product Status'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))
    status = models.BooleanField(default=True, verbose_name=_('Status'))
    in_stock = models.BooleanField(default=True, verbose_name=_('In Stock'))
    featured = models.BooleanField(default=False, verbose_name=_('Featured'))
    digital = models.BooleanField(default=False, verbose_name=_('digital'))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % self.image.url)
    product_image.short_description = _("Product Image")

    def __str__(self):
        return self.title

    def get_percentage(self):
        new_price = (self.price/self.old_price)*100
        return round(new_price)


class ProductImage(models.Model):
    images = models.ImageField(upload_to='product_images/', default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_images')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return _("Image for {product}").format(product=self.product)

    def save(self, *args, **kwargs):
        img = Image.open(self.images)
        max_width = 500
        max_height = 500
        if img.width > max_width or img.height > max_height:
            new_size = (max_width, max_height)
            img.thumbnail(new_size)
            temp_buffer = BytesIO()
            img.save(temp_buffer, format='JPEG')
            temp_buffer.seek(0)
            resized_image = File(temp_buffer)
            self.images.save(f'{self.images.name}.jpg', resized_image)

        super(ProductImage, self).save(*args, **kwargs)


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name=_('product'))
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name=_('Stock Quantity'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    def __str__(self):
        return _("Inventory for {product}").format(product=self.product)


class Size(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Size Name'))

    class Meta:
        verbose_name = _('Product Size')
        verbose_name_plural = _("Product Sizes")

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('color name'))
    code = models.CharField(max_length=7, verbose_name=_('color code'))  # Assuming hexadecimal value like '#FFFFFF'

    class Meta:
        verbose_name = _('Product Color')
        verbose_name_plural = _("Product Colors")

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    def upload_file_name(self, filename):
        p_pid = self.product.pid
        return f'products/{p_pid}/variants/image/{filename}'

    def upload_thumb(self, filename):
        p_pid = self.product.pid
        return f'products/{p_pid}/variants/thumbnails/{filename}'
    pvid = ShortUUIDField(unique=True, length=15, max_length=20, prefix='pvid')
    title = models.CharField(max_length=70, default="ProductVariant")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'),
                                related_name='product_variants')
    image = models.ImageField(upload_to=upload_file_name, default="product.jpg", verbose_name=_('image'))
    thumbnail = models.ImageField(upload_to=upload_thumb, default="thumb.jpg", null=True, blank=True,
                                  verbose_name=_('thumbnail'))
    specification = models.TextField(null=True, blank=True, verbose_name=_('specification'))
    product_status = models.CharField(choices=status, max_length=10, default="in_review",
                                      verbose_name=_('Product Status'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    old_price = models.DecimalField(max_digits=10, decimal_places=2, default=100, verbose_name=_('Old Price'))
    sku = models.CharField(max_length=50, unique=True, help_text=_("Stock Keeping Unit"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))
    featured = models.BooleanField(default=False, verbose_name=_("Featured"))

    class Meta:
        verbose_name = _('Product Variant')
        verbose_name_plural = _("Product Variants")

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % self.image.url)

    def __str__(self):
        return f"{self.product} - {self.title}"


class ProductVariantImage(models.Model):
    def upload_file_name(self, filename):
        p_pid = self.product_variant.product.pid
        return f'products/{p_pid}/variants/image/{filename}'
    images = models.ImageField(upload_to='product_images/', default="product.jpg")
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Product Variant Image')
        verbose_name_plural = _("Product Variant Images")

    def __str__(self):
        return _("Image for {product}").format(product=self.product_variant)


class ProductCombination(models.Model):
    product_v = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name=_('ProductVariant'),
                                  related_name='product_v_combination')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name=_('Size'),
                             related_name='product_c_size')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, verbose_name=_('Color'),
                              related_name='product_c_color')
    inventory = models.PositiveIntegerField(default=0, verbose_name=_("Inventory"),
                                            help_text=_("Available stock for this variant"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _('Product Combination')
        verbose_name_plural = _("Product Combinations")

    def __str__(self):
        return f"{self.product_v} - {self.size} - {self.color}"


class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('User'))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name=_('Product'))
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Title'))
    review = models.TextField(verbose_name=_('Review'))
    rating = models.IntegerField(choices=rating, default=None, verbose_name=_('Rating'))
    verified_purchase = models.BooleanField(default=False, verbose_name=_('Verified purchase'))
    user_location = models.ForeignKey('Profile.UserLocation', on_delete=models.SET_NULL,
                                      blank=True, null=True, verbose_name=_('User location'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated at'))

    class Meta:
        verbose_name = _("Product Review")
        verbose_name_plural = _("Product Reviews")

    def __str__(self):
        return f"{self.product.title} - {self.user} - {self.rating}"

    def get_rating(self):
        return self.rating

