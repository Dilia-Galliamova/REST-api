from django.urls import include, path
from .views import *




urlpatterns = [
    path('post/', RecordViewSet.as_view({'post': 'submit_data'})),
    path('get/<int:pk>/', RecordDetailViewSet.as_view({'get': 'get_data_id'})),
    path('get/', RecordDetailViewSet.as_view({'get': 'get_data_email'})),
    path('patch/<int:pk>/', RecordUpdateViewSet.as_view({'patch': 'update_data'}))
    # path('api-auth/', include('rest_framework.urls')),
]