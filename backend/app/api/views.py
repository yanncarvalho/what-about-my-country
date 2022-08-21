import json
from typing import Dict, List, Tuple, Union
from ariadne import graphql_sync
from app.api import schema
from django.conf import settings as conf
from django.http import JsonResponse
from django.views import View

ErrorResponseValues = List[Dict[str, str]]
ErrorResponse = Dict[str, ErrorResponseValues]
GraphQLRespValues = Union[str, int, float]
GraphQLResp = Dict[str, GraphQLRespValues]

class BasicView(View):
  """BasicView class implements model methods for all views"""

  def http_method_not_allowed(self, request, *_) -> ErrorResponse:
    """error handler to not allowed method"""
    return _error_request(f'{request.method} method not allow to this path.', 405)

  @staticmethod
  def _sanitizeResponse(response: Dict[str, Union[str, int, float]]) -> Tuple[GraphQLResp, int]:
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

class CountryViewVersionOne(BasicView):
  """CountryView class representing the country API view version 1."""

  def post(self, request) -> GraphQLResp:
    """post request"""
    data: Dict[str, Union[str, int, float]] = json.loads(request.body)
    _, response = graphql_sync(
        schema.schema,
        data,
        context_value=request,
        debug=conf.DEBUG,
        error_formatter=schema.format_error,
    )
    result, status_code = BasicView._sanitizeResponse(response)
    return JsonResponse(data=result, status=status_code)




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


def _error_request(message: str, status_code: int) -> ErrorResponse:
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
