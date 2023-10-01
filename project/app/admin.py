from django.contrib import admin
from .models import UserProfile, Lesson, LessonView, Product, Owner, Access

admin.site.register(UserProfile)
admin.site.register(Lesson)
admin.site.register(LessonView)
admin.site.register(Product)
admin.site.register(Owner)
admin.site.register(Access)

