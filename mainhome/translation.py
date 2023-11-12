from .models import CarouselItem
from modeltranslation.translator import translator, TranslationOptions


class CarouselItemTranslationOptions(TranslationOptions):
    fields = ('title', 'caption', 'status')


translator.register(CarouselItem, CarouselItemTranslationOptions)




