import unicodedata


def remove_accents(input_str) -> str:
    """
    Removes accents from the input string using Unicode normalization.
    """
    nfkd_form = unicodedata.normalize('NFD', input_str)
    return ''.join([c for c in nfkd_form if unicodedata.category(c) != 'Mn'])