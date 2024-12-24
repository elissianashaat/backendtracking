import json

from bson import ObjectId
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from authentication.models import User_collection
from authentication.views import get_user
from order.models import Order_collection
from order.mongoDb_utils import convert_array_to_serializable, replace_none_with_default


def get_numbers():
    return list(range(1, 11))


def find_all_order():
    orders = Order_collection.find({})
    orders_list = list(orders)
    print(orders_list)
    return orders_list


@api_view(['GET'])
def get_all_order(request):
    user_email = get_user(request)
    user = User_collection.find_one({"email": user_email})
    if user and user.get('role') == 'ADMIN':
        order = find_all_order()
        print(order)
        send = convert_array_to_serializable(order)
        return JsonResponse({'status': 'success', 'length:': len(order), 'data': send},
                            status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['PUT'])
def assign_order_courier(request):
    user_email = get_user(request)
    user = User_collection.find_one({"email": user_email})
    if user and user.get('role') == 'ADMIN':
        data = json.loads(request.body.decode('utf-8'))
        document_id = ObjectId(data.get('orderId'))
        order = Order_collection.find_one({"_id": document_id})
        if order:
            courierId = replace_none_with_default(data.get('courierId'), order.get('courierId'))
            new_value = {'$set': {'courierId': courierId}}
            order = Order_collection.find_one_and_update({'_id': document_id}, new_value)
            order['_id'] = str(order['_id'])
            return JsonResponse({'status': 'success'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'No order Found'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['DELETE'])
def delete_order(request, variable):
    user_email = get_user(request)
    user = User_collection.find_one({"email": user_email})
    if user:
        document_id = ObjectId(variable)
        order = Order_collection.find_one({"_id": document_id})
        if order:
            Order_collection.delete_one({"_id": document_id})
            return JsonResponse({'status': 'success', 'message': 'Order deleted successfully'},
                                status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_403_FORBIDDEN)
