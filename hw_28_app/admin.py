from django.contrib import admin

from hw_28_app.models import Ad, Categories

from user.models import User, Location

admin.site.register(Ad)
admin.site.register(Categories)
admin.site.register(User)
admin.site.register(Location)
