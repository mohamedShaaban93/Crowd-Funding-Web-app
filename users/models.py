from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    facebook =  models.URLField(null=True, blank=True)
    country = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^01[5|1|2|0][0-9]{8}$',
                                 message="Phone number must be entered in the format: '010|012|015|011'. Up to 11 digits allowed.")
    phone = models.CharField(max_length=11, validators=[phone_regex ],
                             null=True, blank=True)
    image = models.ImageField(
        upload_to='pic_folder/user/',
        default='pic_folder/None/no-img.jpg')
    email_confirmed = models.BooleanField(default=False)
    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Profile.objects.get(id=self.id)
        except Profile.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.image and self.image and obj.image != self.image:
            # delete the old image file from the storage in favor of the new file
            obj.image.delete()

    def delete(self, *args, **kwargs):
        # object is being removed from db, remove the file from storage first
        self.image.delete()
        return super(Profile, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Profile, self).save(*args, **kwargs)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

