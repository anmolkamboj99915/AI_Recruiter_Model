from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),  # ✅ FIXED
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
]