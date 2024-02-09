from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField(null=True)
    done = models.BooleanField(default=False)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
#for user model later
# # Assuming you have a User model with a timezone field
# from django.utils import timezone

# class User(models.Model):
#     username = models.CharField(max_length=100)
#     timezone = models.CharField(max_length=50)  # Store timezone as a string
    
#     def get_local_time(self):
#         # Get the user's timezone
#         user_timezone = timezone.pytz.timezone(self.timezone)
        
#         # Convert UTC time to the user's timezone
#         utc_time = timezone.now()
#         local_time = utc_time.astimezone(user_timezone)
#         return local_time