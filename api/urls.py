from django.urls import path
from . import views

urlpatterns = [
    # 健康检查
    path('health/', views.HealthCheckView.as_view(), name='health'),

    # 负载均衡相关
    path('slb/list/', views.LoadBalancerListView.as_view(), name='slb-list'),
    path('slb/detail/<str:lb_id>/', views.LoadBalancerDetailView.as_view(), name='slb-detail'),

    # 凭证测试
    path('test-credentials/', views.TestCredentialsView.as_view(), name='test-credentials'),
]