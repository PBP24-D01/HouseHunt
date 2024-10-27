from django.db import models
from HouseHuntAuth.models import CustomUser,Seller
import uuid

class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='comments')
    star = models.IntegerField(default=0)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='comments', null=True)
    name = models.CharField(max_length=150,default='Anonymous')
    body = models.CharField(max_length=400) 
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)
        
        
class Reply(models.Model):
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', null=True)
    name = models.CharField(max_length=150,default='Anonymous')
    body = models.CharField(max_length=400) 
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)
    
