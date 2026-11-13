from django.contrib import admin
from .models import Poll, Vote
# Register your models here.
class PollAdmin(admin.ModelAdmin):
    list_display = (
        'question',
        'description',
        'status',
    )

    list_editable = (
        'status',
        'description'
    )

    search_fields = ('question', )
    list_filter = ('status', )

class VoteAdmin(admin.ModelAdmin):
    list_display = (
        'poll',
        'choice',
        'user',
        'created_at'
    )
    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Poll, PollAdmin)
admin.site.register(Vote, VoteAdmin)