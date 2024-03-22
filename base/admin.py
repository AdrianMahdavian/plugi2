from django.contrib import admin
from .models import *
from django import forms


class StudyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class QuestionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['course_part_fragment'].initial = CoursePartFragment.objects.get(name='Elektrontransportkedjan') # fill in the name of the CPF to make it more effective

class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_filter = ('course_part_fragment__course_part__course', 'course_part_fragment__course_part', 'course_part_fragment')


    # If you want to search for questions based on specific fields, use list_search:
    search_fields = ('question', 'answer')

class CoursePartAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('course',)

class CoursePartFragmentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('course_part',)

admin.site.register(Course, StudyAdmin)
admin.site.register(CoursePart, CoursePartAdmin)
admin.site.register(CoursePartFragment, CoursePartFragmentAdmin)
admin.site.register(Question, QuestionAdmin)
