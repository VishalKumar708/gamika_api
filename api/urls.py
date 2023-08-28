from .views import my_api_view
from django.urls import path

from .state_views import *
from .city_views import *
from .area_views import *
from .aarti_views import *
from .literature_views import *
from .business_views import *

urlpatterns = [

    # only show approved cities
    path('GetAllApprovedCity/', GetAllApprovedCity.as_view()),
    # only show unapproved cities
    path('GetAllUnapprovedCity/', GetAllUnapprovedCityLAV.as_view()),
    # get city by cityId
    path('GetCityById/<slug:cityId>/', GetCityById.as_view()),
    # To create new city
    path('CreateNewCity/', CreateNewCity.as_view()),
    # To update city
    path('UpdateCityById/<slug:cityId>/', UpdateCityById.as_view()),
    # get areas by cityId
    path('GetAreaByCityId/<slug:cityId>/', GetAreaByCityId.as_view()),
    # get all business by cityId
    path('GetAllBusinessByCityId/<slug:cityId>/', GetAllBusinessByCityId.as_view()),

    # only show approved states
    path('GetAllApprovedStates/', GetAllApprovedState.as_view()),
    # only show unapproved states
    path('GetAllUnapprovedStates/', GetAllUnapprovedState.as_view()),
    # get state by stateId
    path('GetStateById/<slug:stateId>/', GetStateById.as_view()),
    # get cites by stateId
    path('GetCitiesByStateID/<slug:stateId>/', GetCitiesByStateId.as_view()),
    # create a new state
    path('CreateNewState/', CreateNewState.as_view()),
    # update state by stateId
    path('UpdateStateById/<slug:stateId>/', UpdateStateById.as_view()),


    # Get All approved areas
    path('GetAllApprovedAreas/', GetAllApprovedAreas.as_view()),
    # Get All unapproved areas
    path('GetAllUnapprovedAreas/', GetAllUnapprovedAreas.as_view()),
    # Get area by id
    path('GetAreaById/<slug:areaId>/', GetAreaById.as_view()),
    # Create New Area
    path('CreateNewArea/', CreateNewArea.as_view()),
    # Update city by id
    path('UpdateAreaById/<slug:areaId>/', UpdateAreaById.as_view()),

    # only show approved literatures
    path('GetAllApprovedLiteratures/', GetAllApprovedLiterature.as_view()),
    # only show unapproved literatures
    path('GetAllUnapprovedLiteratures/', GetAllUnapprovedLiteratures.as_view()),
    # Get Literature by id
    path('GetLiteratureById/<slug:literatureId>/', GetLiteratureById.as_view()),
    # Create New Literature
    path('CreateNewLiterature/', CreateNewLiterature.as_view()),
    # Update Literature by id
    path('UpdateLiteratureById/<slug:literatureId>/', UpdateLiteratureById.as_view()),


    # only show approved Aarti
    path('GetAllApprovedAarti/', GetAllApprovedAarti.as_view()),
    # only show unapproved Aarti
    path('GetAllUnapprovedAarti/', GetAllUnapprovedAarti.as_view()),
    # Get Literature by id
    path('GetAartiById/<slug:aartiId>/', GetAartiById.as_view()),
    # Create New Aarti
    path('CreateNewAarti/', CreateNewAarti.as_view()),
    # Update Aarti by id
    path('UpdateAartiById/<slug:aartiId>/', UpdateAartiById.as_view()),

    # Create New Business
    path('GetAllApprovedBusiness/', GetAllApprovedBusiness.as_view()),
    # Get All Unapproved Business
    path('GetAllUnapprovedBusiness/', GetAllUnapprovedBusiness.as_view()),
    # Get All approved Business
    path('CreateNewBusiness/', CreateNewBusiness.as_view()),
    # Get Business by id
    path('GetBusinessById/<slug:businessId>/', GetBusinessById.as_view()),
    # Update Business by id
    path('UpdateBusinessById/<slug:businessId>/', UpdateBusinessById.as_view()),

    path('TestGlobalException/', my_api_view)
    # path('city/', CityCURD.as_view()),
]
