import requests
import os
from django.utils import timezone 
import datetime
import re
from datetime import datetime, timedelta, time
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from .models import AuthUser
from .models import Book
from .models import Reservation
from .models import Tag
from .models import TagBook
from .forms import BookForm
from .forms import ReserveForm
from .forms import RegistrationForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return redirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
 
    return render_to_response('register.html',variables,)
 
def success(request):
    return render_to_response(
    'success.html',
    )

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

    user_reserved = Reservation.objects.filter(reserved_user = user.id, reserved_end__gte = timezone.now(),).order_by('reserved_start')
   


   # book_user_reserved = Book.objects.filter(book_id = user_reserved.book)
    book_own = Book.objects.filter(owner_user = user.id)
    #print user
    return render_to_response('landing.html',{'book': book, 'user_reserved': user_reserved, 'book_own':book_own, 'user':request.user},context_instance=RequestContext(request))
    #return render(request, 'landing.html')

def addBook(request):
    state = 'Enter New Book Details here'
    init = True
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            

            book = form.save(commit=False)
            book.owner_user = AuthUser.objects.get(pk=request.user.id)
            book.last_reserve = timezone.now()
            
            book.save()
            tags = request.POST.get('descTags')
            allTags = tags.split(',')
            for x in allTags:
                x.strip()
                try:
                    TagCheck = Tag.objects.get(tag_name = x)
                    addTag = TagCheck
                except:
                    addTag = Tag.objects.create(tag_name = x)
                    addTag.save()
                addTagBook = TagBook(tag = addTag, book = book)
                addTagBook.save()
                    

            state = 'Newly added Book Details are:'
            init = False
            name = book.name
            avail_start = book.avail_start
            avail_end = book.avail_end

            
            return render_to_response('addBook.html', {'form': form, 'state': state, 'init': init, 'name': name, 'avail_start': avail_start, 'avail_end': avail_end, 'tags':tags}, context_instance=RequestContext(request))   
    else:

        form = BookForm()
    return render_to_response('addBook.html', {'form': form, 'state': state, 'init': init}, context_instance=RequestContext(request))


def showBook(request, book):
    current_book = Book.objects.get(book_id = book)
    reservation = Reservation.objects.filter(book = current_book.book_id)
    current_user = request.user.username
    book_owner = current_book.owner_user.username

    isUser = 0
    if (book_owner == current_user):
        isUser = 1

    allTags = TagBook.objects.filter(book = book)
    tagStr = []
    for x in allTags:
        tagStr.append(x.tag.tag_name)
    return render_to_response('showBook.html',{'isUser': isUser, 'current_book': current_book, 'reservation': reservation, 'allTags':allTags},context_instance=RequestContext(request))

def addReserve(request,book):
    state = 'Add a Reservation for the book'
    init = True
    book = Book.objects.get(book_id = book)
    if request.method == 'POST':
        form = ReserveForm(request.POST)
        
        if form.is_valid():
            reserve = form.save(commit=False)
            reserve.book = book
            reserve.reserved_user = AuthUser.objects.get(pk=request.user.id)
            bookName = reserve.book.name
            reserve_start = reserve.reserved_start
            duration = reserve.duration
            reserve_end = reserve_start + timedelta(minutes = duration)
            reserve.reserved_end = reserve_end

            overlapObj = Reservation.objects.filter(reserved_start__lt = reserve_end, reserved_end__gt = reserve_start)
            state = 'Reservation in the time frame already exists'
            error = True
            bookavail = Book.objects.get(book_id = book)
            bookavail_start = bookavail.avail_start
            bookavail_end = bookavail.avail_end

            if (len(overlapObj) == 0) :
                reserve.save()
                state = 'Newly added Reservation Details for the book '
                error = False

            if (reserve_start < bookavail_start or reserve_end > bookavail_end):
                state = 'book is not available '
                error = True
                        
            init = False
            return render_to_response('addReserve.html', {'error':error,'form': form, 'state': state, 'init': init, 'book':book,'bookName': bookName, 'reserve_start': reserve_start, 'reserve_end': reserve_end, 'duration': duration}, context_instance=RequestContext(request))        
         

    else:
        form = ReserveForm()
    return render_to_response('addReserve.html',{'state':state,'form':form, 'init': init, 'book':book},context_instance=RequestContext(request))    

def editResource(request, book):
    state = 'Edit the book details'
    init = True
    existBook = Book.objects.get(book_id = book)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=existBook)
        if form.is_valid():

            bookDetails = form.save(commit=False)
            #bookDetails.book_id = existBook.book_id
            bookDetails.owner_user = AuthUser.objects.get(pk=request.user.id)
            bookDetails.last_reserve = existBook.last_reserve
            bookDetails.save()  

            state = 'Newly Edited Details of the book are'
            init = False
            editName = bookDetails.name
            navail_start = bookDetails.avail_start
            navail_end = bookDetails.avail_end
            return render_to_response('editResource.html', {'form': form, 'state': state, 'init': init, 'editName': editName, 'navail_start': navail_start, 'navail_end': navail_end,'existBook':existBook}, context_instance=RequestContext(request))        
         

    else:
        
        data = {'name': '{{book}}', 'avail_start':'{{existBook.avail_start}}', 'avail_end': '{{existBook.avail_end}}'}
        form = ReserveForm(initial=existBook)

    return render_to_response('editResource.html',{'state': state, 'form':form, 'init': init, 'book':book},context_instance=RequestContext(request))  

def delReserve(request, reserve):
    state = 'Delete the Reservation for '
    init = 1
    existReserve = Reservation.objects.get(reserved_id = reserve)
    if request.method == 'POST':
        existReserve.delete()
        init = 0
        state = 'Deleted the Reservation'
        return render_to_response('delReserve.html',{'state': state, 'init': init,},context_instance=RequestContext(request))

    return render_to_response('delReserve.html',{'state': state, 'init': init, 'existReserve': existReserve},context_instance=RequestContext(request))


def showTag(request, tagid):

    state = 'books available for this tag are '
    tagBook = TagBook.objects.filter(tag = tagid)
    

    return render_to_response('showTag.html',{'state': state,'tagid':tagid, 'tagBook':tagBook},context_instance=RequestContext(request))

