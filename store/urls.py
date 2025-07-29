from django.urls import path,include
from . import views
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='product')
router.register('category',views.CategoryViewSet,basename='category')
products_router=routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('comments',views.CommentViewSet,basename='product-comments')
router.register('cart',views.CartViewSet)

urlpatterns = router.urls+products_router.urls
