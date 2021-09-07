import logging
from json import JSONDecodeError

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Account


class UserView(APIView):
    @staticmethod
    def put(request: Request) -> Response:
        """creates a new account if there is no record with specified email"""
        request_body = request.data
        try:
            # TODO: add a validator
            accounts: Account = Account.objects.filter(email=request_body['email'])
            if len(accounts) > 0:
                raise ValueError(request_body['email'])

        except JSONDecodeError as e:
            logging.warning('Malformed input data: %s', e)
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            logging.warning('Key is missed: %s', e)
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            logging.warning('Try to save a new user with existing data: %s', e)
            return Response(data={}, status=status.HTTP_409_CONFLICT)

        new_account = Account(**request_body)
        new_account.save()
        new_pk = new_account.pk
        return Response(data={
            'id': new_pk
        })

    @staticmethod
    def get(request: Request, user_id: int) -> Response:
        """
        Returns user data with the given id
        :param request: Request object
        :param user_id: user's id
        :return: JSON object with user's data or empty object
        """
        try:
            account = Account.objects.get(pk=user_id)
        except Account.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)

        # TODO: use a validator to get JSON
        return Response(data={
            'id': account.id,
            'first_name': account.first_name,
            'last_name': account.last_name,
            'email': account.email,
        })

    @staticmethod
    def patch(request: Request, user_id: int) -> Response:
        """
        Updates info about the particular user
        :param request: Request object
        :param user_id: User's id
        :return: 200, 400 or 404
        """
        request_body = request.data
        try:
            account = Account.objects.get(pk=user_id)
        except Account.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)

        # TODO: to write a validator for input
        return Response(data={}, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request: Request, user_id: int) -> Response:
        try:
            account = Account.objects.filter(pk=user_id)
        except Account.DoesNotExists as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        account.delete()
        return Response(data={}, status=status.HTTP_200_OK)
