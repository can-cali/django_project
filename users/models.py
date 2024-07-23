from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self): # __str__ method is used to return a string representation of the object.
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
            # we are resizing photos to 300x300 pixels. to avoid large photos.
            # PIL library is used to resize photos.
            # we are overriding save method to resize photos.
            # we are saving the image to the same path.
            # we are using the super() method to run the save method of the parent class.
            # we are opening the image using the Image class of the PIL library.
