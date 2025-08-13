from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('viewprofile/',views.viewprofile,name='viewprofile'),
    path('editprofile/',views.editprofile,name='editprofile'),
    path('delprofile/<id>/',views.delprofile,name='delprofile'),
    path('shopindex/',views.shopindex,name='shopindex'),
    path('shopregister/',views.shopreg,name='shopregister'),
    path('shoplogin/',views.shoplogin,name='shoplogin'),
    path('shopviewprofile/',views.shopviewprofile,name='shopviewprofile'),
    path('shopeditprofile/',views.shopeditprofile,name='shopeditprofile'),
    path('shopdelprofile/<id>/',views.shopdelprofile,name='shopdelprofile'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('shophome/',views.shophome,name='shophome'),
    path('product_list/',views.product_list,name='product_list'),
    path('home/',views.home,name='home'),
    path('seller_list/',views.seller_list,name='seller_list'),
    path('edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<product_id>/',views.delete_product,name='delete_product'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('adhome/', views.adhome, name='adhome'),
    path('aduser/', views.aduser, name='aduser'),
    path('adshop/', views.adshop, name='adshop'),
    path('review/', views.review, name='review'),

    path('re_product/<int:cid>/', views.re_product, name='re_product'),
    path('adseller_list/<int:shop_id>/', views.adseller_list, name='adseller_list'),
    path('product/<int:product_id>/review/', views.review_view, name='submit_review'),
    path('product/<int:product_id>/reviews/', views.view_reviews, name='view_reviews'),
    path('product/<int:product_id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('random-products/', views.display_random_products, name='random_products'),
    path('adminedit_product/<int:product_id>/', views.adminedit_product, name='adminedit_product'),
    path('productcom/',views.productt,name='product'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('deleteshop/<int:shop_id>/', views.delete_shop, name='delete_shop'),
    path('addelete_product/<int:p_id>/', views.addelete_product, name='addelete_product'),
    path('logout/', views.custom_logout, name='logout'),
    path('camera/', views.camera_view, name='camera'),
    path("generate/", views.generate_image, name="generate_image"),
    

    path('detect/', views.detect_object, name='detect_object'),
    
    path('admin_shops/', views.admin_shops, name="admin_shops"),
    path('approve_shop/<int:shop_id>/', views.approve_shop, name="approve_shop"),
    path('notify-me/<int:product_id>/', views.notify_me, name='notify_me'),
    path('nearby-products/', views.nearby_products, name='nearby_products'),
    path('get-nearby-products-data/', views.get_nearby_products_data, name='get_nearby_products_data'),



    path('add_poster/', views.add_poster, name='add_poster'),
    path('poster_list/', views.poster_list, name='poster_list'),
    path('shop/<int:shop_id>/products/', views.shop_products, name='shop_products'),
    path('shop/posters/', views.shop_posters, name='shop_posters'),
    path('delete_poster/<int:poster_id>/', views.delete_poster, name='delete_poster'),

]
