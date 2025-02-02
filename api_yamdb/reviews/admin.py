from django.contrib import admin

from reviews.models import Title, Category, Genre, Review, Comment


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'get_genres')
    list_filter = ('year', 'category', 'genre')
    search_fields = ('name',)

    def get_genres(self, obj):
        return ", ".join(obj.genre.values_list("name", flat=True))

    get_genres.short_description = "Жанры"



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'score', 'pub_date')
    list_filter = ('score', 'pub_date')
    search_fields = ('author__username', 'title__name')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'text', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('author__username', 'review__title__name')
