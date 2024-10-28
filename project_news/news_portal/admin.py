from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('creation_date', 'content_type', 'title', 'preview_text', 'author', 'rating')
    list_filter = ('creation_date', 'content_type', 'author', 'rating')
    search_fields = ('title', 'text')

    def preview_text(self, obj):
        return obj.text[:40] + '...' if len(obj.text) > 40 else obj.text
    preview_text.short_description = 'Preview of Text'  # Указываем заголовок для столбца


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'rating')
    list_filter = ('user', 'rating')
    search_fields = ('user__username',)

    def get_username(self, obj):
        return obj.user.username  # Возвращаем имя пользователя
    get_username.short_description = 'Username'  # Заголовок для столбца



admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
