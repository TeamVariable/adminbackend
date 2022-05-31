from django.template import Library


register = Library()

# form dictioanry key value initailization 
@register.filter(name="keyinit")
def key_init(dictionary, key) -> str:
    print(f"{dictionary}, {key}")
    return dictionary.get(key)