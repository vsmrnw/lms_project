from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import Signal
from django.template.loader import render_to_string

from .models import Course, Lesson

set_views = Signal()
course_enroll = Signal()


def check_quantity(sender, instance, **kwargs):
    error = None
    actual_count = sender.objects.filter(course=instance.course).count()
    set_count = Course.objects.filter(id=instance.course.id) \
        .values('count_lessons')[0]['count_lessons']

    if actual_count >= set_count:
        error = (f'Количество уроков ограничено! Ранее вы указывали что курс '
                 f'будет содержать {set_count} уроков')

    return error


def incr_views(sender, **kwargs):
    session = kwargs['session']
    views = session.setdefault('views', {})
    course_id = str(kwargs['id'])
    count = views.get(course_id, 0)
    views[course_id] = count + 1
    session['views'] = views
    session.modified = True


def send_enroll_email(**kwargs):
    template_name = 'email/enroll_email.html'
    course = Course.objects.get(id=kwargs['course_id'])
    context = {
        'course': course,
        'message': f'Вы были успешно записаны на курс {course.title}.'
                   f'Первый урок будет доступен уже {course.start_date}'
    }
    send_mail(subject='Запись на курс | Платформа Edushka',
              message='',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[kwargs['request'].user.email],
              html_message=render_to_string(template_name, context, kwargs[
                  'request']),
              fail_silently=False)


pre_save.connect(check_quantity, sender=Lesson)
set_views.connect(incr_views)
course_enroll.connect(send_enroll_email)
