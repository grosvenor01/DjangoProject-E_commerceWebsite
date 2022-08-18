from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .import views
urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('product/<int:id>',views.product,name='product'),
    path('shopping-cart/',views.shopping_cart,name='shopping_cart'),
    path('add_to_cart/<int:id>',views.add_to_cart,name='add_to_cart'),
    path('remove_shoppingcart_item/<int:id>',views.remove_shoppingcart_item,name='remove_shoppingcart_item'),
    path('wishliste/',views.wishliste,name='wishliste'),
    path('add_to_wishlist/<int:id>',views.add_to_wishlist,name='add_to_wishlist'),
    path('remove_wishlist_item/<int:id>',views.remove_wishlist_item,name='remove_wishlist_item'),
    path('logout/',views.logout,name='logout'),
    path('confirme/',views.confirme,name='confirme'),
    path('search_product/',views.search_product,name='search_product'),
    path('search/<int:id>',views.search,name='search'),
    path('pack/<int:id>',views.packs,name='packs'),
    path('formations/',views.formations,name='formations'),
    path('services/',views.services,name='services'),
    path('add_comment_pack/<int:id>',views.add_comment_pack,name='add_comment_pack'),
    path('add_comment/<int:id>',views.add_comment,name='add_comment'),
    path('confirme_packs/<int:id>',views.confirme_packs,name='confirme_packs'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)