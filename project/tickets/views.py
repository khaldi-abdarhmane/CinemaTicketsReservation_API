from ast import Delete
from http.client import NO_CONTENT
from telnetlib import STATUS
from unicodedata import name
from urllib import response
from django.http import JsonResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from tickets.models import Guest, Movie, Reservation
from rest_framework.decorators import api_view
from tickets.serializers import GuestSerializer, MovieSerializer, ReservationSerializer 
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
# Create your views here.

#1 withaout RESTa and query FBV

def no_rest_no_model(request):
    employees=[
        {"firstName":"John", "lastName":"Doe"},
        {"firstName":"Anna", "lastName":"Smith"},
        {"firstName":"Peter", "lastName":"Jones"}
          ]
    return JsonResponse(employees,safe=False)


#2 no_rest_from_avaec model 
def no_rest_from_model(request):
    data=Guest.objects.all()
    response= {
        'guest' : list(data.values('name','mobile'))
    }
    return JsonResponse(response)
def rest_model_id(request):
    data=Guest.objects.all()
    response= {
        'guest' : list(data.values('name','mobile','id'))
    }
    return JsonResponse(response)    

# List == GET
# Create == POST
# pk query == GET 
# Update == PUT
# Delete destroy == DELETE

#3 Function based views 
#3.1 GET POST

@api_view(['GET','POST'])
def FBV_List(request):
    
    #GET
    if  request.method== 'GET' :
        
        
        serialize=GuestSerializer(guest,many=True)
        return Response(serialize.data)

    #POST
    elif request.method == 'POST':
        
         serialize=GuestSerializer(data=request.data)
         if serialize.is_valid():
             serialize.save()
             return Response(serialize.data, status=status.HTTP_201_CREATED)
         return Response(serialize.data,status=status.HTTP_400_BAD_REQUEST)

#3.1 GET PUT DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #Get
    if request.method == 'GET':
       serializer = GuestSerializer(guest)
       return Response(serializer.data)
    elif request.method == 'PUT':
         serializer=GuestSerializer(guest,data=request.data) ####
         if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUE)
    #DELETE
    if request.method == 'DELETE':
         guest.delete()
         return Response(status=status.HTTP_204_NO_CONTENT)

#CBV class based views
#4.1 get post
class CBV_List(APIView):
      def get(self,request):
          guest= Guest.objects.all()
          serialize=GuestSerializer(guest,many=True)
          return Response(serialize.data)
      def post(self,request):
          serialize=GuestSerializer(data=request.data)
          if serialize.is_valid():
             serialize.save()
             return Response(serialize.data, status=status.HTTP_201_CREATED)
          return Response(serialize.data,status=status.HTTP_400_BAD_REQUEST)    
#4.2 get put post          
class CBV_pk(APIView):
      def get_object(self,pk):
          try:
               return Guest.objects.get(pk=pk)
          except Guest.DoesNotExist:
                 raise Http404
      def get(self , request , pk): 
          guest = self.get_object(pk)
          serializer = GuestSerializer(guest)
          return Response(serializer.data) 
      def put(self , request , pk):
          guest = self.get_object(pk)  
          serializer=GuestSerializer(guest,data=request.data) ####
          if serializer.is_valid():
             serializer.save()
             return Response(serializer.data)
          return Response(serializer.errors,status=status.HTTP_400_BAD_REQUE) 
      def delete(self , request , pk):
          guest = self.get_object(pk)
          guest.delete()
          return Response(status=status.HTTP_204_NO_CONTENT)        







#5 Mixins 
#5.1 mixins list

class mixins_list(mixins.ListModelMixin , mixins.CreateModelMixin , generics.GenericAPIView ):
      queryset = Guest.objects.all()
      serializer_class= GuestSerializer
      def get(self , request):
          return self.list(request)
      def post(self , request):
          return self.create(request)  

# 5.2 mixins get put delete           
class mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin , generics.GenericAPIView):
      queryset= Guest.objects.all()
      serializer_class = GuestSerializer
      def get(self , request ,pk):
          return self.retrieve(request)
      def put(self , request ,pk):
          return self.update(request)
      def delete(self , request , pk):
          return self.destroy(request)

# class viewsets_guest(viewsets.ModelViewSet):
#     queryset = Guest.objects.all()
#     serializer_class = GuestSerializer

# class viewsets_movie(viewsets.ModelViewSet):
#     queryset = Movie.objects.all()
#     serializer_class = MovieSerializer
#     filter_backend = [filters.SearchFilter]
#     search_fields = ['movie']

# class viewsets_reservation(viewsets.ModelViewSet):
#     queryset = Reservation.objects.all()
#     serializer_class = Reservation

#viewsets
class viewsets_guest(viewsets.ModelViewSet):
      queryset = Guest.objects.all()
      serializer_class = GuestSerializer
class viewsets_movie(viewsets.ModelViewSet):
      queryset = Movie.objects.all()
      serializer_class = MovieSerializer
class viewsets_reservation(viewsets.ModelViewSet):
      queryset = Reservation.objects.all()
      serializer_class = ReservationSerializer            




# 6 Generics 
#6.1 get and post
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

#6.2 get put and delete 
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]     



#8 Find movie
@api_view(['GET'])
def find_movie(request):
    
    
    movies = Movie.objects.filter(
        hall =request.query_params['hall'],
        # movie = request.query_params['movie'],
    )
    # print("vvv:"+request.query_params.__str__())
    serializer = MovieSerializer(movies, many= True)
    return Response(serializer.data)

#9 create new reservation 
@api_view(['POST'])
def new_reservation(request):

    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()
    return Response(status=status.HTTP_201_CREATED)

