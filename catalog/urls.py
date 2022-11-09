from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Index),
    re_path(r'^zhenschinam/obuv/\w+|zhenschinam/odezhda/\w+|zhenschinam/aksessuaryi/\w+|muzhchinam/obuv/\w+|muzhchinam/odezhda/\w+|muzhchinam/aksessuaryi/\w+$', views.ActionFilterBySubtypeClothes),
    re_path(r'^zhenschinam/obuv|zhenschinam/odezhda|zhenschinam/aksessuaryi|muzhchinam/obuv|muzhchinam/odezhda|muzhchinam/aksessuaryi$', views.ActionFilterByTypeClothes),
    re_path(r'^zhenschinam|muzhchinam$', views.ActionFilterByGender),
]
