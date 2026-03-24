from django.shortcuts import render

# Create your views here.
def blog(request):
    # get all the data
    return render(request, 'blog.html', {'title':'blog'})


def post(request):
    #get post data based on the id
    return render(request, 'post.html', {'title':'post'})


    