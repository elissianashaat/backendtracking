import json
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from bson import ObjectId

from authentication.models import User_collection
from authentication.views import get_user

# Create your views here.

from order.models import Order_collection
from order.mongoDb_utils import convert_array_to_serializable, replace_none_with_default


def find_all_order(v):
    orders = Order_collection.find({'userId': v})
    orders_list = list(orders)  # Convert cursor to list
    print(orders_list)
    return orders_list


def find_order_courier(v):
    orders = Order_collection.find({'courierId': v})
    orders_list = list(orders)  # Convert cursor to list
    print(orders_list)
    return orders_list



def get_numbers():
    return list(range(1, 11))


@api_view(['GET'])
def get_all_order(request):
    user_email = get_user(request)
    order = find_all_order(user_email)
    print(order)
    send = convert_array_to_serializable(order)
    return JsonResponse({'status': 'success', 'length:': len(order), 'data': send},
                        status=status.HTTP_200_OK)


@api_view(['GET'])
def get_order_courier(request, variable):
    order = find_order_courier(variable)
    print(order)
    send = convert_array_to_serializable(order)
    return JsonResponse({'status': 'success', 'length:': len(order), 'data': send},
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def create_order(request):
    user_email = get_user(request)
    user = User_collection.find_one({"email": user_email})
    if user:
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        # details = models.CharField(max_length=255)
        # deliveryTime = models.CharField(max_length=255)
        # status = models.CharField(max_length=255)
        # userId = models.CharField(max_length=255)
        pickup = data.get('pickup')
        dropOff = data.get('dropOff')
        details = data.get('details')
        deliveryTime = data.get('deliveryTime')
        order = {
            'pickupLocation': pickup,
            'dropOffLocation': dropOff,
            'details': details,
            'deliveryTime': deliveryTime,
            "userId": user_email,
            'courierId': 'null',
            'status': 'PENDING'
        }
        Order_collection.insert_one(order)

        return JsonResponse({'status': 'success', 'message': 'Order added successfully', 'data': {'date': data,
                                                                                                  'User': user_email}},
                            status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
def get_order(request,variable):
    document_id = ObjectId(variable)
    original_value = Order_collection.find_one({'_id': document_id})
    print(original_value)
    if original_value:
        original_value['_id'] = str(original_value['_id'])
        return JsonResponse({'status': 'success', 'data': {'date': original_value}},
                            status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_order(request,variable):
    user_email = get_user(request)
    user = User_collection.find_one({"email": user_email})
    if user:
        document_id = ObjectId(variable)
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        original_value = Order_collection.find_one({'_id': document_id})
        print(original_value)
        if original_value and original_value.get('status') == 'PENDING':
            status = replace_none_with_default(data.get('status'), original_value.get('status'))
            new_value = {'$set': {'status': status}}
            order = Order_collection.find_one_and_update({'_id': document_id}, new_value)

            order['_id'] = str(order['_id'])
            return JsonResponse({'status': 'success', 'data': {'date': order}},)
        else:
            return JsonResponse({'error': 'Invalid'});
    else:
        return JsonResponse({'error': 'Invalid'})
