from django.contrib.auth.models import User
from django.db import models


class Owner(models.Model):
    name = models.CharField(max_length=64, verbose_name="Владелец", unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"


class UserProfile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    product_access = models.ManyToManyField("Product", through="Access")

    def __str__(self):
        return f"{self.name.username}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователя"


class Product(models.Model):
    title = models.CharField(max_length=256, verbose_name="Название продукта", unique=True)
    owner = models.ForeignKey(to="Owner", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Lesson(models.Model):
    title = models.CharField(max_length=128, verbose_name="Название урока")
    description = models.TextField(verbose_name="описание урока")
    video_link = models.URLField(verbose_name="Ссылка на видеофайл")
    video_duration = models.DurationField(verbose_name="Размер видео")
    product = models.ManyToManyField("Product")
    watch = models.ManyToManyField("UserProfile", through="LessonView")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Access(models.Model):
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    is_granted = models.BooleanField(default=False)

    def __str__(self):
        return f"Доступ к продукту {self.product} для {self.user}"

    class Meta:
        verbose_name = "Доступ"
        verbose_name_plural = "Доступ"


class LessonView(models.Model):
    user = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    lesson = models.ForeignKey("Lesson", on_delete=models.CASCADE)
    watching_duration = models.DurationField(default=0, verbose_name="Длительность просмотра")
    watched_at = models.DateTimeField(auto_now_add=True)
    is_watched = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"Урок {self.lesson} просмотрен {self.user}"

    def save(self, *args, **kwargs):
        if self.watching_duration >= self.lesson.video_duration * 0.8:
            self.is_watched = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Просмотр"
        verbose_name_plural = "Просмотры"
