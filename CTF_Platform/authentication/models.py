from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

# Create your models here.
def validate_phone_number(value):
        if not value.isdigit() or len(value)!=10:
           raise ValidationError("Enter a valid phone number")
        else:
            return value

class AccountManager(BaseUserManager):
    def create_user(self, email, username,password=None):
	    if not email:
		    raise ValueError('Users must have an email address')
	    if not username:
		    raise ValueError('Users must have a username')

	    user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

	    user.set_password(password)
	    user.save(using=self._db)
	    return user

    def create_superuser(self, email, username, password):
	    user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
	    user.is_admin = True
	    user.is_staff = True
	    user.is_superuser = True
	    user.is_active = True
	    user.save(using=self._db)
	    return user

class UserAccount(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email",max_length=60,unique=True)
    username                = models.CharField(max_length=30,unique=True)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=False)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    first_name              = models.CharField(max_length=30)
    last_name               = models.CharField(max_length=30)
    college_name            = models.CharField(max_length=200,blank=False,null=False)

    YEARS=(
        ('ONE','1st year'),
        ('TWO','2nd year'),
        ('THREE','3rd year'),
        ('FOUR','4th year'),

    )
    year = models.CharField(max_length=20,choices=YEARS,blank=False,null=False)

    GENDER=(
        ('M','Male'),
        ('F','Female'),
        ('O','Others'),
    )
    gender = models.CharField(max_length=20,choices=GENDER,blank=False,null=False)

    mobile_no=models.CharField(
        max_length=10,
        blank=False,
        null=False,
        validators=[MinLengthValidator(10),validate_phone_number])

    BRANCH=(
        ('ARCH','Architecture, Planning and Design'),
        ('CERA','Ceramic Engineering and Technology'),
        ('CHEM','Chemical Engineering'),
        ('CIVIL','Civil Engineering'),
        ('CSE','Computer Science and Engineering'),
        ('EEE','Electrical Engineering'),
        ('ECE','Electronics Engineering'),
        ('MECH','Mechanical Engineering'),
        ('META','Metallurgical Engineering'),
        ('MINE','Mining Engineering'),
        ('PHARMA','Pharmaceutical Engineering and Technology'),
        ('MNC','Mathematics and Computing'),
        ('EP','Engineering Physics'),
        ('BIOCHEM','Biochemical Engineering'),
        ('BIOMED','Biomedical Engineering'),

    )
    branch = models.CharField(max_length=100,choices=BRANCH,blank=False,null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects=AccountManager()

    def __str__(self):
        return f'{self.username}'

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
	    return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
	    return True