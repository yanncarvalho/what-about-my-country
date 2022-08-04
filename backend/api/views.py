import json
from typing import Any, Dict, List, Tuple, Union
from ariadne import graphql_sync
from backend.api import schema
from django.http import JsonResponse

from django.conf import settings as conf
from django.views import View


class CountryView(View):
  """CountryView class representing the country API view."""
  @staticmethod
  def _sanitizeResponse(response: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    """ handles response before returning to user.

    Args:
    - response: a dictonary with response from graphql.

    Returns:
      Tuple with response code and dictionary with sanitized response.
    """
    if 'errors' in response.keys():
        response.pop("data", None)
        return response, 400
    else:
        return response, 200

  def post(self, request) -> Dict[str, Union[str, int, float]]:
    """post request"""
    data: Dict[str, Union[str, int]] = json.loads(request.body)
    _, response = graphql_sync(
        schema.schema,
        data,
        context_value=request,
        debug=conf.DEBUG,
        error_formatter=schema.format_error,
    )
    result, status_code = CountryView._sanitizeResponse(response)
    return JsonResponse(data=result, status=status_code)

  def http_method_not_allowed(self, request, *_) -> Dict[str, List[Dict[str, str]]]:
    """error handler to not allowed method"""
    return _error_request(f'{request.method} method not allow to this path.', 405)


def error_404(request, exception):
  """not found error response

  Args:
  - request: information about requisition

  Returns:
    A dictionary with not found error response
  """
  return _error_request(f'{request.path} path not found.', 400)


def error_500(_):
    """server error response

    Returns:
      A dictionary with server error response
    """
    return _error_request('Something happened: server cannot provide your request', 500)


def _error_request(message: str, status_code: int) -> Dict[str, List[Dict[str, str]]]:
    """default error formatting message

    Returns:
      A dictionary with response in JsonResponse
    """
    response = {
        'errors': [
            {
                'message': f'{message}'
            }
        ]
    }
    return JsonResponse(data=response, status=status_code)
