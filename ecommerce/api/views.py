from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from store.models import Product
from store.serializers import ProductSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_home(request):
    params = dict(request.GET)
    # if params:
    #     message = 'Params: '
    #     for param_key, param_value in params.items():
    #         message += f"{param_key}: {param_value}, "
    #     return JsonResponse({"message": message})
    # else:
    #     return JsonResponse({"message": "Hmm, you didn't pass any params, did you?"})
    if params.get("pid"):
        try:
            id = int(params["pid"][0])
        except Exception:
            return Response({"detail": "Sorry, the product id must be a number."})
        try:
            product = Product.objects.get(pk=id)
        except Exception:
            return Response({"detail": "Sorry, a product with that id doesn't exist."})
        data = ProductSerializer(product).data
        return Response({"product": data})
    else:
        return Response({"detail": "Hmm, you didn't pass the product id, did you?"})
