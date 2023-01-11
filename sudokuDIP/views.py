from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from .FileSystemStorage import MyCustomStorage
from .forms import UploadForm
from .models import Image

# Create your views here.
def index(request):
    fs_empty = FileSystemStorage()
    fs_empty.delete('image.jpg')
    show_img = 0

    if request.method == 'POST' and request.FILES['myfile']:
        print('vao post')
        myfile = request.FILES['myfile']
        fs = MyCustomStorage()
        file = fs.save('image.jpg', myfile)
        fileurl = fs.url(file)
        show_img = 1

    # if request.method == "POST":
    #     form=UploadForm(data=request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         obj=form.instance
    #         return
    #     else:
    #         form=UploadForm()
    #     img=Image.objects.all()

    template = loader.get_template('sudokuDIP/index.html')
    context = {
        'show_img': show_img
    }
    # img=Image.objects.all()
    return HttpResponse(template.render(context, request))