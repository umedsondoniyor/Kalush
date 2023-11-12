from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from Product.models import Product
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_("User"))
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True,
                                        blank=True, verbose_name=_("Profile Picture"))
    bio = models.TextField(blank=True, verbose_name=_("Biography"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Birthdate"))
    phone_number = PhoneNumberField(null=True, blank=True, verbose_name=_("Phone number"))

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return str(self.user.username)


class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s Location"


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    street = models.CharField(max_length=100, verbose_name=_("Street"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    country = models.CharField(max_length=100, verbose_name=_("Country"))
    postal_code = models.CharField(max_length=20, verbose_name=_("Postal Code"))
    phone_number = PhoneNumberField(verbose_name=_("Phone number"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")

    def __str__(self):
        return f"{self.user.username}'s Address"


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("User"))
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name=_("Product"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Wish List")
        verbose_name_plural = _("Wish Lists")

    def __str__(self):
        return f"{self.product.title} - {self.user}"





