from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from base.models import Product, Review
from base.serializers import ProductSerializer
from rest_framework import status
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import boto3
from boto3.s3.transfer import TransferConfig
import os

@api_view(['GET'])
def getProducts(request):
    query_params=request.query_params

    keyword = request.query_params.get("keyword")
    if keyword==None:
        keyword=" "
    print("query",request.query_params.get("keyword"))
    products=Product.objects.filter(name__icontains=keyword).order_by('-createdAt')
    # We want to paginate filtered results
    print("products",products)
    page=request.query_params.get("page")
    paginator=Paginator(products,4)
    try:
        products=paginator.page(page)
    # when we first visit the page,there is no query set
    except PageNotAnInteger:
        products=paginator.page(1)
    # if user sends high number
    except EmptyPage:
        products=paginator.page(paginator.num_pages)
    # if page==None:
    if not page:
        page=1
    print("page in getProducts",page)
    # page=int(page)
    print("pageee",page)

    # this data has to be serialized before turned back to front end. it worked fine with django, but now we use drf
    # we need to create serializer for every different model
    # many is for serializing multiple object
    serializer=ProductSerializer(products, many=True)
    return Response({'products':serializer.data, 'page':page, 'pages':paginator.num_pages})

@api_view(['GET'])
def getTopProducts(request):
    products=Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer=ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request,pk):
    # product=None
    # for i in products:
    #     if i['_id']==pk:
    #         product=i
    #         break
    product=Product.objects.get(id=pk)
    serializer=ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user=request.user
    print("user in post",user)
    print("request.data",request.data)
    name=request.data['name']
    price=request.data['price']
    brand=request.data['brand']
    countInStock=request.data['countInStock']
    category=request.data['category']
    description=request.data['description']
    image=request.data['image']
    print("image",image)
    product=Product.objects.create(user=user, name=name,
                                   price=price,brand=brand,
                                   countInStock=countInStock,category=category,description=description, image=image)
    product.save()
    serializer=ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request,pk):
    data=request.data
    product=Product.objects.get(id=pk)
    product.name=data['name']
    product.price=data['price']
    product.brand=data['brand']
    product.countInStock=data['countInStock']
    product.category=data['category']
    product.description=data['description']

    product.save()
    serializer=ProductSerializer(product,many=False)
    return Response(serializer.data)

# this is for put request
@api_view(['POST'])
def uploadImage(request):
    data=request.data
    print("request in upload image",data)

    product_id=data['product_id']
    product=Product.objects.get(id=product_id)
    product.image=request.FILES.get('image')
    product.save()
    return Response('Image was uploaded')

@api_view(['POST'])
def upload(request):
    data=request.FILES.get("image")
    GB = 1024 ** 3
    config = TransferConfig(multipart_threshold=5 * GB)


    client=boto3.client("s3",
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                        # s3 does not need region
                        # region_name=os.environ.get(AWS_REGION_NAME),
                        )


    response = client.put_object(Body=data,Bucket="bingology-bucket",Key="testing",ContentType="image/jpeg"

        # {
        #     'Bucket': "bingology-bucket",
        #     'Key': "testing",
        #     'ACL': 'public-read',
        #     # I set it as image/jpeg when cropped the image
        #     'ContentType': "image/jpeg"
        # },
    )
    # response = client.generate_presigned_url(
    #     'put_object',
    #     {
    #         'Bucket': "bingology-bucket",
    #         'Key': "testing",
    #         'ACL': 'public-read',
    # 'ContentType': "image/jpeg"
    # },
    # )
    print("response",response)
    return Response(response)


# @api_view(['DELETE'])
# @permission_classes([IsAdminUser])
# def deleteProduct(request, pk):
#     user = request.user
#     print("userrrrrr",user)
#     product=Product.objects.get(id=pk)
#     print("product", product)
#     product.delete()
#     return Response("Product deleted")

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.delete()
    return Response('Producted Deleted')

@api_view(['POST'])
@permission_classes({IsAuthenticated})
def createProductReview(request,pk):
    user=request.user
    product=Product.objects.get(id=pk)
    data=request.data
    alreadyExists= product.review_set.filter(user=user).exists()
    if alreadyExists:
        content={'details':"Product already reviewed"}
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
    elif data['rating']==0:
        content={'details':"Please select a rating"}
        return Response(content,status=status.HTTP_400_BAD_REQUEST)
    else:
        review=Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )
    reviews=product.review_set.all()
    product.numReviews=len(reviews)
    total=0
    for review in reviews:
        total+=review.rating
    product.rating=total/len(reviews)
    product.save()
    return Response({'detail':"Review successfully added"})