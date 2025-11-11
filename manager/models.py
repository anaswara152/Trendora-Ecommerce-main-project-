from django.db import models

# Create your models here.

class category(models.Model):
    cname=models.CharField(max_length=100)

    def __str__(self):
        return self.cname
    


class product(models.Model):
    name=models.CharField(max_length=20)
    size=models.CharField(max_length=20) 
    fabric=models.CharField(max_length=20)
    description=models.TextField()
    listprice=models.FloatField()   
    price=models.FloatField()
    price50=models.FloatField()
    price100=models.FloatField()
    categoryid=models.ForeignKey(category,on_delete=models.CASCADE)
    image=models.FileField(upload_to='media')
    def __str__(self):
        return self.name
