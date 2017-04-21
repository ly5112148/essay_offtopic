# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from models import *
from apps.main.models import Essay


def test(request):
    return render(request, 'teacherPage.html')


# 登陆页面的显示
def login(request):
    return render(request, 'teacher/Login&Register.html')


# 注册事件响应
def register_action(request):
    teacher_id = request.POST.get('teacher_id')
    name = request.POST.get('name')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    if password == confirm_password:
        Teacher.objects.create(teacher_id=teacher_id, name=name, password=password, avatar='')
        return render(request, 'teacher/Login&Register.html', {'result': 'succes'})
    else:
        return render(request, 'teacher/Login&Register.html', {'result': 'fail'})


def main(request):
    user = ''
    query = ''
    if request.session.get('teacher_id'):
        query = Teacher.objects.get(teacher_id=request.session.get('teacher_id'))
        teacher = Teacher.objects.filter(teacher_id=query.teacher_id)
    else:
        Teacher_id = request.POST.get('teacher_id')
        PASSWORD = request.POST.get('password')
        query = Teacher.objects.get(teacher_id=Teacher_id)
        if PASSWORD == query.password:
            request.session['teacher_id'] = Teacher_id
            request.session['name'] = query.name
            # request.session['personico'] = query.avatar
            teacher = Teacher.objects.filter(teacher_id=Teacher_id)
        else:
            return render(request, 'Login&Register.html', {'result': 'error'})
    result = {}
    result['personico'] = query.avatar
    result['name'] = query.name
    trainedTopics_list = TrainedTopics.objects.all()
    return render(request, 'teacher/teacherPage.html', {'result': result, 'trainedTopics_list': trainedTopics_list})


# 发布作文
def essayRelease(request):
    type = request.POST.get('type')
    title = request.POST.get('title')
    description = request.POST.get('description')
    due_time = request.POST.get('due_time')
    Essay.objects.create(title=title, due_time=due_time, description=description, type=type,
                              teacher_id='1')  # request.session.get('teacher_id')
    return render(request, 'teacher/teacherPage.html')


def exit(request):
    del request.session['user_id']
    del request.session['name']
    return render(request, 'teacher/Login&Register.html')
