from typing import List, Union

import yaml

from .processors import (NeutralProcessor, ArabicProcessor,
                         EnglishProcessor, SpacesProcessor)


class TextCleaner:
    def __init__(self, n_jobs: int = -2,
                 remove_stopwords: bool = False,
                 keep_numbers: bool = True,
                 remove_foreign_chars: bool = True):

        self.remove_foreign_chars = remove_foreign_chars
        self.remove_stopwords = remove_stopwords
        self.keep_numbers = keep_numbers
        self.n_jobs = n_jobs

        self.neutral_processor = NeutralProcessor(n_jobs=n_jobs)
        self.spaces_processor = SpacesProcessor(n_jobs=n_jobs)

        self.arabic_processor = ArabicProcessor(n_jobs=n_jobs,
                                                keep_numbers=self.keep_numbers,
                                                remove_stopwords=self.remove_stopwords,
                                                remove_foreign_chars=self.remove_foreign_chars)

        self.english_processor = EnglishProcessor(n_jobs=n_jobs,
                                                  keep_numbers=self.keep_numbers,
                                                  remove_stopwords=self.remove_stopwords,
                                                  remove_foreign_chars=self.remove_foreign_chars)

    def __call__(self, inputs: Union[str, List[str]], lang: str) -> Union[str, List[str]]:
        if lang not in {'ar', 'en', 'neutral'}:
            raise TypeError(f"lang should be either 'ar', 'en' or 'neutral', not {lang}")

        output = self.neutral_processor(inputs)

        if lang == "ar":
            output = self.arabic_processor(output)

        elif lang == "en":
            output = self.english_processor(output)

        else:
            output = self.arabic_processor(output)
            output = self.english_processor(output)

        return self.spaces_processor(output)


def load_cleaner(configs_file: str = r"configs/configs.yaml") -> TextCleaner:
    with open(configs_file, 'r') as f:
        configs = yaml.safe_load(f)['cleaner_configs']

    return TextCleaner(**configs)
