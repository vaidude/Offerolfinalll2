from django.db import models

# Create your models here.
class Register(models.Model):
    name=models.CharField(max_length=50,null=True,blank=True)
    email=models.EmailField(unique=True,null=True,blank=True)
    phone=models.IntegerField(null=True,blank=True)
    gender_choices=(
        ('MALE','male'),
        ('FEMALE','female'),
        ('OTHERS','others')
        
    )
    gender=models.CharField(choices=gender_choices,max_length=10)
    age=models.IntegerField(null=True,blank=True)
    password=models.CharField(max_length=8,null=True,blank=True)
    image=models.ImageField(upload_to='user/',null=True,blank=True)
    def __str__(self):
        return self.name

class shopregister(models.Model):
    shopname=models.CharField(max_length=50,null=True,blank=False)
    shopownername=models.CharField(max_length=50,null=True,blank=False)
    email=models.EmailField(unique=True,null=True,blank=False)
    phone=models.IntegerField(null=True,blank=True)
    storeid=models.CharField(max_length=50,null=True,blank=False,unique=True)
    password=models.CharField(max_length=8,null=True,blank=True)
    image=models.ImageField(upload_to='shop/',null=True,blank=True)
    location=models.CharField(max_length=50,null=True,blank=False)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')
    def __str__(self):
        return self.shopname

class product(models.Model):
    productname=models.CharField(max_length=50,null=True,blank=False)
    productimage=models.ImageField(upload_to='product/',null=True,blank=True) 
    productprice=models.IntegerField(null=True,blank=True)
    offerprice=models.DecimalField(max_digits=100,null=True,blank=True,decimal_places=2) 
    discountvalue=models.IntegerField(null=True,blank=True) 
    stock=models.IntegerField(null=True,blank=True) 
    shopname=models.ForeignKey(shopregister,on_delete=models.CASCADE)

class review(models.Model):
    product = models.ForeignKey('product', on_delete=models.CASCADE)  # Link to product
    productdes = models.CharField(max_length=224)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)

class Wishlist(models.Model):
        user=models.ForeignKey(Register,on_delete=models.CASCADE)
        products=models.ForeignKey(product,on_delete=models.CASCADE)
        
class UploadedImage(models.Model):
    image = models.ImageField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
class NotifyModel(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user} - {self.product}"


class ShopPoster(models.Model):  
    shop = models.ForeignKey(shopregister, on_delete=models.CASCADE, related_name="posters")  
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)  
    expire_date = models.DateField(null=True,blank=True)

    def __str__(self):  
        return f"Poster for {self.shop.shopname}"  
