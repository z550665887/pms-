from django.conf.urls import url
from django.contrib import admin
from work import views as work_views  # @UnresolvedImport
from django.conf.urls import handler404,handler500

handler404="work.views.pagenofound"
handler500="work.views.pageerror"
urlpatterns = [
    url(r'^login', work_views.login),
    url(r'^index', work_views.home,name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^new', work_views.new,name='new'),
    url(r'^change', work_views.change,name='change'),
    url(r'^myApple', work_views.myApple,name='myApple'),
    url(r'^myAssignment', work_views.myAssignment,name='myAssignment'),
    url(r'^myOperated', work_views.myOperated,name='myOperated'),
    #url(r'^search', work_views.search,name='search'),
    url(r'^tablecontrol', work_views.tablecontrol,name='tablecontrol'),
    url(r'^equipment', work_views.equipment,name='equipment'),
    url(r'^create', work_views.create,name='create'),
    url(r'^logout', work_views.logout,name='logout'),
    url(r'^success', work_views.success,name='success'),
    url(r'^detail', work_views.detail,name='detail'),
    url(r'^result', work_views.result,name='result'),
    url(r'^test', work_views.test,name='test'),
    url(r'^tese', work_views.test,name='tese'),
    url(r'^welcome', work_views.welcome,name='welcome'),
    url(r'^tablesuccess', work_views.tablesuccess,name='tablesuccess'),
    ]