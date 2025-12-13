from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loan
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

User = get_user_model()

admin.site.site_header = "Administrador MiniLibrary"
admin.site.site_title = "MiniLibrary Panel"
admin.site.index_title = "Bienvenido al panel de MiniLibrary"

@admin.action(description="Marcar prestamos como devueltos")
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned=True)

class LoanInline(admin.TabularInline):
    model = Loan
    extra = 0

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    
class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False
    verbose_name_plural = "Detalle de libro"
    
class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInline]
    list_display = ('username', 'email')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('pages',)
    inlines = [ReviewInline, BookDetailInline]
    list_display = ('title', 'author','pages','publication_date')
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'genres', 'publication_date')
    ordering = ['-publication_date'] # forma descendente
    date_hierarchy = 'publication_date'
    autocomplete_fields = ['author', 'genres']
    
    fieldsets = (
        ("Información general", {
            "fields": ("title", "author", "publication_date", "genres")
        }),
        ("Detalles", {
            "fields":("isbn", "pages"),
            "classes": ("collapse",)   
        })
    )
    
    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_staff
    
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ('loan_date',)
    list_display = ('user', 'book','loan_date', 'is_returned')
    actions = [mark_as_returned]


admin.site.register(BookDetail)
admin.site.register(Review)

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(User, CustomUserAdmin)