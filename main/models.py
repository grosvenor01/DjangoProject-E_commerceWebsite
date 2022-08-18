from asyncio.windows_events import NULL
from datetime import date, datetime
from secrets import choice
from tkinter import CASCADE
from tokenize import blank_re
from unicodedata import category
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()
class category(models.Model):
    category_name=models.CharField(max_length=200)
    def __str__(self):
        return self.category_name
class pub(models.Model):
    photo=models.ImageField(upload_to='pub')
    offre=models.IntegerField()
    nom_produit=models.CharField(max_length=250)
    prix=models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return self.nom_produit
class produit(models.Model):
    photo_produit=models.ImageField(upload_to="produits")
    statu=models.CharField(max_length=50,choices=(('Sold','Sold'),('Normal','Normal')))
    category_name=models.ForeignKey("category", on_delete=models.CASCADE)
    nom_produit=models.CharField(max_length=200)
    referance_produit=models.CharField(max_length=250)
    prix=models.DecimalField(max_digits=10,decimal_places=2)
    encien_prix=models.DecimalField(max_digits=10,blank=True,decimal_places=2)
    date_fin_sold=models.DateField(blank=True)
    moyenne=models.IntegerField()
    description=models.TextField()
    dimension_lonegeur=models.IntegerField()
    dimension_largeur=models.IntegerField()
    en_stoke=models.CharField(max_length=50,choices=(('en_stoke','en_stoke'),('out_stock','out_stock')))
    def __str__(self):
        return self.nom_produit
class cart_product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit=models.ForeignKey(produit, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    produit=models.ForeignKey(produit,on_delete=models.CASCADE)
    coupon=models.BooleanField(default=False)
class command(models.Model):
    cart=models.ForeignKey(cart_product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=250)
    email=models.EmailField()
    phone_number=models.CharField(max_length=10,null=False, blank=False, unique=True)
    address=models.CharField(max_length =300)
class pack(models.Model):
    nom_pack=models.CharField(max_length=300)
    photo_principal=models.ImageField(upload_to='pack')
    photo_1=models.ImageField(blank=True,upload_to='secondary_pack')
    photo_2=models.ImageField(blank=True,upload_to='secondary_pack')
    photo_3=models.ImageField(blank=True,upload_to='secondary_pack')
    photo_4=models.ImageField(blank=True,upload_to='secondary_pack')
    prix_pack=models.DecimalField(max_digits=10,decimal_places=2)
    referance_pack=models.CharField(max_length=100)
    description_pack=models.TextField()
    dimension_lonegeur=models.IntegerField()
    dimension_largeur=models.IntegerField()
    moyenne=models.IntegerField(default=5)
    def __str__(self):
        return self.nom_pack
class comments(models.Model):
    produit=models.ForeignKey(produit,on_delete=models.CASCADE,blank=True,null=True)
    username=models.CharField(max_length=200,blank=True)
    comment_text=models.TextField()
    date=models.DateTimeField(default=datetime.now())
    stars=models.IntegerField()
class comments_pack(models.Model):
    pack=models.ForeignKey(pack,on_delete=models.CASCADE,blank=True,null=True)
    username=models.CharField(max_length=200,blank=True)
    comment_text=models.TextField()
    date=models.DateTimeField(default=datetime.now())
    stars=models.IntegerField()
class command_packs(models.Model):
    pack=models.ForeignKey(pack,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=250)
    email=models.EmailField()
    phone_number=models.CharField(max_length=10,null=False, blank=False, unique=True)
    address=models.CharField(max_length =300)
class maison(models.Model):
    nbr_chambre=models.IntegerField()
    dimension_cuisine_longeur=models.DecimalField(max_digits=10,decimal_places=2)
    jardin=models.CharField(max_length =300,choices=(('oui','oui'),('non','non')))
    