from django.contrib import admin
from .models import Profile, Address, UserLocation, WishList


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'date_of_birth', 'phone_number']
    list_filter = ['user']
    list_per_page = 50
    search_fields = ['user']


class UserLocationAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'city']
    list_filter = ['user']
    list_per_page = 50
    search_fields = ['user', 'country', 'city']


class AdressAdmin(admin.ModelAdmin):
    list_display = ['user', 'country', 'city', 'phone_number']
    list_filter = ['user', 'country', 'city']
    list_per_page = 50
    search_fields = ['user', 'country', 'city', 'street', 'phone_number']


class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['user', 'product']
    list_per_page = 50
    search_fields = ['user']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserLocation, UserLocationAdmin)
admin.site.register(Address, AdressAdmin)
admin.site.register(WishList, WishListAdmin)


