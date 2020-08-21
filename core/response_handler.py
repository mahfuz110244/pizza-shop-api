from rest_framework.response import Response


def custom_response_ok(success, status_code, data=None, headers=None, error=None, errorMessage=None):
    """
    This is Custom Return Response Handler
    :param success:
    :param status_code:
    :param data:
    :param headers:
    :param error:
    :param errorMessage:
    :return:
    """
    if not success:
        error = {'errorCode': status_code, 'errorMessage': errorMessage}
    response = {'success': success, 'status_code': status_code, 'data': data, 'error': error}
    return Response(response, status=status_code, headers=headers)