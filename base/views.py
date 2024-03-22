from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import *
from .forms import *
# Create your views here.


# Standard
def index(request):
    return render(request, 'base/index.html')

def contact(request):
    return render(request, 'base/contact.html')


# Pluggviews
class CourseList(ListView):
    model = Course
    template_name = 'base/courselist.html'
    context_object_name = 'courses'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = [('/', ''), ('/kurser', 'Kurser')]
        return context


class CoursePartList(ListView):
    model = CoursePart
    template_name = 'base/coursepartlist.html'
    context_object_name = 'course_parts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_slug = self.kwargs['course_slug']
        course = get_object_or_404(Course, slug=course_slug)

        context['course'] = course
        context['coursepart'] = CoursePart.objects.filter(course__slug=course_slug)
        context['breadcrumbs'] = [
            ('/', ''),
            ('/kurser', 'Kurser'),
            (f'/kurser/{course_slug}', course.name)
        ]
        return context

    def get_queryset(self):
        course_slug = self.kwargs['course_slug']
        return CoursePart.objects.filter(course__slug=course_slug).order_by('ordering')

    

class CoursePartDetail(DetailView):
    model = CoursePart
    template_name = 'base/coursepartdetail.html'
    context_object_name = 'course_part'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_part = self.object
        context['coursepartfragments'] = CoursePartFragment.objects.filter(course_part=course_part).order_by('ordering')
        context['course'] = course_part.course
        context['breadcrumbs'] = [
            ('/', ''),
            ('/kurser', 'Kurser'),
            (f'/{course_part.course.slug}', course_part.course.name),
            (f'/{course_part.course.slug}/{course_part.slug}', course_part.name)
        ]
        return context

class QuestionListView(ListView):
    model = Question
    template_name = 'base/question_list.html'
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cpf_slug = self.kwargs['cpf_slug']
        course_part_fragment = get_object_or_404(CoursePartFragment, slug=cpf_slug)
        course_part = course_part_fragment.course_part  # Assuming you have a ForeignKey relationship to CoursePart

        context['cpf_id'] = course_part_fragment.id
        context['cpf'] = course_part_fragment
        context['course_part'] = course_part  # Pass course_part to the context
        context['breadcrumbs'] = [
            ('/', ''),
            ('/kurser', 'Kurser'),
            # You might need to adjust this depending on your model relationships
            (f'/{course_part.course.slug}', course_part.course.name),
            (f'/{course_part.course.slug}/{course_part.slug}', course_part.name),
             (f'/{course_part.course.slug}/{course_part.slug}/{cpf_slug}/frågor', course_part_fragment.name)
        ]
        return context

    def get_queryset(self):
       cpf_slug = self.kwargs['cpf_slug']
       return Question.objects.filter(course_part_fragment__slug=cpf_slug).order_by('id')

class UpdateQuestion(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    template_name = 'base/editquestion.html'
    form_class = QuestionForm

    def get_success_url(self):
        # Get the related Course, CoursePart, and CoursePartFragment slugs
        course_slug = self.object.course_part_fragment.course_part.course.slug
        course_part_slug = self.object.course_part_fragment.course_part.slug
        cpf_slug = self.object.course_part_fragment.slug

        return reverse('base:question-list', kwargs={'course_slug': course_slug, 'course_part_slug': course_part_slug, 'cpf_slug': cpf_slug})

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False