from django.http import HttpResponse
from .models import User

def index(request):
    users = User.objects.all()
    str = ""
    for user in users:
        str += user.first_name + "\n"
    return HttpResponse(str)
