from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _


class CarouselItem(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=100, verbose_name=_("Title"))
    image = models.ImageField(upload_to='carousel_images/', verbose_name=_("image"), default="carousel.jpg")
    caption = models.TextField(verbose_name=_("Caption"), null=True, blank=True)
    link = models.URLField(blank=True, verbose_name=_("Link"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive', verbose_name=_("Status"))
    priority = models.IntegerField(default=0, verbose_name=_("Priority"))  # Add this field

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Carousel Item")
        verbose_name_plural = _("Carousel Items")

    def carousel_img(self):
        return mark_safe('<img src="%s" width="50" height="50"/>' % self.image.url)

    carousel_img.short_description = _("Carousel Image")

    def __str__(self):
        return self.title




