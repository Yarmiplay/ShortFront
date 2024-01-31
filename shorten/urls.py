from django.urls import path
from . import views

# Define route strings and corresponding functions
route_data = [
    ("create/", views.homepage),
    ("s/<str:key>/", views.short_redirect),
]

# Create URL patterns
urlpatterns = [
    path(route, view_func)
    for route, view_func in route_data
]

# Duplicate each pattern without trailing slashes
urlpatterns += [
    path(route[:-1], view_func)
    for route, view_func in route_data
]