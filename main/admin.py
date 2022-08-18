from unicodedata import category
from django.contrib import admin
from .models import command_packs, produit,pub,cart_product,category,wishlist,command,pack,comments,comments_pack,maison
admin.site.register(produit)
admin.site.register(command_packs)
admin.site.register(pub)
admin.site.register(cart_product)
admin.site.register(category)
admin.site.register(wishlist)
admin.site.register(command)
admin.site.register(pack)
admin.site.register(comments)
admin.site.register(comments_pack)
admin.site.register(maison)

# Register your models here.
