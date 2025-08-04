from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    Product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50, default="")
    subcategory=models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    desc=models.CharField( max_length=50)
    date_field = models.DateField()
# we neet to install Pillow for image field and need to add media url in settings file
    image=models.ImageField( upload_to=None, default="")
    # rating to filter top brands
    rating_field = models.IntegerField(default=0) 

    def __str__(self):
        return self.Product_name