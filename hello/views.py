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
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from .models import AuthUser
from .models import Book
from .models import Reservation
from .models import Tag
from .models import TagBook
from .forms import BookForm
from .forms import EditBookForm
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
            #login(request, user)
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
def logout_view(request):
    logout(request)
    return render_to_response('auth.html',context_instance=RequestContext(request))
   

def landing(request):
    user = request.user
    if user.is_active : 

        book = Book.objects.all().order_by('-last_reserve').filter(avail_end__gte = timezone.now())

        user_reserved = Reservation.objects.filter(reserved_user = user.id).order_by('reserved_start').filter(reserved_end__gte = timezone.now())
       
        time = timezone.now()

       # book_user_reserved = Book.objects.filter(book_id = user_reserved.book)
        book_own = Book.objects.all().filter(owner_user = user.id, avail_end__gte = timezone.now()).order_by('avail_start')
        #print user

        return render_to_response('landing.html',{'time':time, 'book': book, 'user_reserved': user_reserved, 'book_own':book_own, 'user':request.user},context_instance=RequestContext(request))

    else:
        return render_to_response('auth.html',context_instance=RequestContext(request))

def addBook(request):
    state = 'Enter New Book Details here'
    init = True
    valid_avail = True
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            

            book = form.save(commit=False)
            book.owner_user = AuthUser.objects.get(pk=request.user.id)
            book.last_reserve = timezone.now()
            if book.avail_start > book.avail_end:
                valid_avail = False
                state = "PLease enter valid availability time details"
                return render_to_response('addBook.html', {'form': form, 'state': state, 'valid_avail':valid_avail}, context_instance=RequestContext(request))
            
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
                if valid_avail:
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
    reservation = Reservation.objects.filter(book = current_book.book_id, reserved_end__gte = timezone.now())
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
            
            bookavail_start = book.avail_start
            bookavail_end = book.avail_end
            
            if reserve_end < timezone.now():
                state = 'Make a reservation in the future'
                error =True
                return render_to_response('addReserve.html', {'error':error,'form': form, 'state': state, 'init': init, 'book':book,'bookName': bookName, 'reserve_start': reserve_start, 'reserve_end': reserve_end, 'duration': duration}, context_instance=RequestContext(request))

            
            if (reserve_start < bookavail_start or reserve_end > bookavail_end):
                state = 'book is not available '
                error = True
                return render_to_response('addReserve.html', {'error':error,'form': form, 'state': state, 'init': init, 'book':book,'bookName': bookName, 'reserve_start': reserve_start, 'reserve_end': reserve_end, 'duration': duration}, context_instance=RequestContext(request))

            if (duration <= 0):
                state = 'provide positive duration'
                error = True
                return render_to_response('addReserve.html', {'error':error,'form': form, 'state': state, 'init': init, 'book':book,'bookName': bookName, 'reserve_start': reserve_start, 'reserve_end': reserve_end, 'duration': duration}, context_instance=RequestContext(request))

            
            if (len(overlapObj) == 0) :
               
                reserve.save()
                state = 'Newly added Reservation Details for the book '
                error = False
            
            init = False
            return render_to_response('addReserve.html', {'error':error,'form': form, 'state': state, 'init': init, 'book':book,'bookName': bookName, 'reserve_start': reserve_start, 'reserve_end': reserve_end, 'duration': duration}, context_instance=RequestContext(request))        
         

    else:
        form = ReserveForm()
    return render_to_response('addReserve.html',{'state':state,'form':form, 'init': init, 'book':book},context_instance=RequestContext(request))    

def editResource(request, book):
    state = 'Edit the book details'
    init = True
    valid_avail = True
    existBook = Book.objects.get(pk = book)
    oldName = existBook.name
    oldAvail = existBook.avail_start
    oldEnd = existBook.avail_end
    if request.method == 'POST':
        form = EditBookForm(request.POST, instance=existBook)
        if form.is_valid():

            bookDetails = form.save(commit=False)
            #bookDetails.book_id = existBook.book_id
            bookDetails.owner_user = AuthUser.objects.get(pk=request.user.id)
            bookDetails.last_reserve = existBook.last_reserve
            if bookDetails.avail_start > bookDetails.avail_end:
                valid_avail = False
                state = "PLease enter valid availability time details"
                return render_to_response('addBook.html', {'form': form, 'state': state, 'valid_avail':valid_avail}, context_instance=RequestContext(request))
            
            bookDetails.save()  

            state = 'Newly Edited Details of the book are'
            init = False
            editName = bookDetails.name
            navail_start = bookDetails.avail_start
            navail_end = bookDetails.avail_end
            return render_to_response('editResource.html', {'form': form, 'state': state, 'init': init, 'editName': editName, 'navail_start': navail_start, 'navail_end': navail_end}, context_instance=RequestContext(request))        
    else:
        
        data = {'name': '{{book}}', 'avail_start':'{{existBook.avail_start}}', 'avail_end': '{{existBook.avail_end}}'}
        form = EditBookForm(instance=existBook)
    return render_to_response('editResource.html',{'state': state, 'form':form, 'init': init},context_instance=RequestContext(request))  

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

def rssFeed(request, book):
    
    data = serializers.serialize("xml", Reservation.objects.filter(book_id = book))


    return render_to_response('rssFeed.html',{'data':data},context_instance=RequestContext(request))


def bookOwner(request, owner):
    #user = AuthUser.objects.get(username = owner)
    #user = AuthUser.objects.get(pk=owner)
            
    books = Book.objects.filter(owner_user = owner, avail_end__gte = timezone.now()).order_by('avail_start')
    reservations = Reservation.objects.filter(reserved_user = owner, reserved_end__gte = timezone.now()).order_by('reserved_start')

    return render_to_response('bookOwner.html',{'books':books, 'reservations': reservations},context_instance=RequestContext(request))

