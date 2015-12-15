import requests
import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.template.context_processors import csrf
from django.template import RequestContext
#from django.core.context_processors import csrf
from .models import AuthUser
from .models import Book
from .models import Reservation
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'auth.html')


# def index(request):
# 	times = int(os.environ.get('TIMES',3))
#     	return HttpResponse('Hello! ' * times)
def login_user(request):
    state = "Please log in below..."
    username = password = ''
    c = {}
    c.update(csrf(request))
	
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('landing/', {'user':user})
                    #return render_to_response('landing.html',{'user':user},context_instance=RequestContext(request))
                #state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('auth.html',{'state':state, 'username': username, 'password':password},context_instance=RequestContext(request))#
    #return direct_to_template('auth.html',{'state':state, 'username': username},)

def landing(request):
    user = request.user
    book = Book.objects.all().order_by('last_reserve')
    user_reserved = Reservation.objects.filter(reserved_user = user.id)
   # book_user_reserved = Book.objects.filter(book_id = user_reserved.book)
    book_own = Book.objects.filter(owner_user = user.id)
    #print user
    return render_to_response('landing.html',{'book': book, 'user_reserved': user_reserved, 'book_own':book_own, 'user':request.user},context_instance=RequestContext(request))
    #return render(request, 'landing.html')

def db(request):

    #greeting = Greeting()
    #greeting.save()

    #greetings = Greeting.objects.all()
	
	users = AuthUser.objects.all()
	return render(request, 'db.html', {'users': users})

