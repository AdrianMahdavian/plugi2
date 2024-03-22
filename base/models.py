from django.db import models
from django.template.defaultfilters import slugify  


# Create your models here.
class Course(models.Model): 
    name = models.CharField(max_length=100, null=False)
    slug = models.SlugField(null=False, unique=True)
    #image = models.ImageField(upload_to=course_image_uploader, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class CoursePart(models.Model):
    name = models.CharField(max_length=100, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=True)
    slug = models.SlugField(null=False, unique=True)
    #image = models.ImageField(upload_to=course_part_image_uploader, null=True, blank=True)
    ordering = models.IntegerField(null=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(CoursePart, self).save(*args, **kwargs)

    
    def __str__(self):
        return self.name
    

class CoursePartFragment(models.Model):
    name = name = models.CharField(max_length=100, null=False)
    course_part = models.ForeignKey(CoursePart, on_delete=models.CASCADE, null=False)
    slug = models.SlugField(null=False, unique=True)
    ordering = models.IntegerField(null=False)


    #def save(self, *args, **kwargs):
    #    self.slug = slugify(self.name)
    #    super(CoursePartFragment, self).save(*args, **kwargs)

    def total_question_count(self):
        normal_question_count = Question.objects.filter(course_part_fragment=self).count()
        #student_question_count = StudentQuestion.objects.filter(course_part_fragment=self, student=user).count()
        return normal_question_count 


    def __str__(self):
        return self.name




class Question(models.Model):
    question = models.TextField(null=False)
    answer = models.TextField(null=True, blank=True)
    #image = models.ImageField(upload_to=question_image_uploader, null=True, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    course_part_fragment = models.ForeignKey(CoursePartFragment, on_delete=models.CASCADE, null=False,  related_name='questions')

    def __str__(self):
        return self.question