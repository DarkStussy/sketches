from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.forms import UserRegistrationForm
from accounts.models import FavoritePhoto
from main.models import Order
from main.forms import AddUserAnswer


def login_user(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main:home")
        else:
            error = 'Логин или пароль неверный!'

    return render(request, 'accounts/login_user.html', {'error': error})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def profile(request):
    try:
        favorites = FavoritePhoto.objects.get(user=request.user)
    except FavoritePhoto.DoesNotExist:
        favorites = FavoritePhoto.objects.create(user=request.user)

    paginator = Paginator(favorites.image.all(), 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)

    orders = Order.objects.filter(user=request.user)
    answer_form = AddUserAnswer()
    return render(request, "accounts/profile.html", {"user": request.user, 'favorites': images,
                                                     'favobj': favorites, 'orders': orders, 'answer_form': answer_form})


@login_required
@require_POST
def add_answer(request, order_id):
    answer_form = AddUserAnswer(request.POST)
    order = get_object_or_404(Order, id=order_id)
    if answer_form.is_valid():
        cd = answer_form.cleaned_data
        order.user_answer = cd['text']
        order.save()
    return redirect('accounts:profile')
