from django.contrib import admin
from . models import Registration
from django.utils.html import format_html

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['registration_number', 'id', 'full_name', 'age', 'club_name', 'gender', 'weight_category', 'nationality', 'photo_preview']
    list_display_links = ['registration_number', 'full_name']
    search_fields = ['registration_number', 'full_name', 'club_name', 'nationality']
    list_filter = ['gender', 'weight_category']
    ordering = ['id']
    readonly_fields = ['large_photo', 'id', 'registration_number']

    fieldsets = (
        ('Profile Photo', {
            'fields': ('large_photo', 'photo')
        }),
        ('Registration', {
            'fields': ('registration_number',)
        }),
        ('Personal Information', {
            'fields': ('id', 'full_name', 'age', 'nationality')
        }),
        ('Tournament Details', {
            'fields': ('club_name', 'gender', 'weight_category')
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%; object-fit:cover;" />', 
                obj.photo.url
            )    
        return "No Photo"
    photo_preview.short_description = 'Photo'

    def large_photo(self, obj):
        if obj.photo:
            return format_html(
                '''
                <div style="text-align: center; margin: 10px 0;">
                    <img src="{}" style="
                        width: 200px;
                        height: 200px;
                        border-radius: 50%;
                        object-fit; cover;
                        border: 4px solid #333;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                    "/>
                    <p style="margin-top: 8px; font-weight: bold; font-size: 15px;">
                </div>
                ''',
                obj.photo.url,
                obj.full_name,
                obj.registration_number
            )
        return format_html('<p style="color:gray;">No photo uploaded</p>')
    large_photo.short_description = 'Player Photo'