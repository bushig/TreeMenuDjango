from django.contrib import admin

from .models import Menu, MenuItem

class MenuAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        return ['foreign_keys']



# Register your models here.
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem)