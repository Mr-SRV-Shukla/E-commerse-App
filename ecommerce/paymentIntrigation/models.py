from django.db import models

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    number = models.IntegerField(default=0)
    address = models.CharField(max_length=255)  
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=10)  

    def __str__(self):
        return f"Order {self.order_id} - {self.name}"


class OrdersUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="updates",default="")
    update_desc = models.TextField()  
    timestamp = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Update {self.update_id} for Order {self.order.order_id}"
