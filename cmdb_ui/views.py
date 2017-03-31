from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse

# Create your views here.


def index(request):
    return HttpResponseRedirect(reverse('cmdb_ui:login'))


@csrf_exempt
def login(request):
    return render(request, 'login.html')



