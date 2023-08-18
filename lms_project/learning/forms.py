from .models import Course, Review, Lesson
from django import forms
from django.forms.widgets import Textarea, TextInput
from django.forms.utils import ValidationError


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description', 'start_date',
                  'duration', 'price', 'count_lessons',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content', )


class LessonForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label='Выберите курс',
                                    required=True, label='Курс', help_text='Укажите курс к которому хотите '
                                                                           'добавить урок!')
    preview = forms.CharField(widget=Textarea(
        attrs={'placeholder': 'Опишите содержание урока', 'rows': 20, 'cols': 35, }), label='')

    class Meta:
        model = Lesson
        fields = ('name', 'preview', 'course', )
        labels = {'name': '', 'preview': '', 'course': ''}
        widgets = {'name': TextInput(attrs={'placeholder': 'Введите название урока'}),
                   'preview': Textarea(attrs={
                       'placeholder': 'Опишите содержание урока',
                       'rows': 20,
                       'cols': 35, })
                   }
        help_texts = {'preview': 'Описание не должно быть пустым'}
        error_css_class = 'error_field'
        required_css_class = 'required_field'

    def clean_preview(self):
        preview_data = self.cleaned_data['preview']
        if len(preview_data) > 200:
            raise ValidationError(
                'Слишком длинное описание! Сократите до 200 символов')
