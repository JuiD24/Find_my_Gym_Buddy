from django.db import models
from django.contrib.auth.models import User as auth_user

# Create your models here.

class groupModel(models.Model):
    groupName = models.CharField(max_length=300)
    groupUsers = models.ManyToManyField(auth_user,related_name='groupUsers')
    groupAdmin = models.ForeignKey(auth_user, on_delete=models.CASCADE) #if i delete user, delete all info entered by that user
    added_on = models.DateTimeField(auto_now_add=True)
    groupImage = models.ImageField(
        max_length = 144,
        upload_to = 'uploads/%Y/%m/%d/',
        null=True
    )

    def __str__(self):
        return str(self.groupName) + " " + str(self.groupAdmin.username)

class requestModel(models.Model):
    group= models.ForeignKey(groupModel, on_delete=models.CASCADE)
    group_Admin = models.ForeignKey(auth_user, on_delete=models.CASCADE, related_name='group_Admin') #if i delete user, delete all info entered by that user
    requested_User =models.ForeignKey(auth_user, on_delete=models.CASCADE, related_name='requested_User')
    is_approved = models.BooleanField(default=False)


    def __str__(self):
        return str(self.group) + " " + str(self.group_Admin.username) + " " + str(self.requested_User.username) + " " + str(self.is_approved)

class activityModel(models.Model):
    group = models.ForeignKey(groupModel, on_delete=models.CASCADE)     
    activity_name = models.CharField(max_length=300)
    number_of_sets = models.CharField(max_length=300)
    addedBy = models.ForeignKey(auth_user, on_delete=models.CASCADE)   
    activity_added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.group) + " " + str(self.addedBy.username) + " " + str(self.activity_name) + " " + str(self.activity_added_on)

class userActivityModel(models.Model):
    activity= models.ForeignKey(activityModel, on_delete=models.CASCADE)   
    user = models.ForeignKey(auth_user, on_delete=models.CASCADE)  
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.activity) + " " + str(self.user.username) + " " + str(self.is_completed)