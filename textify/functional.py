import re
from enum import Enum
from typing import List, Set, Union, Tuple

import pyarabic.araby as araby
import unicodedata
from nltk.corpus import stopwords
from num2words import num2words

ARABIC_STOPWORDS = set(stopwords.words('arabic'))
ENGLISH_STOPWORDS = set(stopwords.words('english'))


class Patterns(Enum):
    WHITESPACES = re.compile(r'\s+')
    PUNCTUATIONS = re.compile(r'[^\w\s]')
    URL = re.compile(r'https?\S+')
    EMAIL = re.compile(r'\S+@\S+')
    # non-Arabic or non-English characters or numbers
    FOREIGN_CHARS = re.compile(r'[^\w\s\d\u0600-\u06FF]')
    NON_ENGLISH = re.compile(r'[^A-Za-z0-9]')
    NON_ARABIC = re.compile(r'[^\u0621-\u064A0-9]')
    NUMBERS = re.compile(r"\d*\.\d+|\d+")


def remove_pattern(text: str, pattern: re.Pattern, replace_by: str = ' ') -> str:
    return re.sub(pattern, replace_by, text)


def collapse_spaces(text: str) -> str:
    return remove_pattern(text, Patterns.WHITESPACES.value, ' ')


def remove_punctuation(text: str) -> str:
    return remove_pattern(text, Patterns.PUNCTUATIONS.value)


def remove_url(text: str) -> str:
    return remove_pattern(text, Patterns.URL.value)


def remove_email(text: str) -> str:
    return remove_pattern(text, Patterns.EMAIL.value)


def keep_english_only(text: str) -> str:
    return remove_pattern(text, Patterns.NON_ENGLISH.value)


def keep_arabic_only(text: str) -> str:
    return remove_pattern(text, Patterns.NON_ARABIC.value)


def keep_arabic_english_numbers_only(text: str) -> str:
    return remove_pattern(text, Patterns.FOREIGN_CHARS.value)


def normalize_unicode(text: str) -> str:
    return unicodedata.normalize("NFKD", text)


def remove_words(text: str, words_collection: Union[List, Set, Tuple]) -> str:
    words = [word for word in text.split() if word not in words_collection]
    return " ".join(words)


def remove_arabic_stopwords(text: str) -> str:
    return remove_words(text, ARABIC_STOPWORDS)


def remove_english_stopwords(text: str) -> str:
    return remove_words(text, ENGLISH_STOPWORDS)


def lower_case(text: str) -> str:
    return text.lower()


def upper_case(text: str) -> str:
    return text.upper()


def strip_text(text: str) -> str:
    return text.strip()


def remove_arabic_diacritics(sentence: str) -> str:
    return araby.strip_tashkeel(sentence)


def number_to_words(number: Union[int, float], lang: str) -> str:
    return num2words(number, lang=lang)


def number_to_words_english(number: Union[int, float]) -> str:
    return number_to_words(number, lang='en')


def number_to_words_arabic(number: Union[int, float]) -> str:
    return number_to_words(number, lang='ar')


def normalize_numbers(text: str, lang: str) -> str:
    numbers = set(re.findall(Patterns.NUMBERS.value, text))
    words = {number: number_to_words(int(number), lang=lang) for number in numbers}
    for number, word in words.items():
        text = text.replace(number, word)
    return text


def normalize_arabic_numbers(text: str) -> str:
    lang = 'ar'
    numbers = set(re.findall(Patterns.NUMBERS.value, text))
    words = {number: number_to_words(int(number), lang=lang) for number in numbers}
    for number, word in words.items():
        text = text.replace(number, word)
    return text


def normalize_english_numbers(text: str) -> str:
    lang = 'en'
    numbers = set(re.findall(Patterns.NUMBERS.value, text))
    words = {number: number_to_words(int(number), lang=lang) for number in numbers}
    for number, word in words.items():
        text = text.replace(number, word)
    return text


def replace_numbers(text: str, replace_by: str) -> str:
    numbers = set(re.findall(Patterns.NUMBERS.value, text))
    for number in numbers:
        text = text.replace(number, replace_by)
    return text


def replace_arabic_numbers(text: str) -> str:
    return replace_numbers(text, "قيمة عددية")


def replace_english_numbers(text: str) -> str:
    return replace_numbers(text, 'numerical value')


def normalize_characters(text: str, old_values: str, new_value: str) -> str:
    return re.sub(f"[{old_values}]", new_value, text)


def arabic_hamza_normalize(text: str) -> str:
    return normalize_characters(text, "ءاآأؤإئى", "ا")


def arabic_tah_normalize(text: str) -> str:
    return normalize_characters(text, 'ة', "ه")


def truncate_characters(text):
    pattern = r'(.)\1+'
    return re.sub(pattern, r'\1\1', text)
