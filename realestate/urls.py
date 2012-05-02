from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from estatebase.views import EstateTypeView, EstateCreateView, estate_list_view

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'realestate.views.home', name='home'),
    # url(r'^realestate/', include('realestate.foo.urls')),    
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cat/$', EstateTypeView.as_view(), name='estate_list'),
    url (r'^create/(?P<estate_type>\d+)$', view=EstateCreateView.as_view(), name='estate_create'),
    url(r'^estatelist/$',view=estate_list_view),
    url(r'^selectable/', include('selectable.urls')),    
)


       
