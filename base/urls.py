from django import views
from django.urls import path
from .views import *



app_name = 'base'

urlpatterns = [
    path('', index, name='index'),
    path('kontakt', contact, name='contact'),

    path('kurser', CourseList.as_view(), name='course-list'), # all courses
    path('<slug:course_slug>/', CoursePartList.as_view(), name='course-part-list'),

    path('<slug:course_slug>/<slug:slug>', CoursePartDetail.as_view(), name='course-part-detail'), # one single course-part page,

    path('<slug:course_slug>/<slug:course_part_slug>/<slug:cpf_slug>/frågor/', QuestionListView.as_view(), name='question-list'),

    path('ändra/superuser/fråga/<int:pk>', UpdateQuestion.as_view(), name='edit-question'),

    ]