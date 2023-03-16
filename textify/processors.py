from typing import List, Union

from .functional import (normalize_unicode, remove_url, remove_email,
                         keep_arabic_english_numbers_only,
                         lower_case, truncate_characters,
                         collapse_spaces, strip_text)
from .functional import (remove_arabic_diacritics, remove_arabic_stopwords,
                         arabic_hamza_normalize, arabic_tah_normalize,
                         replace_arabic_numbers, normalize_arabic_numbers,
                         keep_arabic_only)
from .functional import (replace_english_numbers, normalize_english_numbers,
                         remove_english_stopwords, keep_english_only)
from .utils import Pipeline


class Processor:
    def __init__(self, *args, n_jobs: int = -2, lang: str = "ar", channel: str = "text"):
        self.pipeline = Pipeline(*args)
        self.n_jobs = n_jobs

        assert lang in {"ar", "en", "neutral"}
        self.lang = lang

        assert channel in {"voice", "text", "neutral"}
        self.channel = channel

    def __call__(self, text: Union[str, List[str]]) -> Union[str, List[str]]:
        return self.pipeline(text, self.n_jobs)


class NeutralProcessor(Processor):
    def __init__(self, n_jobs: int = -2):
        lang = "neutral"
        channel = "text"
        functions = [remove_url, remove_email,
                     keep_arabic_english_numbers_only,
                     lower_case, truncate_characters]

        super().__init__(*functions, lang=lang, channel=channel, n_jobs=n_jobs)


class ArabicProcessor(Processor):
    def __init__(self, keep_numbers: bool = True,
                 remove_stopwords: bool = False,
                 remove_foreign_chars: bool = True,
                 n_jobs: int = -2):

        self.keep_numbers = keep_numbers
        self.remove_foreign_chars = remove_foreign_chars
        self.remove_stopwords = remove_stopwords

        lang = "ar"
        channel = "text"

        functions = [remove_arabic_diacritics]

        if keep_numbers:
            functions.append(normalize_arabic_numbers)
        else:
            functions.append(replace_arabic_numbers)

        if remove_foreign_chars:
            functions.append(keep_arabic_only)

        if remove_stopwords:
            functions.append(remove_arabic_stopwords)

        functions.extend([arabic_hamza_normalize, arabic_tah_normalize])

        super().__init__(*functions, lang=lang, channel=channel, n_jobs=n_jobs)


class EnglishProcessor(Processor):
    def __init__(self, keep_numbers: bool = True,
                 remove_stopwords: bool = False,
                 remove_foreign_chars: bool = True,
                 n_jobs: int = -2):

        self.remove_foreign_chars = remove_foreign_chars
        self.keep_numbers = keep_numbers
        self.remove_stopwords = remove_stopwords

        lang = "en"
        channel = "text"

        if keep_numbers:
            functions = [normalize_english_numbers]
        else:
            functions = [replace_english_numbers]

        if remove_foreign_chars:
            functions.append(keep_english_only)

        if remove_stopwords:
            functions.append(remove_english_stopwords)

        super().__init__(*functions, lang=lang, channel=channel, n_jobs=n_jobs)


class SpacesProcessor(Processor):
    def __init__(self, n_jobs: int = -2):
        lang = "neutral"
        channel = 'text'
        functions = [collapse_spaces, strip_text, normalize_unicode]
        super().__init__(*functions, lang=lang, channel=channel, n_jobs=n_jobs)
