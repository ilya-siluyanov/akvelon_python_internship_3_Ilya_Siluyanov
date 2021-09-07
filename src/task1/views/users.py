import json
import logging
from json import JSONDecodeError

from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from src.task1.models.account import Account


@require_http_methods(["PUT"])
def create_user(request: HttpRequest) -> JsonResponse:
    request_body = request.body
    try:
        request_body = json.loads(request_body)
        accounts: Account = Account.objects.filter(email=request_body['email'])
        if len(accounts) > 0:
            raise ValueError(request_body['email'])

    except JSONDecodeError as e:
        logging.warning('Malformed input data: %s', e)
        return JsonResponse(data={}, status=400)
    except KeyError as e:
        logging.warning('Key is missed: %s', e)
        return JsonResponse(data={}, status=400)
    except ValueError as e:
        logging.warning('Try to save a new user with existing data: %s', e)
        return JsonResponse(data={}, status=409)

    new_account = Account(**request_body)
    new_account.save()
    new_pk = new_account.pk
    return JsonResponse(data={
        'id': new_pk
    })
