from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    AGE_GROUP_CHOICES = [
        ('18-25', '18-25'),
        ('26-35', '26-35'),
        ('36-45', '36-45'),
        ('46+', '46+'),
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    EDUCATION_CHOICES = [
        ('HS', 'High School'),
        ('UG', 'Undergraduate'),
        ('PG', 'Postgraduate'),
        ('DOC', 'Doctorate'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]
    LOCATION_CHOICES = [
        ('U', 'Urban'),
        ('R', 'Rural'),
    ]

    age = models.CharField(max_length=5, choices=AGE_GROUP_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    occupation = models.CharField(max_length=100)
    education = models.CharField(max_length=3, choices=EDUCATION_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    location = models.CharField(max_length=1, choices=LOCATION_CHOICES)

User = get_user_model()

class Question(models.Model):
    text = models.TextField()
    weight = models.FloatField(default=1.0)
    category = models.CharField(max_length=50, blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.display_order}. {self.text[:50]}..."

class ResponseOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=50)
    value = models.IntegerField()
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.question.display_order}.{self.display_order} {self.text}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class AssessmentResult(models.Model):
    STRESS_LEVELS = [
        (0, 'Minimal/None'),
        (1, 'Mild'),
        (2, 'Moderate'),
        (3, 'Moderately Severe'),
        (4, 'Severe')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()
    level = models.IntegerField(choices=STRESS_LEVELS)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_level_display(self):
        return dict(self.STRESS_LEVELS)[self.level]
    
    def get_level_class(self):
        classes = {
            0: 'success',
            1: 'info',
            2: 'warning',
            3: 'orange',
            4: 'danger'
        }
        return classes.get(self.level, 'secondary')
    
    def get_level_color(self):
        colors = {
            0: '#28a745',  # Green
            1: '#17a2b8',  # Teal
            2: '#ffc107',  # Yellow
            3: '#fd7e14',  # Orange
            4: '#dc3545'   # Red
        }
        return colors.get(self.level, '#6c757d')
    
    def get_interpretation(self):
        interpretations = {
            0: "You're doing great! Your stress levels are minimal.",
            1: "You're experiencing mild stress. Consider some self-care activities.",
            2: "You're experiencing moderate stress. You might benefit from support.",
            3: "Your stress levels are moderately severe. Professional help is recommended.",
            4: "You're experiencing severe stress. Please seek professional help immediately."
        }
        return interpretations.get(self.level, "")
    



class Expert(models.Model):
    EXPERT_TYPE_CHOICES = [
        ('PSY', 'Psychiatrist'),
        ('COU', 'Counselor'),
        ('LCSW', 'Clinical Social Worker'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expert_profile')
    expert_type = models.CharField(max_length=50, choices=EXPERT_TYPE_CHOICES)
    bio = models.TextField()
    qualifications = models.TextField()
    location = models.CharField(max_length=100)
    languages = models.CharField(max_length=200)
    experience_years = models.PositiveIntegerField()
    consultation_fee = models.DecimalField(max_digits=6, decimal_places=2)
    availability = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='experts/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_expert_type_display()}"