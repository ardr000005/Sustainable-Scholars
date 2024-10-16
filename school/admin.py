from django.contrib import admin
from django.urls import path
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.contrib import messages
from .models import School

class SchoolAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_verified', 'is_active', 'authorize_button', 'unregister_button']
    search_fields = ['username', 'email']
    list_filter = ['is_verified', 'is_active']

    # Inline buttons to authorize and unregister
    def authorize_button(self, obj):
        if not obj.is_active:
            return mark_safe(f'<a class="button" href="{obj.id}/authorize/">Authorize</a>')
        return "Already Active"
    authorize_button.short_description = "Authorize School"

    def unregister_button(self, obj):
        if obj.is_active:
            return mark_safe(f'<a class="button" href="{obj.id}/deactivate/">Unregister</a>')
        return "Already Inactive"
    unregister_button.short_description = "Unregister School"

    # Bulk actions to authorize and unregister schools
    def activate_school(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected schools have been authorized.")
    activate_school.short_description = "Authorize selected Schools"

    def deactivate_school(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected schools have been unregistered.")
    deactivate_school.short_description = "Unregister selected Schools"

    actions = [activate_school, deactivate_school]

    # Custom admin URLs for handling authorization and deactivation
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:school_id>/authorize/', self.admin_site.admin_view(self.authorize_school)),
            path('<int:school_id>/deactivate/', self.admin_site.admin_view(self.deactivate_school)),
        ]
        return custom_urls + urls

    def authorize_school(self, request, school_id):
        school = School.objects.get(pk=school_id)
        if not school.is_active:
            school.is_active = True
            school.save()
            self.message_user(request, f"{school.username} has been authorized.")
        else:
            self.message_user(request, f"{school.username} is already active.", level=messages.WARNING)
        return redirect('/admin/school/school/')

    def deactivate_school(self, request, school_id):
        school = School.objects.get(pk=school_id)
        if school.is_active:
            school.is_active = False
            school.save()
            self.message_user(request, f"{school.username} has been unregistered.")
        else:
            self.message_user(request, f"{school.username} is already inactive.", level=messages.WARNING)
        return redirect('/admin/school/school/')

admin.site.register(School, SchoolAdmin)
