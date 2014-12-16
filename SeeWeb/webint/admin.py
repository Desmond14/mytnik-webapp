from django.contrib import admin
from webint.models import UserProfile
from webint.models import RuleStorage

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user','position',)

class RuleStorageAdmin(admin.ModelAdmin):
	list_display = ('instance_name','instance_description','json_file')

	

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(RuleStorage, RuleStorageAdmin)
# Register your models here.
