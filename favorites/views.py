from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from .models import Favorite, FavoriteItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.


def _favorite_id(request):
    favorite = request.session.session_key
    if not favorite:
        favorite = request.session.create()
    return favorite


def add_favorite(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        favorite = Favorite.objects.get(favorite_id=_favorite_id(request))
    except Favorite.DoesNotExist:
        favorite = Favorite.objects.create(
            favorite_id = _favorite_id(request)
        )
    favorite.save()

    try:
        favorite_item = FavoriteItem.objects.get(product=product, favorite=favorite)
        #favorite_item.quantity +=1
        favorite_item.save()
    except FavoriteItem.DoesNotExist:
        favorite_item = FavoriteItem.objects.create(
            product = product,
            quantity = 1,
            favorite = favorite,
        )
        favorite_item.save()

    return redirect('favorite')


def remove_favorite_item(request, product_id, quantity=1):
    favorite = Favorite.objects.get(favorite_id=_favorite_id(request))
    product = get_object_or_404(Product, id=product_id)
    favorite_item = FavoriteItem.objects.get(product=product, favorite=favorite, quantity=quantity)
    favorite_item.delete()
    return redirect('favorite')


def favorite(request, total=0, quantity=0, favorite_items=None):
    try:
        #if request.user.is_authenticated:
        #    favorite_items = FavoriteItem.objects.filter(user=request.user, is_active=True)
        #else:
        favorite = Favorite.objects.get(favorite_id=_favorite_id(request))
        favorite_items = FavoriteItem.objects.filter(favorite=favorite, is_active=True)

        for favorite_item in favorite_items:
            total += (favorite_item.product.price * favorite_item.quantity)
            quantity += favorite_item.quantity
    except ObjectDoesNotExist:
        pass #ignora

    context = {
        'total': total,
        'quantity': quantity,
        'favorite_items': favorite_items
    }

    return render(request, 'store/favorite.html', context)

@login_required(login_url='login')
def communicate(request):
    return render(request, 'store/communicate.html')
