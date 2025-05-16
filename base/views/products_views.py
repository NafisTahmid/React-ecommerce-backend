from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.serializers import ProductSerializer
from base.models import Product, Review
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from base.products import products
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword', '')
    print('query', query);
    if query == None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name__icontains=query)
        page = request.query_params.get("page")
        paginator = Paginator(products,2)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page == None:
            page = 1

        page = int(page)


    serializer = ProductSerializer(products, many=True)
    return Response({"products":serializer.data, "page":page, "pages":paginator.num_pages})

@api_view(['GET'])
def getProduct(request, pk):
   product = Product.objects.get(pk=pk)
   serializer = ProductSerializer(product, many=False)
   return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request,pk):
    selectedProduct = Product.objects.get(pk=pk)
    selectedProduct.delete()
    return Response("Product deleted successfully :D")


@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user =request.user
    product = Product.objects.create(
        user = request.user,
        name = 'Sample name',
        price = 0,
        brand = 'Sample brand',
        countInStock = 0,
        category = 'Sample category',
        description = 'Sample description' 

    )
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    product = Product.objects.get(_id=pk)
    data = request.data
    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']

    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def uploadImage(request):
    data = request.data
    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)
    product.image = request.FILES.get('image')
    product.save()
    return Response('Image was uploaded successfully :D')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    product = Product.objects.get(_id=pk)
    user = request.user
    data = request.data

    # 1. Review already exists
    already_exists = product.review_set.filter(user=user).exists()
    if already_exists:
        content = {'detail': 'Review already exists'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
    # 2. No rating or 0
    elif data['rating'] == 0:
        content = {'detail': 'Please select a rating here'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3. Create new review
    else:
        review = Review.objects.create(
            product = product,
            user = user,
            name = user.first_name,
            rating = data['rating'],
            comment = data['comment']

        )
        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0
        for i in reviews:
            total += i.rating
        product.rating = total / len(reviews)
        product.save()

        return Response('Review added')