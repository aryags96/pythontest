from django.db import models

# Create your models here.
from django.db import models
from datetime import timedelta,date
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, phone,role, password=None):
        """
        Creates and saves a User with the given email, role and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            role=role,
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,phone, role, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            role=role,
            phone=phone
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    phone=models.IntegerField()
    options=(("employer","employer"),
             ("job_seeker","job_seeker"))
    role = models.CharField(max_length=100,choices=options,default="faculty")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','role','password']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class CompanyProfile(models.Model):
    company=models.OneToOneField(MyUser,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    logo=models.ImageField(upload_to="image",null=True)

    def __str__(self):
        return self.company_name

class Jobs(models.Model):

    edd = date.today() + timedelta(days=15)
    company=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE)
    post_name=models.CharField(max_length=50)
    experience=models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    posted_date=models.DateField(auto_now_add=True, null=True)
    last_date= models.DateField(default=edd, null=True)

    def __str__(self):
        return self.post_name

class JobSeekerProfile(models.Model):
    user=models.OneToOneField(MyUser,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    profile_pic = models.ImageField(upload_to="image",null=True)
    qualification=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    resume=models.FileField(upload_to="documents",null=True)

    def __str__(self):
        return self.name


class Application(models.Model):
    job=models.ForeignKey(Jobs,on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    options = (('applied', 'applied'), ('intouch', 'intouch'), ('selected', 'selected'),
               ('not selected', 'not selected'))
    application_status = models.CharField(max_length=20, choices=options, default='applied')
    company=models.ForeignKey(CompanyProfile,on_delete=models.CASCADE,null=True)



