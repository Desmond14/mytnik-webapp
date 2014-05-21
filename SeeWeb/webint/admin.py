from django.contrib import admin
from webint.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user','position',)

	

admin.site.register(UserProfile, UserProfileAdmin)
# Register your models here.
