from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.http import HttpResponse, JsonResponse
from datetime import datetime, time, timezone
from . import forms
from . import models
from django.contrib.auth.models import User as auth_user


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    context = {
        "title": "Gym Buddy",
        "body" : "Find my Gym Buddy"
    }
    return render(request,"index.html", context=context)

def showGroups(request):
    context = {
        "body" : "Your Groups",
    }
    return render(request,"showGroups.html", context=context)

def createGroup(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    if request.method == "POST":
        form = forms.GroupForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            form.saveGroup(request)
            return redirect("/")
    else:
        form = forms.GroupForm()
    context = {
        "title": "Create Group Page",
        "form" : form
    }    
    return render(request,"createGroup.html", context=context)    

def joinGroup(request):
    if not request.user.is_authenticated:
        return redirect ("/login/")
    context = {
        "body" : "Join Groups",
    }
    return render(request,"joinGroups.html", context=context)

def joinGroupList(request):
    objects = models.groupModel.objects.exclude(groupUsers= (request.user))
    groupDict = {}
    groupDict["groupLists"] = []
    for groupObj in objects:
        reqObj = models.requestModel.objects.filter(group = groupObj).filter(requested_User = request.user)
        if len(reqObj) == 0:
            temp_group = {}
            temp_group["groupName"] = groupObj.groupName
            temp_group["groupID"] = groupObj.id
            temp_group["groupAdmin"] = groupObj.groupAdmin.username
            temp_group["groupAdminID"] = groupObj.groupAdmin.id 
            time_diff = datetime.now(timezone.utc) - groupObj.added_on
            time_diff_s = time_diff.total_seconds()
            if time_diff_s < 60:
                temp_group["date"] = str(int(time_diff_s)) + " seconds ago"
            else:
                time_diff_m = divmod(time_diff_s,60)[0]
                if time_diff_m < 60:
                    temp_group["date"] = str(int(time_diff_m)) + " minutes ago"
                else:
                    time_diff_h = divmod(time_diff_m,60)[0]
                    if time_diff_h < 24:
                        temp_group["date"] = str(int(time_diff_h)) + " hours ago"
                    else:    
                        temp_group["date"] = groupObj.added_on.strftime("%Y-%m-%d")    
            groupDict["groupLists"] += [temp_group]
    return JsonResponse(groupDict) 

def groupList_view(request):
    # console.log("") p2.article_set.all()  models.groupModel.objects.all()--> groupModel.objects.filter(groupUsers = request.user)
    # print("list 1", models.groupModel.objects.filter(groupUsers = request.user))
    print("group list view ",(request.user).groupmodel_set.all())  #-----------------------------------------
    groupobjects = models.groupModel.objects.filter(groupUsers = request.user)
    groupDict = {}
    groupDict["groupLists"] = []
    for groupObj in groupobjects:
        temp_group = {}
        temp_group["groupName"] = groupObj.groupName
        temp_group["groupAdmin"] = groupObj.groupAdmin.username
        time_diff = datetime.now(timezone.utc) - groupObj.added_on
        time_diff_s = time_diff.total_seconds()
        if time_diff_s < 60:
            temp_group["date"] = str(int(time_diff_s)) + " seconds ago"
        else:
            time_diff_m = divmod(time_diff_s,60)[0]
            if time_diff_m < 60:
                temp_group["date"] = str(int(time_diff_m)) + " minutes ago"
            else:
                time_diff_h = divmod(time_diff_m,60)[0]
                if time_diff_h < 24:
                    temp_group["date"] = str(int(time_diff_h)) + " hours ago"
                else:    
                    temp_group["date"] = groupObj.added_on.strftime("%Y-%m-%d")    
        groupDict["groupLists"] += [temp_group]
        print("group dic", groupDict)
    return JsonResponse(groupDict) 

def request_view(request, group_ID, groupAdmin_ID):
    print(group_ID ,groupAdmin_ID, request.user.id)
    groupModel_instance = models.groupModel.objects.get(id=group_ID)
    user_instance = models.auth_user.objects.get(id =groupAdmin_ID)
    request_instance = models.requestModel()
    request_instance.group = groupModel_instance
    request_instance.group_Admin = user_instance
    request_instance.requested_User = request.user
    request_instance.save()
    context = {
        "body" : "Join Groups",
    }
    return render(request,"joinGroups.html", context=context)

def request_page_view(request):
    request_from_other_users = models.requestModel.objects.filter(group_Admin=request.user)
    request_to_join_other_groups = models.requestModel.objects.filter(requested_User = request.user)
    print(request_from_other_users)
    print(request_to_join_other_groups)
    context = {
        "body":"Your Request",
        "request_from_other_users_list": request_from_other_users,
        "request_to_join_other_groups" : request_to_join_other_groups,
    }
    return render(request,"showRequest.html", context=context) 

def acceptRequest_view(request, req_ID):
    request_obj = models.requestModel.objects.get(id = req_ID)
    request_obj.is_approved = True
    request_obj.group.groupUsers.add(request_obj.requested_User)
    request_obj.save()
    # print("request obj ",request_obj.group)
    return redirect("/requestPage/")
    # group_instance = models.groupModel.objects.filter(id = req_ID)request_obj.group.
    # groupUsers.add(request_obj.requested_User)
    # request_page_view(request)
    #change is_approved = true
    # take group obj...filter n then add requsted user to it group_instance.groupUsers.add(request.user)

def declineRequest_view(request, req_ID):
    request_obj = models.requestModel.objects.get(id = req_ID)
    request_obj.delete()
    return redirect("/requestPage/")
    
def register_view(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.registerUser(request)    #registration form -> registerUser function 
            return redirect("/login/")
    else:    
        form = forms.RegistrationForm()
    context = {
        "title": "CSU Chico Registration Page",
        "form" : form
    }    
    return render(request,"registration/register.html", context=context)

def logout_view(request):
    logout(request)
    return redirect("/login/")