from django.contrib import admin
from .models import Project, ProjectMember, Favorite


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('title', 'owner', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'owner__username',
                     'owner__first_name', 'owner__last_name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'owner', 'status')
        }),
        ('Описание', {
            'fields': ('description',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    list_per_page = 25


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    model = ProjectMember
    list_display = ('user', 'project', 'joined_at')
    list_filter = ('joined_at', 'project')
    search_fields = ('user__username', 'project__title')
    ordering = ('-joined_at',)
    readonly_fields = ('joined_at',)

    fieldsets = (
        (None, {
            'fields': ('project', 'user')
        }),
        ('Информация', {
            'fields': ('joined_at',)
        }),
    )

    list_per_page = 25


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = ('user', 'project', 'created_at')
    list_filter = ('created_at', 'project')
    search_fields = ('user__username', 'project__title')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('user', 'project')
        }),
        ('Информация', {
            'fields': ('created_at',)
        }),
    )

    list_per_page = 25