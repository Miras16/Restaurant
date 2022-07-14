from django.contrib import admin

# Register your models here.
from .models import Staff,DishMenu,Posts,Comment, Category, Subsection, Profile, Booking

class StaffAdmin(admin.ModelAdmin):
    list_display = ('name','photo', 'address', 'description')
admin.site.register(Staff, StaffAdmin)

class DishMenuAdmin(admin.ModelAdmin):
    list_display = ('img', 'title', 'subtitle', 'price')
admin.site.register(DishMenu)

admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Subsection)
admin.site.register(Profile)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'booking_date', 'booking_time')
admin.site.register(Booking, BookingAdmin)