from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import *


class PostAdminForm(forms.ModelForm):
    ingredients = forms.CharField(label='Ingredients', widget=CKEditorUploadingWidget(), required=False)
    content = forms.CharField(label='Description', widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Post
        fields = '__all__'


class PostImageAdmin(admin.ModelAdmin):
    pass


class PostImageInline(admin.StackedInline):
    model = PostImage
    max_num = 10
    extra = 0


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True
    list_display = ('id', 'title', 'created_at', 'is_published', 'favorites', 'cooked', 'category', 'views', 'get_photo')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')
    list_editable = ('is_published', 'favorites', 'cooked')
    list_filter = ('is_published', 'category', 'tags')
    inlines = [PostImageInline, ]
    save_on_top = True
    readonly_fields = ('created_at', 'views')
    fields = ('title', 'slug', 'category', 'tags', 'favorites', 'cooked', 'ingredients', 'content', 'main_photo', 'is_published', 'views', 'created_at')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    def get_photo(self, obj):
        if obj.main_photo:
            return mark_safe(f'<img src="{obj.main_photo.url}" width="50">')
        return '-'

    get_photo.short_description = 'Main photo'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title', 'parent')
    list_display = ('title', 'parent')
    list_filter = ('parent',)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)