from .models import Favorite, FavoriteItem
from .views import _favorite_id

def counter(request):
    favorite_count = 0

    try:
        favorite = Favorite.objects.filter(favorite_id=_favorite_id(request))

        if request.user.is_authenticated:
            favorite_items = FavoriteItem.objects.all().filter(user=request.user)
        else:
            favorite_items = FavoriteItem.objects.all().filter(favorite=favorite[:1])

        for favorite_item in favorite_items:
            favorite_count += favorite_item.quantity
    except Favorite.DoesNotExist:
        favorite_count = 0
    return dict(favorite_count=favorite_count)
