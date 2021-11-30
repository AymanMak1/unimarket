from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
#from tinymce.models import HTMLField
from django.dispatch import receiver
from django.db.models.signals import post_save

class Category(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=20)
    is_published = models.BooleanField(verbose_name=_("is_published"), default=True)
    image = models.FileField(verbose_name=_("image"), upload_to="image/cat/")

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.title


class Goods(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=20)
    is_published = models.BooleanField(verbose_name=_("is_published"), default=True)
    is_recommend = models.BooleanField(verbose_name=_("is_recommend"), default=False)
    is_top = models.BooleanField(verbose_name=_("is_top"), default=False)
    is_active = models.BooleanField(verbose_name=_("is_active"), default=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name=_("category")
    )
    price = models.FloatField(verbose_name=_("price"))
    image = models.FileField(verbose_name=_("image"), upload_to="image/goods/")
    text = models.TextField(verbose_name=_("text"))
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ("category", "title")

    def __str__(self):
        return self.title


class Carousel(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=100)
    text = models.CharField(verbose_name=_("text"), max_length=200)
    image = models.FileField(verbose_name=_("image"), upload_to="image/carousel/")

    class Meta:
        verbose_name = _("slide")
        verbose_name_plural = _("slides")

    def __str__(self):
        return self.title

class Profile(models.Model):   
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField()
	facebook = models.TextField()
	phone = models.TextField()

       
	def __str__(self):
         return self.user.username
    
	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()
