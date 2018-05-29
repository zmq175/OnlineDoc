from django.contrib import admin

# Register your models here.
from OnlineDocument.models import Tag, Category, Document, Favorite, History

# import those models to admin page
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Document)
admin.site.register(Favorite)
admin.site.register(History)
