from django.urls import path

from bndes_dataset import views


urlpatterns = [
    path('search/',
         views.BNDESDatasetGetView.as_view(),
         name='search'),
]
