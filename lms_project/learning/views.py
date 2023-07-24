from django.http import HttpResponse


def create(request):
    return HttpResponse('Страница создания нового курса')


def delete(request, course_id):
    return HttpResponse(f'Страница для удаления {course_id} курса')


def detail(request, course_id):
    return HttpResponse(f'Страница информации о {course_id} курсе')


def enroll(request, course_id):
    return HttpResponse(f'Страница для записи на курс {course_id}')


def index(request):
    return HttpResponse('Страница отображения всех доступных курсов')
