from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path(route= 'about/', view=views.about, name='about'),
    path(route= "contact/", view =views.contact, name ="contact"),
    path(route = "registration/", view = views.registration_request, name ="registration"),
    path(route='login/', view = views.login_request, name ="login" ),
    path(route = 'logout/', view = views.logout_request, name ="logout"),
    path(route='', view=views.get_dealerships, name='index'),
    path(route = 'reviews/', view = views.get_dealer_details_query, name='details-query'),
    path(route = 'reviews/<int:dealerID>/', view = views.get_dealer_details_url, name='details-url'),
    path(route = 'reviews/<int:dealerID>/review', view = views.add_review, name = 'add-review' ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)