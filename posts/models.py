from django.db import models



class Post(models.Model):
    CATEGORY_CHOICES = (
        ('Dj', 'Django'),
        ('R', 'Ruby')
    )

    title = models.CharField(max_length=100)
    custom_id = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=3, blank=True, null=True, choices=CATEGORY_CHOICES)
    publish_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.title