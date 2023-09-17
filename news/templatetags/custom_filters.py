from django import template

register = template.Library()

class CensorException(Exception):
    pass

# Регистрируем фильтр
@register.filter()

#фильтр censor, который заменяет буквы нежелательных слов в заголовках и текстах статей на символ «*»
def censor(value):
    bad_words = ['грибок', 'бля', 'этим', 'блин']
    try:
        if not isinstance(value, str):
            raise CensorException('Цензурироваться может только строковой тип данных (str).')

        for word in bad_words:
            if word.lower() in bad_words:
                value = value.replace(word, f"{word[0]}{'*' * (len(word) - 1)}")
        return value

    except CensorException as e:
        print(e)
