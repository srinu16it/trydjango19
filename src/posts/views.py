from django.core.mail import send_mail
from urllib import quote_plus
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404,redirect
from .forms import PostForm
from .models import Post

# Create your views here.

def post_create(request):
    #if not request.user.is_staff: #or not request.user.is_superuser:
    #    raise Http404

    form=PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        print form.cleaned_data.get("title")
        instance.save()
        #message success
        messages.success(request, "Sucessfully Created")
        return HttpResponseRedirect(instance.get_absloute_url())
    else:
        messages.error(request,"not Sucessfully created")
    context={
        "form":form,
    }
    return render(request,"post_form.html",context)

def post_detail(request,slug=None): #retrieve
    instance=get_object_or_404(Post, slug=slug)
    context={
        "title": instance.title,
        "instance":instance,
    }
    return render(request,"post_detail.html",context)

def post_list(request): #list items
    queryset_list = Post.objects.all()

    query=request.GET.get("q")
    if query:
        queryset_list= queryset_list.filter(
        Q(title__icontains=query)|
        Q(content__icontains=query)|
        Q(user__first_name__icontains=query)
        ).distinct()

    paginator = Paginator(queryset_list, 6) # Show 25 contacts per page
    page_request_var= "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context={
        "object_list":queryset,
        "title":"list",
        "page_request_var": page_request_var
      }
    return render(request,"post_list.html",context)


def post_update(request, slug =None):
    #if not request.user.is_staff: #or not request.user.is_superuser:
    #    raise Http404
    instance=get_object_or_404(Post, slug=slug)
    form=PostForm(request.POST or None,request.FILES or None,instance=instance)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        #message success
        messages.success(request, "Item saved",extra_tags='some-tag')
        return HttpResponseRedirect(instance.get_absloute_url())

    context={
        "title": instance.title,
        "instance":instance,
        "form":form,
    }
    return render(request,"post_form.html",context)

def post_delete(request, slug =None):
    #if not request.user.is_staff: #or not request.user.is_superuser:
    #    raise Http404
    instance=get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Sucessfully Deleted")
    return redirect("posts:list")

def about(request):
	return render(request, "about.html", {})
