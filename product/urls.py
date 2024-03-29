from django.urls import path
from django.views.decorators.cache import cache_page

from blog.views import BlogListView
from product.apps import ProductConfig
from product.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, CategoryListView

app_name = ProductConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),
    path('product_create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/view/', cache_page(60)(ProductDetailView.as_view()), name='product_details'),
    path('product_update/<int:pk>', ProductUpdateView.as_view(), name='product_update'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),

]
