from django.shortcuts import render,redirect # for render, redirect page 
from django.contrib.auth.decorators import login_required #login must required don't open profile page without login
from S_M_S.models import Course, Session_Year,CustomUser,Student,Staff,Subject,Staff_Notification,Staff_leave,Staff_Feedback,Student_Notification,Student_Feedback,Student_leave,Attendance,Attendance_Report # import  Course, Session_Year,CustomUser,Student models here
from django.contrib.sessions.models import Session

@login_required(login_url='/') # don't open profile page (HOD/home.html) without login (url - login - login.html - dologin - render login.html page)
def HOME(request): 
    # count use for how many Students , staff , course , subject
    student_count = Student.objects.all().count() # count Students
    staff_count = Staff.objects.all().count()
    course_count = Course.objects.all().count()
    subject_count = Subject.objects.all().count()
    
    # for how many male and female students
    student_gender_male = Student.objects.filter(gender = "Male").count()
    student_gender_female = Student.objects.filter(gender="Female").count()
    
    # send this data to home.html
    context = {
        'student_count':student_count,
        'staff_count':staff_count,
        'course_count':course_count,
        'subject_count':subject_count,
        'student_gender_male':student_gender_male, 
        'student_gender_female':student_gender_female,
    }
    return render(request,'HOD/home.html',context)

@login_required(login_url='/') # don't open profile page (HOD/add_student.html) without login
def ADD_STUDENT(request):
    course = Course.objects.all()# get all column in Course
    session_year = Session_Year.objects.all()# get all column in Session_Year
    

    if request.method=="POST":# take data from add_student.html
        profile_pic = request.FILES.get('profile_pic')# use files not post for files
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
        
        if not(first_name.isalpha() and last_name.isalpha()):
            request.session['message'] = "Check First_Name or Last_name"
        elif username == "" and password == "":
            request.session['message'] = "username or password failed"
        else:
        
            if CustomUser.objects.filter(email=email).exists():# if database email and add_student.html email are same then
                request.session['message'] = "Email Is Already Taken" # send massage on add_student.html page with redirect 
                return redirect('add_student')
            
            if CustomUser.objects.filter(username=username).exists():# if database username and add_student.html username are same then
                request.session['message'] = "username Is Already Taken" # send massage on add_student.html page with redirect 
                return redirect('add_student')
            
            else:
                # get add_student data in CustomUser and save in CustomUser(blueline=Customuser and white add_student.html)
                # Object Creation
                user=CustomUser(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    profile_pic = profile_pic,
                    user_type=3
                )
                user.set_password(password)
                user.save()# save this data in CustomUser

                course = Course.objects.get(id=course_id)# take course_id in course from (Course model)
                session_year = Session_Year.objects.get(id= session_year_id)# take session_year_id in session_year from (Session_Year model)
                # get add_student data in student and save in student(blueline=Customuser and white add_student.html)
                student = Student(
                    admin=user,# admin get from user(CostomUser)
                    address= address,# get from add_student.html
                    session_year_id=session_year,# get from session_year
                    course_id=course,# get from course
                    gender = gender # get from add_student.html

                )
                student.save()
                request.session['message'] = user.first_name + " " + user.last_name + " are successfully added" # send massage on add_student.html page with redirect 
                return redirect('add_student')
            
    context={
        'course':course,# send add_student.html for (course) dropdown and send value
        'session_year':session_year # send add_student.html for (course) dropdown send value
    }

    return render(request,'HOD/add_student.html',context)    #send context to HOD/add_student.html


@login_required(login_url='/') 
def VIEW_STUDENT(request): 
    student=Student.objects.all() 
    context={
       'student':student, # Send data for take a value in 'HOD/view_student.html'
    }
    return render(request,'HOD/view_student.html',context)

def EDIT_STUDENT(request,id): # this id come from urls('edit_student')  
    student=Student.objects.filter(id=id)# this id show in browser url

    course=Course.objects.all()
    session_year=Session_Year.objects.all()
    context={
        'student':student,
        'course': course,
        'session_year':session_year,
    }
    return render(request,'HOD/edit_student.html',context)



@login_required(login_url='/') 
def UPDATE_STUDENT(request):  
    if request.method=="POST":    
        student_id = request.POST.get('student_id') 
        profile_pic= request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_year_id = request.POST.get('session_year_id')
       
        if not(first_name.isalpha() and last_name.isalpha()):
            request.session['message'] = "Check First_Name or Last_name"
            return redirect('view_student')
        else:
            user=CustomUser.objects.get(id=student_id)# take id from edit_student.html and all info of that id
            
            
            if user.email != email :

                if CustomUser.objects.filter(email=email).exists():# if database email and add_student.html email are same then
                    request.session['message'] = "Email Is Already Taken" # send massage on add_student.html page with redirect 
                    return redirect('view_student')
            
            if user.username != username :
                if CustomUser.objects.filter(username=username).exists():# if database username and add_student.html username are same then
                    request.session['message'] = "username Is Already Taken" # send massage on add_student.html page with redirect 
                    return redirect('view_student')
            if password != None and password != "":
                user.set_password(password)#if you want change password then use this line othewise skip
            if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic #if you want change profile_pic then use this line othewise skip    

            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            student=Student.objects.get(admin=student_id)
            student.address=address
            student.gender=gender

            course=Course.objects.get(id=course_id)# we send course_id in edit_student.html
            student.course_id=course

            session_year=Session_Year.objects.get(id=session_year_id)
            student.session_year_id=session_year
            
            
            student.save()

            request.session['message'] = "Record Are Successfully Updated!" # send massage on view_student.html page with redirect 
            return redirect('view_student')

        
    return render(request,'HOD/edit_student.html')



@login_required(login_url='/') 
def DELETE_STUDENT(request,admin):# (admin = CustomUser id )
    
    student1=Student.objects.get(id=admin)
    user = CustomUser.objects.get(id=student1.admin.id)
    user.delete()
    request.session['message'] = "Record Are Successfully Deleted!"

    return redirect('view_student') 



@login_required(login_url='/') 
def ADD_COURSE(request):
    if request.method=="POST":
        course_name = request.POST.get('course_name')
        if not(course_name.isalpha()):
            request.session['message'] = "Use Alphabets for Course Name"
        else:
            course=Course.objects.all()
            for i in course:
                if i.name == course_name:
                    request.session['message'] = "Course Is Already Taken" # send massage on add_student.html page with redirect 
                    return redirect('add_course')
                    
            course=Course(
                name=course_name, #(name = Course(model) course_name = add_course.html)
            )
            course.save()
            request.session['message'] = "Course Are Successfully Created!"
            return redirect('add_course')
        

    return render(request,'HOD/add_course.html')



@login_required(login_url='/') 
def VIEW_COURSE(request):
    course=Course.objects.all()
    context={
        'course':course,
    }
    return render(request,'HOD/view_course.html',context)



@login_required(login_url='/') 
def EDIT_COURSE(request,id):# id come from urls (edit_course)   
    course=Course.objects.get(id=id) # first id from Course(model) and second id from edit_course.html
    context={
        'course':course
    }
    return render(request,'HOD/edit_course.html',context)



@login_required(login_url='/') 
def UPDATE_COURSE(request):    
    if request.method=='POST':
        name = request.POST.get('name')
        course_id = request.POST.get('course_id')
        courses = Course.objects.all()
        if name.isalpha():
            for i in courses:
                if i.name.lower() == name.lower():
                    request.session['message'] = "Course Is Already Taken" 
                    return redirect('view_course')
            else:
                course.name = name #(course_name= edit_course name=Course (model))
                course.save()
                request.session['message'] = "Course Are Successfully Updated!"
                return redirect('view_course')
        else:
            request.session['message'] = "Course name should be Alphabets only" 
            return redirect('edit_course',course_id)
    return render(request,'HOD/edit_course.html')



@login_required(login_url='/') 
def DELETE_COURSE(request,id):
    course=Course.objects.get(id=id)
    course.delete() # and delete the data from database
    request.session['message'] = "Course Are Successfully Deleted!"
    return redirect('view_course')


@login_required(login_url='/') 
def ADD_STAFF(request):
    if request.method=='POST':
        profile_pic=request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        address=request.POST.get('address')
        gender=request.POST.get('gender')

        if not(first_name.isalpha() and last_name.isalpha()):
            request.session['message'] = "Check First_Name or Last_name"
        elif username == "" and password == "":
            request.session['message'] = "username or password failed"
        else:
            if CustomUser.objects.filter(email=email).exists():
                request.session['message'] = "Email Is Already Taken!"
                return redirect('add_staff')

            if CustomUser.objects.filter(username=username).exists():
                request.session['message'] = "Username Is Already Taken!"
                return redirect('add_staff')

            else:
                user= CustomUser(
                    profile_pic=profile_pic,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    user_type=2,
                    )    
                user.set_password(password) # after this process you can use username and password in login.html
                user.save()# save in CustomUser
            
                staff=Staff(
                    admin=user,
                    address=address,
                    gender=gender,
                )
                staff.save() # save all data in staff(model) (database)

                # Save Manava all data

                request.session['message'] = "Staff Are Successfully Added!"
                return redirect('add_staff')


    return render(request,'HOD/add_staff.html')    



@login_required(login_url='/') 
def VIEW_STAFF(request):
    staff=Staff.objects.all()#retrive all Staff data
    
    context={
        'staff':staff # and send to the view_staff
    }
    # send Manava all data use in view_staff.html 
    # in view_staff -edit action - edit_staff  
    return render(request,'HOD/view_staff.html',context)



@login_required(login_url='/') 
def EDIT_STAFF(request,id): # Staff(model) id come from urls (edit_staff)
    staff=Staff.objects.get(id=id)# match Staff(model)(2) id with staff(model all data) (1) id
    context={
        'staff':staff # send same id all data in edit_staff Using value
    }
    # in edit_staff -action - update_staff  
    return render(request,'HOD/edit_staff.html',context)



@login_required(login_url='/') 
def UPDATE_STAFF(request):
    if request.method=="POST":
        # for id = (send all data (view_staff -> create id in  view_staff.html -> use same id edit_staff.html -> update_staff (here)))
        staff_id= request.POST.get('staff_id')# 
        profile_pic=request.FILES.get('profile_pic')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password')
        address=request.POST.get('address')
        gender=request.POST.get('gender')

        user=CustomUser.objects.get(id=staff_id)
        if not(first_name.isalpha() and last_name.isalpha()):
            request.session['message'] = "Check First_Name or Last_name"
            return redirect('view_staff')
        else:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.email = email

            
            if password != None and password != "":
                user.set_password(password)#if you want change password then use this line othewise skip
            if profile_pic != None and profile_pic != "":
                user.profile_pic = profile_pic #if you want change profile_pic then use this line othewise skip    
            user.save()      # save this information in CustomUser (model)  
            
            staff=Staff.objects.get(admin=staff_id)# admin come from Staff(model)-> CustomUser id (in all info of that id) store in admin 
            staff.address = address
            staff.gender = gender
            staff.save() # save admin(CustomUser) + staff information in Staff (model)

            request.session['message'] = "Staff Is Successfully Updated!" # send massage on view_staff.html page with redirect 
            return redirect('edit_staff')

    return render(request,'HOD/edit_staff.html')



@login_required(login_url='/') 
def DELETE_STAFF(request,admin):# admin(CustomUser) id come from urls (delete_staff)
    staff = CustomUser.objects.get( id = admin )
    staff.delete()

    request.session['message'] = "Record Are Successfully Deleted!" # send massage on view_staff.html page with redirect 
    return redirect('view_staff')    



@login_required(login_url='/') 
def ADD_SUBJECT(request):
    course=Course.objects.all()
    staff=Staff.objects.all()
    
    
    if request.method == "POST":
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id') # take only Course(model) id(value) from add_subject
        staff_id = request.POST.get('staff_id')  # take only Staff(model) id(value) from add_subject
        
        if not(subject_name.isalpha() ):
            request.session['message'] = "Use Alphabet for Subject_Name "
            return redirect('add_subject')
        
        else:
        
            course = Course.objects.get(id=course_id) #using this id take all information of that (Course(model)) id and store in course 
            staff=Staff.objects.get(id=staff_id) #using this id take all information of that (Staff(model)) id and store in staff
            
            # and save all information of that id (Course(model)) and id (Staff(model))
            subject=Subject(
                name = subject_name,
                course= course,
                staff= staff,
            )
            subject.save()

            request.session['message'] = "Subjects Are Successfully Updated!" 
            return redirect('add_subject')

    context = {
        'course': course, # send all data in add_subject use for value (id)
        'staff' : staff, # send all data in add_subject use for value (id)
    }

    return render(request,'HOD/add_subject.html',context)



@login_required(login_url='/') 
def VIEW_SUBJECT(request):
    subject=Subject.objects.all()
    context={
        'subject': subject
    }

    return render (request,'HOD/view_subject.html',context)


@login_required(login_url='/') 

def EDIT_SUBJECT(request,id):

    subject = Subject.objects.get( id = id )
    course = Course.objects.all()
    staff = Staff.objects.all() 

    context ={
        'subject':subject,
        'course': course,
        'staff': staff
    }

    return render (request,'HOD/edit_subject.html',context)

@login_required(login_url='/') 
def UPDATE_SUBJECT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')
    
        course = Course.objects.get(id=course_id)
        staff = Staff.objects.get(id=staff_id)

          
        if not(subject_name.isalpha() ):
            request.session['message'] = "Use Alphabet for Subject_Name "
            return redirect('view_subject')
        
        else:

            subject=Subject(
                id = subject_id,
                name = subject_name,
                course = course,
                staff = staff,
            )
            
            subject.save()
            request.session['message'] = "Subjects Are Successfully Updated!" 
            return redirect('view_subject')

    return render(request, 'HOD/edit_subject.html')    

@login_required(login_url='/') 
def DELETE_SUBJECT(request,id):
    subject = Subject.objects.get(id=id)
    subject.delete()

    request.session['message'] = "Subject Are Successfully Deleted!"  
    return redirect('view_subject')    


@login_required(login_url='/') 
def ADD_SESSION(request):
    if request.method == "POST":
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')
    
        session = Session_Year(
            session_start = session_year_start,
            session_end = session_year_end,
        )
        session.save()
        request.session['message'] = "Session Are Successfully Created!"  
        return redirect('add_session') 

    return render (request,'HOD/add_session.html')    

@login_required(login_url='/') 
def VIEW_SESSION(request):
    session = Session_Year.objects.all()
    context={
        'session':session
    }
    return render (request,'HOD/view_session.html',context)

@login_required(login_url='/')     
def EDIT_SESSION(request,id):
    
    session = Session_Year.objects.filter(id = id)
    context = {
        'session': session
    }
    
    return render(request,'HOD/edit_session.html',context)    

@login_required(login_url='/') 
def UPDATE_SESSION(request):
    if request.method == "POST":
        session_id = request.POST.get('session_id')
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            id = session_id,
            session_start =session_year_start,
            session_end =session_year_end,
        )
        session.save()

        request.session['message'] = "Session Are Successfully Updated!" 
        return redirect('view_session')

    return render(request,'HOD/edit_session.html')    

@login_required(login_url='/') 
def DELETE_SESSION(request,id):
    session=Session_Year.objects.get(id = id)
    session.delete()
    request.session['message'] = "Session Are Successfully Deleted!"
    return redirect('view_session')

@login_required(login_url='/') 
def STAFF_SEND_NOTIFICATION(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notification.objects.all().order_by('-id')[0:5]

    context = {
        'staff':staff,
        'see_notification':see_notification,
    }
    return render(request,'HOD/staff_notification.html',context)    

@login_required(login_url='/') 
def SAVE_STAFF_NOTIFICATION(request):
    if request.method == "POST":
        staff_id = request.POST.get('staff_id')
        message = request.POST.get ('message')

        staff = Staff.objects.get(admin=staff_id)

        notification = Staff_Notification(
            staff_id = staff,
            message = message,

        )
        notification.save()
        request.session['message'] = "Notification Are Successfully Send!" 

        return redirect('staff_send_notification')

    
@login_required(login_url='/') 
def STAFF_LEAVE_VIEW(request):    
    staff_leave = Staff_leave.objects.all()
    context = {
        'staff_leave':staff_leave,
    }
    return render(request,'HOD/staff_leave.html',context)

@login_required(login_url='/') 
def STAFF_APPROVE_LEAVE(request,id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')   

@login_required(login_url='/') 
def STAFF_DISAPPROVE_LEAVE(request,id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 2
    leave.save()
    return redirect('staff_leave_view')  


@login_required(login_url='/') 
def STUDENT_LEAVE_VIEW(request):
    student_leave = Student_leave.objects.all()
    context={
        'student_leave':student_leave,
    }
    return render(request,'HOD/student_leave.html',context)  


@login_required(login_url='/') 
def STUDENT_APPROVE_LEAVE(request,id):
    student_leave = Student_leave.objects.get(id=id)
    student_leave.status = 1
    student_leave.save()
    return redirect('student_leave_view')


@login_required(login_url='/') 
def STUDENT_DISAPPROVE_LEAVE(request,id):
    student_leave = Student_leave.objects.get(id=id)
    student_leave.status = 2
    student_leave.save(

        
    )
    return redirect('student_leave_view')



@login_required(login_url='/') 
def STAFF_FEEDBACK(request):
    feedback = Staff_Feedback.objects.all()  
    feedback_history = Staff_Feedback.objects.all().order_by('-id')[0:5]
    context={
            'feedback':feedback,
            'feedback_history':feedback_history,
    }
    return render(request,'HOD/staff_feedback.html',context)

@login_required(login_url='/')
def STAFF_FEEDBACK_SAVE(request):   
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        feedback = Staff_Feedback.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()


        return redirect('staff_feedback_reply') 

@login_required(login_url='/')
def STUDENT_FEEDBACK(request):
    feedback = Student_Feedback.objects.all() 
    feedback_history = Student_Feedback.objects.all().order_by('-id')[0:5] 
    context={
            'feedback':feedback,
            'feedback_history':feedback_history,
    }
    return render(request,'HOD/student_feedback.html',context)   

@login_required(login_url='/')
def STUDENT_FEEDBACK_SAVE(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')
        
        feedback = Student_Feedback.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.status = 1
        feedback.save()

        return redirect('student_feedback_reply')

@login_required(login_url='/')
def STUDENT_SEND_NOTIFICATION(request):
    student = Student.objects.all()
    notification = Student_Notification.objects.all()
    context ={
        'student':student,
        'notification':notification,
    }
    return render(request,'HOD/student_notification.html',context)        

@login_required(login_url='/')
def SAVE_STUDENT_NOTIFICATION(request): 
       
    if request.method == 'POST':
        message = request.POST.get('message')
        student_id = request.POST.get('student_id')
        
        student = Student.objects.get(admin =student_id)
       
        stud_notification = Student_Notification(
            student_id = student,
            message = message,
        )
        
        stud_notification.save()
        request.session['message'] = "Student Notification Are Successfully Send!" 
        return redirect('student_send_notification') 

    return render(request,'HOD/student_notification.html')        



def VIEW_ATTENDANCE(request):
    
    subject=Subject.objects.all()
    session_year=Session_Year.objects.all()
    action= request.GET.get('action')
    get_subject=None
    get_session_year=None
    attendance_date = None
    attendance_report=None


    if action is not None:
        if request.method== "POST":
            
            subject_id = request.POST.get('subject_id')
            session_year_id =  request.POST.get('session_year_id')
            attendance_date = request.POST.get('attendance_date')
            
            get_subject = Subject.objects.get(id=subject_id)
            get_session_year = Session_Year.objects.get(id=session_year_id)
            
            attendance =Attendance.objects.filter(subject_id = get_subject,attendance_date=attendance_date)
            for i in attendance:
                attendance_id = i.id
                attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)
            
           
    context = {
        'subject':subject,
        'session_year':session_year,
        'action':action,
        'get_subject':get_subject,
        'get_session_year':get_session_year,
        'attendance_date' :attendance_date,
        'attendance_report':attendance_report,
    }
    return render(request,'HOD/view_attendance.html',context)