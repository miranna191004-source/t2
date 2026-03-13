from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Skill, UserSkill


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'created_at', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {
            'fields': ('first_name', 'last_name', 'email', 'avatar',
                       'bio', 'phone', 'github_url')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions')
        }),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined', 'created_at')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created_at', 'last_login', 'date_joined')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    model = Skill
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at',)


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    model = UserSkill
    list_display = ('user', 'skill', 'created_at')
    list_filter = ('created_at', 'skill')
    search_fields = ('user__username', 'skill__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('user', 'skill')
        }),
        ('Информация', {
            'fields': ('created_at',)
        }),
    )