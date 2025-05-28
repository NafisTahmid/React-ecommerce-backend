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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect


@api_view(['GET'])
def getProducts(request):
    query = request.query_params.get('keyword', '')
    print(query)
    products = Product.objects.filter(name__icontains=query).order_by('_id')

    page = request.query_params.get('page', 1)
    paginator = Paginator(products, 4)  # 2 items per page

    try:
        page_number = int(page)
        products_page = paginator.page(page_number)
    except (PageNotAnInteger, ValueError):
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    serializer = ProductSerializer(products_page, many=True)
    return Response({
        'products': serializer.data,
        'page': products_page.number,  # Current page number
        'pages': paginator.num_pages,  # Total pages
        'count': paginator.count  # Total items
    })
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

@csrf_exempt
@csrf_protect
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

        return Response({'detail':'Review added'})


@api_view(["GET"])
def topProducts(request):
    products = Product.objects.filter(rating__gte=4).order_by('_id')[0:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)