from django_select2 import forms as s2forms

class CityWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains"
    ]
    
class CategoryWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains"
    ]
    
    def build_attrs(self, base_attrs, extra_attrs=None):
        """Add select2's tag attributes."""
        default_attrs = {
            "data-minimum-input-length": 0,
            "data-tags": "true",
            "data-token-separators": '[",", " "]',
        }
        default_attrs.update(base_attrs)
        return super().build_attrs(default_attrs, extra_attrs=extra_attrs)