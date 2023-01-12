from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from .FileSystemStorage import MyCustomStorage
from .forms import UploadForm
from .models import Image
from .SudokuSolver import SudokuSolver

# Create your views here.
def index(request):
    show_img = 0
    show_matrix = 0
    matrix = [[0 for i in range(0,9)] for j in range(0,9)]
    if 'submit-upload' in request.POST:
        if request.method == 'POST' and request.FILES['myfile']:
            print('vao post')
            myfile = request.FILES['myfile']
            fs = MyCustomStorage()
            file = fs.save('image.jpg', myfile)
            fileurl = fs.url(file)
            show_img = 1

    if 'submit-process' in request.POST:
        show_img = 1
        show_matrix = 1
        matrix = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
                    [5, 2, 0, 0, 0, 0, 0, 0, 0],
                    [0, 8, 7, 0, 0, 0, 0, 3, 1],
                    [0, 0, 3, 0, 1, 0, 0, 8, 0],
                    [9, 0, 0, 8, 6, 3, 0, 0, 5],
                    [0, 5, 0, 0, 9, 0, 6, 0, 0],
                    [1, 3, 0, 0, 0, 0, 2, 5, 0],
                    [0, 0, 0, 0, 0, 0, 0, 7, 4],
                    [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    # if request.method == "POST":
    #     form=UploadForm(data=request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         obj=form.instance
    #         return
    #     else:
    #         form=UploadForm()
    #     img=Image.objects.all()
    
    if 'submit-solver' in request.POST:
        show_img = 1
        objSolve = SudokuSolver(matrix)
        if objSolve.solveSudoku(0,0):
            matrix = objSolve.grid
    
    if show_img == 0:
        fs_empty = FileSystemStorage()
        fs_empty.delete('image.jpg')
    
    template = loader.get_template('sudokuDIP/index.html')
    context = {
        'show_img': show_img,
        'show_matrix': show_matrix,
        'matrix': matrix,
        'range': range(9),
    }
    # img=Image.objects.all()
    return HttpResponse(template.render(context, request))