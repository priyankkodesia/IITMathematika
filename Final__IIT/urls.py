"""Final_IIT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    # these are the two new imports
    password_change,
    password_change_done,
)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home_teacher/register/$',views.register,name='register'),
    url(r'^registrationsuccess/',views.RegistrationSuccessView.as_view(),name='registrationsuccess'),
    url(r'^editconfirm/',views.EditConfirmView.as_view(),name='editconfirm'),
    url(r'^deleteconfirm/',views.DeleteConfirmView.as_view(),name='deleteconfirm'),
    url(r'^(?P<pk>\d+)/update/$',views.UpdateUserView.as_view(),name='update'),
    url(r'^user_fetch_form/$',views.StudentFetchView.as_view(),name='fetch_form'),    #actual form to get user
    url(r'^student_fetch/',views.student_fetch,name='student_fetch'),    # containing JSON data from DB
    url(r'^(?P<pk>\d+)/delete$',views.DeleteUserView.as_view(),name='delete_user'),
    url(r'^(?P<id>\d+)/delete_event$',views.DeleteEventView,name='delete_event'),


    url(r'^$',TemplateView.as_view(template_name="landing.html")),
    url(r'^login$',views.LoginView.as_view(),name='login'),
    url(r'^logout/$',views.LogoutView.as_view(),name='logout'),
    url(r'^home_teacher/event_add/$',views.add_event,name='add_event'),
    url(r'^home_teacher/',views.teacherHomeView,name='teacher_home'),
    url(r'^home_student/',views.StudentHomeView.as_view(),name='student_home'),


    url(r'^studentdetail/(?P<pk>\d+)/', views.StudentDetailView.as_view(), name='student_detail'),
    url(r'^studentlist/$',views.StudentListView,name='student_list'),
    
    
    ###built in password reset functionality-start
    url(r'^accounts/password/reset/done/$',
        password_reset_done,
        {'template_name': 'registration/password_reset_done.html'},
        name="password_reset_done"),
    # new url definitions
    url(r'^accounts/password/change/$', password_change, {
        'template_name': 'registration/password_change_form.html'},
        name='password_change'),
    url(r'^accounts/password/change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),
    ### end
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

