from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None

# Amount-in-words filter (reusable in templates)
try:
    from ..helpers import amount_to_words
except Exception:
    # fallback import style
    from heart_charity.helpers import amount_to_words

@register.filter(name='amount_in_words')
def amount_in_words_filter(value):
    """Converts numeric amount to words for display in templates."""
    try:
        return amount_to_words(value)
    except Exception:
        return ""

