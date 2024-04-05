from category.models import Category

class DataMixin:
    
    def get_default_context(self, **kwargs):
        context = kwargs
        if 'title' not in context: 
            context['title'] = 'Goyda'
        context['categories'] =  Category.objects.all()
        return context