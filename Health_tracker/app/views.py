from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta
from .models import ExerciseRecord, DietRecord

# 登录
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html')

# 注册
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 退出登录
def user_logout(request):
    logout(request)
    return redirect('login')

# 首页
@login_required
def home(request):
    return render(request, 'home.html')

# 运动打卡
@login_required
def exercise(request):
    user = request.user
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())

    if 'del_id' in request.GET:
        get_object_or_404(ExerciseRecord, id=request.GET['del_id'], user=user).delete()
        return redirect('exercise')

    if request.method == 'POST' and not request.POST.get('edit_id'):
        ExerciseRecord.objects.create(
            user=user,
            date=request.POST['date'],
            exercise=request.POST['exercise'],
            duration=request.POST['duration'],
            calories_burned=request.POST['calories']
        )
        return redirect('exercise')

    edit_obj = None
    if 'edit_id' in request.GET:
        edit_obj = get_object_or_404(ExerciseRecord, id=request.GET['edit_id'], user=user)

    if request.method == 'POST' and request.POST.get('edit_id'):
        obj = get_object_or_404(ExerciseRecord, id=request.POST['edit_id'], user=user)
        obj.date = request.POST['date']
        obj.exercise = request.POST['exercise']
        obj.duration = request.POST['duration']
        obj.calories_burned = request.POST['calories']
        obj.save()
        return redirect('exercise')

    all_data = ExerciseRecord.objects.filter(user=user)
    today_data = all_data.filter(date=today)
    week_data = all_data.filter(date__gte=week_start)

    today_time = sum(i.duration for i in today_data)
    today_burn = sum(i.calories_burned for i in today_data)
    week_time = sum(i.duration for i in week_data)
    week_burn = sum(i.calories_burned for i in week_data)

    return render(request, 'exercise.html', {
        'records': all_data,
        'edit': edit_obj,
        'today_time': today_time,
        'today_burn': today_burn,
        'week_time': week_time,
        'week_burn': week_burn
    })

# 饮食记录
@login_required
def diet(request):
    user = request.user
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())

    if 'del_diet_id' in request.GET:
        get_object_or_404(DietRecord, id=request.GET['del_diet_id'], user=user).delete()
        return redirect('diet')

    if request.method == 'POST' and not request.POST.get('diet_edit_id'):
        DietRecord.objects.create(
            user=user,
            date=request.POST['date'],
            meal=request.POST['meal'],
            food=request.POST['food'],
            calories=request.POST['calories']
        )
        return redirect('diet')

    diet_edit = None
    if 'diet_edit_id' in request.GET:
        diet_edit = get_object_or_404(DietRecord, id=request.GET['diet_edit_id'], user=user)

    if request.method == 'POST' and request.POST.get('diet_edit_id'):
        obj = get_object_or_404(DietRecord, id=request.POST['diet_edit_id'], user=user)
        obj.date = request.POST['date']
        obj.meal = request.POST['meal']
        obj.food = request.POST['food']
        obj.calories = request.POST['calories']
        obj.save()
        return redirect('diet')

    all_diet = DietRecord.objects.filter(user=user)
    today_diet = all_diet.filter(date=today)
    week_diet = all_diet.filter(date__gte=week_start)

    today_in = sum(i.calories for i in today_diet)
    week_in = sum(i.calories for i in week_diet)

    return render(request, 'diet.html', {
        'records': all_diet,
        'diet_edit': diet_edit,
        'today_in_cal': today_in,
        'week_in_cal': week_in
    })