from django.contrib import admin
from .models import *

admin.site.register(Materials)
admin.site.register(Jobs)
admin.site.register(Materialsjobs)
admin.site.register(Stein)
admin.site.register(Slag)

admin.site.register(Totalbalanceresult)
admin.site.register(Metalleachresult)
admin.site.register(Metalextractiondata)
admin.site.register(Metal)
