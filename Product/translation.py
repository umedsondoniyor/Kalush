from .models import Product, Category, Brand, Size, Color, ProductVariant
from modeltranslation.translator import translator, TranslationOptions


class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'specification', 'product_status')


class CategoryTranslationOptions(TranslationOptions):
    fields = ('title', )


class BrandTranslationOptions(TranslationOptions):
    fields = ('name', )


class SizeTranslationOptions(TranslationOptions):
    fields = ('name', )


class ColorTranslationOptions(TranslationOptions):
    fields = ('name', )


class PVariantTranslationOptions(TranslationOptions):
    fields = ('title', 'specification', 'product_status')


# Register the translation options for the Product model
translator.register(Product, ProductTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Brand, BrandTranslationOptions)
translator.register(Size, SizeTranslationOptions)
translator.register(Color, ColorTranslationOptions)
translator.register(ProductVariant, PVariantTranslationOptions)

