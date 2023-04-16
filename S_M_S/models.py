from django.db import models
from django.contrib.auth.models import AbstractUser # Abstract built-in process used for user creation whose backend working is hidden

# Create your models here.

class CustomUser(AbstractUser):
    USER = (
        (1,'HOD'),
        (2,'STAFF'),
        (3,'STUDENT'),
    )
    
    user_type = models.CharField(choices=USER, max_length=50, default=1) # user choices (HOD,Staff,Student)
    profile_pic = models.ImageField(upload_to='media/profile_pic')



class Course(models.Model):
    name=models.CharField(max_length=100)    
    created_at=models.DateTimeField(auto_now_add=True) # Automaticaly store the date of creation  when you save a data
    updated_at=models.DateTimeField(auto_now=True)  # Automaticaly store the date of creation  when you save a data

    def __str__(self):# in Data base show same name otherwise show (Course object(1))
        return self.name
    

class Session_Year(models.Model):  
    session_start =models.CharField(max_length=100)
    session_end =models.CharField(max_length=100)

    def __str__(self):
        return self.session_start + " to " + self.session_end # in Data base show same date(01/01/2019 to 31/11/2020) otherwise show (Session_Year object (1))
    


class Student(models.Model):  
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)# admin get all customuser field like user_type, profile_pic, first_name,last_name,email,username etc.(using OneToOneField) 
    address=models.TextField()
    gender=models.CharField(max_length=100)
    course_id=models.ForeignKey(Course,on_delete=models.DO_NOTHING)# Course madhun jo course pahije tyacha id store karto (foreignkey use karun)
    session_year_id=models.ForeignKey(Session_Year,on_delete=models.DO_NOTHING )# Session_Year madhun jo Session_Year pahije tyacha id store karto (foreignkey use karun)
    created_at=models.DateTimeField(auto_now_add=True)  # Automaticaly store the date of creation  when you save a data
    updated_at=models.DateTimeField(auto_now=True)  # Automaticaly store the date of creation  when you save a data
    # database key(ForeignKey,etc) data types(CharField,etc1)

    def __str__(self):
        return self.admin.first_name + " " + self.admin.last_name # in Data base show same name otherwise show (Course object(1))
    


class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()   
    gender = models.CharField( max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.username



class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)      
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

  
class Staff_Notification(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status =models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.staff_id.admin.first_name



class Student_Notification(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status =models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.student_id.admin.first_name        
    

class Staff_leave(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)    
    date = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.staff_id.admin.first_name + " " + self.staff_id.admin.last_name


class Student_leave(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)    
    date = models.CharField(max_length=100)
    message = models.TextField()
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.student_id.admin.first_name + " " + self.student_id.admin.last_name        
    

class Staff_Feedback(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)    
    feedback = models.TextField()
    feedback_reply = models.TextField()
    status=models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.staff_id.admin.first_name + " " + self.staff_id.admin.last_name



class Student_Feedback(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)    
    feedback = models.TextField()
    feedback_reply = models.TextField()
    status=models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name + " " + self.student_id.admin.last_name        



class Attendance(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(Session_Year, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject_id.name
    

class Attendance_Report(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_id.admin.first_name
    
    
class Student_Result(models.Model):
    student_id =models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment_mark = models.IntegerField()
    exam_Mark =models.IntegerField()
    created_at=models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name
    