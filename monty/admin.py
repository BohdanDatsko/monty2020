from django.contrib import admin

from monty.models import Dictionary, Theme, Word, Test


class DictionaryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ThemeAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class WordAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TestAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Dictionary, DictionaryAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Word, WordAdmin)
admin.site.register(Test, TestAdmin)
