from django.http import JsonResponse


def handler404(request, exception):
    message = ('Path not Found!')
    response = JsonResponse({'data': message}) 
    response.status_code = 404
    return response

def handler500(request):
    message = ('Internal Server Error !!')
    response = JsonResponse({'data': message}) 
    response.status_code = 500
    return response