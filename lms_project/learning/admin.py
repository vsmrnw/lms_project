from django.contrib import admin
from .models import Course, Lesson, Tracking, Review

# Register your models here.


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'start_date', 'description', )
    list_display_links = ('title', 'start_date', )
    list_editable = ('description', )
    search_fields = ('^title', )
    list_per_page = 3
    actions_on_top = True
    actions_selection_counter = True
    actions_on_bottom = True


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('course', 'name', 'preview', )
    list_display_links = ('name',)
    search_fields = ('name', )
    list_per_page = 3
    actions_on_top = False
    actions_selection_counter = True
    actions_on_bottom = True


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'user', 'passed', )
    search_fields = ('passed',)
    list_per_page = 3
    actions_on_top = False
    actions_selection_counter = True
    actions_on_bottom = True

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', )
    search_fields = ('content', )
    list_per_page = 100