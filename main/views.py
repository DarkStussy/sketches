from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.models import FavoritePhoto
from .forms import OrderForm, AddExampleImageForm
from .models import ExampleImage, Service, Order, OrderImage


def home(request):
    example_images = ExampleImage.objects.all()
    paginator = Paginator(example_images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    return render(request, 'main/home.html', {'example_images': images})


def services(request):
    all_services = Service.objects.all()
    return render(request, 'main/services.html', {'services': all_services})


@login_required
def order(request, serv_id=None):
    service = None
    if serv_id:
        service = get_object_or_404(Service, pk=serv_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            order = Order.objects.create(user=request.user, service=cd['service'], description=cd['description'],
                                         email=request.user.email,
                                         first_name=request.user.first_name,
                                         last_name=request.user.last_name,
                                         phone_number=cd['phone_number'])
            files = request.FILES.getlist('file_field')
            for f in files:
                OrderImage.objects.create(order=order, image=f)
            return render(request, 'main/order_success.html')
    form = OrderForm(initial={'service': service})
    return render(request, 'main/make_order.html', {'form': form, 'service': service})


@login_required
@require_POST
def favorite_add(request, img_id):
    example_image = get_object_or_404(ExampleImage, pk=img_id)
    try:
        favorite = FavoritePhoto.objects.get(user=request.user)
    except FavoritePhoto.DoesNotExist:
        favorite = FavoritePhoto(user=request.user)
        favorite.save()
        favorite.image.add(example_image)
    else:
        favorite.image.add(example_image)
    return redirect('accounts:profile')


@login_required
@require_POST
def favorite_delete(request, fv_id, photo_id):
    favorite = get_object_or_404(FavoritePhoto, pk=fv_id)
    image = ExampleImage.objects.get(id=photo_id)
    favorite.image.remove(image)
    return redirect('accounts:profile')


@staff_member_required
def add_example_image(request):
    if request.method == 'POST':
        form = AddExampleImageForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('image_field')
            for i in images:
                ExampleImage.objects.create(image=i)

            return redirect('main:home')
    form = AddExampleImageForm()
    return render(request, 'main/add_example_image.html', {'form': form})
