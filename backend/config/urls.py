from django.contrib import admin

from django.urls import path

from esgcore.views import (

    ActivityListView,

    BatchListView,

    IssuesListView,

    UploadFileView,

    ApproveActivityView,

    RejectActivityView
)

urlpatterns = [

    path('admin/', admin.site.urls),

    path(
        'api/activities/',
        ActivityListView.as_view()
    ),

    path(
        'api/batches/',
        BatchListView.as_view()
    ),

    path(
        'api/issues/',
        IssuesListView.as_view()
    ),

    path(
        'api/upload/',
        UploadFileView.as_view()
    ),

    path(
        'api/approve/<int:pk>/',
        ApproveActivityView.as_view()
    ),

    path(
        'api/reject/<int:pk>/',
        RejectActivityView.as_view()
    ),
]