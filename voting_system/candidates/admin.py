from django.contrib import admin
from .models import Candidate, Category
# Register your models here.
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'director',
        'year',
        'description',
    )
    list_editable = (
        'description',
    )
    search_fileds = ('title',)
    list_filter = ('category',)

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Category)