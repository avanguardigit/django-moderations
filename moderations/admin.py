from django.contrib import admin
from .models import Report, Motivation, Case, State, Judgement
# Register your models here.

class MotivationAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class StateAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class ReportRelationshipInline(admin.TabularInline):
    fields = ["id", "signaler", "motivation", "create_date"]
    model = Report
    extra = 0
    readonly_fields = ["signaler", "motivation", "create_date"]
    show_change_link = True
    classes = ['collapse']


class CaseAdmin(admin.ModelAdmin):
    inlines = [ReportRelationshipInline]
    list_display = ["id", "__str__", "count_reports"]
    search_fields = ["id", "author__email"]
    fieldsets = (
        ('Target', {'fields': [('target_content_type', 'target_object_id'),'target_object']}),
        ('Status', {'fields': ['state', 'judgement']}),
        ('Info', {'fields': ('create_date', 'last_update')}),
    )

    readonly_fields = ['target_object', 'create_date', 'last_update']



class JudgementAdmin(admin.ModelAdmin):
    list_display = ["id", "reported", "moderator", "action", "end_date"]
    search_fields = ["id", "reported__email"]
    list_filter = ['reported', "moderator", "action", "create_date"]
    fieldsets = (
        ('Target', {'fields': ['moderator', 'reported']}),
        ('Note', {'fields': ['moderator_note']}),
        ('Action', {'fields': ['action', 'end_date']}),
        ('Info', {'fields': ['create_date', 'last_update']}),
    )

    readonly_fields = ['moderator']

    def save_model(self, request, obj, form, change):
        if not obj.moderator:
            obj.moderator = request.user
        obj.save()

admin.site.register(State, StateAdmin)
admin.site.register(Motivation, MotivationAdmin)
admin.site.register(Case, CaseAdmin)
admin.site.register(Judgement, JudgementAdmin)