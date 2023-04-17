from django.shortcuts import render,redirect,HttpResponse # for render, redirect page 
from django.contrib.auth import authenticate,logout,login # provide inbuild method of authenticate,login and logout
from django.contrib.auth.decorators import login_required #login must required
from S_M_S.models import CustomUser # import models here  from appname.models import classname 
from django.contrib.auth.decorators import login_required #login must required don't open page without login


# render base.html page
def BASE(request): 
    return render(request,'base.html')

# render login.html page
def LOGIN(request): 
    return render(request,'login.html')    

#login page (backend)
def doLogin(request):
    if request.method=="POST": # take data from login.html page
    # authenticate get all data of user page (S_M_S constomuser data chake in DB Browser)
        user = authenticate(username=request.POST.get('email'), # get username (email) from login.html
                                                  password=request.POST.get('password'),) # get password (password) from login.html
    
    if user!=None: #login page empty  direct go to else part
        login(request,user) #  for login when user is correct then  login successfully  and go to the next page
        user_type = user.user_type # user take user_type of user
        if user_type == '1':
            return redirect ('hod_home')
        elif user_type == '2':
            return redirect('staff_home')
        elif user_type == '3':
            return redirect('student_home')
        else:
            context = {'message':'Invalid User name and Password'} # messages for invalid name and password 
            return render(request, 'login.html', context)  # and send login.html
    else:
        context = {'message':'Invalid User Name and Password'}  # messages for invalid name and password 
        return render(request, 'login.html', context)  # and send login.html      

def doLogout(request):
    logout(request) #  for logout 
    return redirect('login') # redirect for show same page (url - login - login.html - dologin - render login.html page) 

@login_required(login_url='/') # when you change password then go to the login.html page
def PROFILE(request):
    # take all info of 1 user using id(unique) (CustomUser.objects.get(id=request.user.id)) in user
    user = CustomUser.objects.get(id=request.user.id) #take id from customuser (database) id take because id is unique so for profile change id is important
    context={                                         #id=request.user.id comes from user(dologin)
        "user":user, # create dictionary
    }
    return render (request,'profile.html',context) # dictionary send to the profile.html 

@login_required(login_url='/') # when you change password then go to the login.html page
def PROFILEUPDATE (request):
    if request.method=="POST":# take data from profile.html page
        profile_pic=request.FILES.get('profile_pic')# get data from profile.html # use files not post for files
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        #email=request.POST.get('email') # don't change this
        #username=request.POST.get('username') # don't change this
        password=request.POST.get('password')
       
        if not(first_name.isalpha() and last_name.isalpha()):
            request.session['message'] = "Check First_Name or Last_name"
        else:    
            try:
                customuser=CustomUser.objects.get(id=request.user.id)#take id from customuser (database) id take because id is unique so for profile change id is important
                customuser.first_name= first_name # give data to data base
                customuser.last_name= last_name
                
                if password != None and password != "":
                    customuser.set_password(password)#if you want change password then use this line othewise skip
                if profile_pic != None and profile_pic != "":
                    customuser.profile_pic = profile_pic #if you want change profile_pic then use this line othewise skip    
                customuser.save()    # sava data in data base
                request.session['message'] = "Your profile updated successfully!" # send massage on profile.html page with redirect 
                return redirect('profile')
            except:
            
                request.session['message'] = "Failed to update profile!" # send massage on profile.html with redirect page
                return redirect('profile')         
    return render (request,'profile.html') 
