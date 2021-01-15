from django.shortcuts import render
from django.utils import timezone
import requests
from .models import Search
from bs4 import BeautifulSoup
BASE_KERALA_URl="https://kerala.craigslist.org/d/services/search/?query={}"

# Create your views here.
def home(request):
    return render(request,template_name='base.html')


def new_search(request):
    search=request.POST.get('search')
    resp=requests.get(BASE_KERALA_URl.format(search))
    data=resp.text
    soup = BeautifulSoup(data, features='html.parser')
    baseimageurl = "https://images.craigslist.org/{}_300x300.jpg"

    post_listing  = soup.find_all('li', {'class': 'result-row'})
    final_post=[]
    for post in post_listing:
        post_title = post.find(class_='result-title').text
        post_url=post.find('a').get("href")

        imageurl="https://images.all-free-download.com/images/graphicthumb/blue_sky_hill_small_lake_hd_picture_166027.jpg"
        if post.find(class_='result-image').get('data-ids'):
            post_image=post.find(class_='result-image').get('data-ids').split(',')[0]
            post_image=post_image.split(':')[1]
            print(post_image)
            imageurl=baseimageurl.format(post_image)

        final_post.append((post_title, post_url,imageurl))
    stuff_for_frontend={'search':search,'final_post':final_post,}



    print(search)
    Search.objects.create(search=search)

    return render(request,'myapp/new_search.html',stuff_for_frontend)

def history(request):
    s=Search.objects.all()
    his={'history':s}

    return render(request,'myapp/history.html',his)