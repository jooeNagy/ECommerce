from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product, Review
from rest_framework import status
from .serializers import productSerializer
from .filters import ProductsFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg

# Create your views here.


@api_view(['GET'])
def all_products(request):
    # products = Product.objects.all()
    filterSet = ProductsFilter(request.GET, queryset= Product.objects.all().order_by('id'))
    paginator = PageNumberPagination()
    paginator.page_size = 10
    queryset = paginator.paginate_queryset(filterSet.qs, request)
    serializer = productSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def one_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = productSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_product(request):
    data = request.data
    serializer = productSerializer(data = data)
    if serializer.is_valid():
        product = Product.objects.create(**data, user = request.user)
        res = productSerializer(product, many = False)
        return Response(res.data)
    
    else:
        return Response(serializer.errors)
    


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response("You can not Update this Product", status=status.HTTP_403_FORBIDDEN)
    
    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    product.save()
    serializer = productSerializer(product, many=False)
    return Response(serializer.data)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if product.user != request.user:
        return Response("You can not Delete this Product", status=status.HTTP_403_FORBIDDEN)

    product.delete()
    return Response("Product has been deleted successfully!", status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, pk):
    product = get_object_or_404(Product, id=pk)
    user = request.user
    data = request.data
    review = product.reviews.filter(user=user)


    if data['ratings'] <= 0 or data['ratings'] > 5:
        return Response('Select Rating Between 1-5', status = status.HTTP_400_BAD_REQUEST)
    
    elif review.exists():
        new_review = {'ratings': data['ratings'], 'comment': data['comment']}
        review.update(**new_review)

        ratings = product.reviews.aggregate(avg_ratings = Avg('ratings'))
        product.ratings = ratings['avg_ratings']

        product.save()
        return Response('Product Review Updated')
    else:
        Review.objects.create(
            product = product,
            user = user,
            ratings = data['ratings'],
            comment = data['comment']
        )
        ratings = product.reviews.aggregate(avg_ratings = Avg('ratings'))
        product.ratings = ratings['avg_ratings']
        product.save()

        return Response('Product Review Created')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)

    review = product.reviews.filter(user=user)

    if review.exists():
        review.delete()
        ratings = product.reviews.aggregate(avg_ratings = Avg('ratings'))
        product.ratings = ratings['avg_ratings']
        product.save()
        return Response('Product Review Deleted')
    else:
        return Response('Review Not Found!', status=status.HTTP_404_NOT_FOUND)