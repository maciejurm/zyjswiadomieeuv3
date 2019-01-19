from django.db import models
from taggit_selectize.managers import TaggableManager
from django.utils.text import slugify
from django.contrib.auth.models import User
from stream_django.activity import Activity
from django.urls import reverse
from tinymce import HTMLField

class Event(models.Model, Activity):
    title = models.CharField(max_length=255, verbose_name='Tytuł')
    slug = models.SlugField(max_length=255)
    image = models.ImageField(upload_to='event', verbose_name='Tło wydarzenia')
    localization = models.CharField(max_length=255, verbose_name='Lokalizacja', blank=True, null=True)
    body = HTMLField(verbose_name='Szczegóły wydarzenia')
    date_start = models.DateTimeField(verbose_name='Start wydarzenia', help_text='Aby dodać godzinę wydarzenia, wystarczy po rozwinięciu kalendarza kliknąć ikonę zegara.')
    date_end = models.DateTimeField(verbose_name='Koniec wydarzenia', blank=True, null=True, help_text='To pole jest dodatkowe, jeśli nie masz dokładnej daty zakończenia wydarzenia, nie musisz tego podawać.')
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    tags = TaggableManager(verbose_name='Tagi', blank=True)
    button = models.CharField(max_length=50, blank=True, null=True, verbose_name='Przycisk', default='Więcej informacji', help_text='Nazwa przycisku, który przekieruje użytkownika na wybraną przez Ciebie stronę. Na przykład na stronę z zakupem biletu. Więc można dodać w nim na przykład "Kup bilet" lub "Więcej informacji".')
    button_link = models.URLField(max_length=255, blank=True, null=True, verbose_name='Przekierowanie przycisku', help_text='Link przekierowujący użytkownika klikającego w przycisk.')
    active = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date_start',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    @property
    def activity_actor_attr(self):
        return self.author