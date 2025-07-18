from django.urls import path,include
from . import views
from rest_framework.routers import SimpleRouter

router=SimpleRouter()
router.register('products',views.ProductViewSet,basename='product')
router.register('category',views.CategoryViewSet,basename='category')

urlpatterns = [
    path('',include(router.urls))
]
