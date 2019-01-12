from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from stream_django.feed_manager import feed_manager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='cover', null=True)
    photo = models.ImageField(verbose_name='Zdjęcie profilowe' ,upload_to='profile', null=True)
    body = models.TextField(verbose_name='O mnie', blank=True, null=True)
    www = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    phonenumber = models.IntegerField(verbose_name='Numer telefonu', blank=True, null=True, help_text='To pole przydaje się w przypadku tworzenia wydarzeń, aby użytkownicy w łatwy sposób mogli się z Tobą skontaktować.')

    def __str__(self):
        return 'Profil użytkownika {}.'.format(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Follow(models.Model):
    user = models.ForeignKey('auth.User', related_name='friends', on_delete=models.CASCADE)
    target = models.ForeignKey('auth.User', related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'target')

def unfollow_feed(sender, instance, **kwargs):
    feed_manager.unfollow_user(instance.user_id, instance.target_id)


def follow_feed(sender, instance, created, **kwargs):
    if created:
        feed_manager.follow_user(instance.user_id, instance.target_id)


post_save.connect(follow_feed, sender=Follow)
post_delete.connect(unfollow_feed, sender=Follow)