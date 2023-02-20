from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from .FileSystemStorage import MyCustomStorage
from .forms import UploadForm
from .models import Image
from .SudokuSolver import SudokuSolver
from ocr import *
import cv2
# Create your views here.
def index(request):
    show_img = 0
    show_matrix = 0
    error_matrix = 0
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

        original = cv2.imread('sudokuDIP\static\sudokuDIP\image\image.jpg')
        gray = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray,20,30,30)
        edged = cv2.Canny(gray,10,20)

        txt = process(find_contours(edged,original))

        # biggest_cnt = find_biggestcnt(original)
        # img_warped = warp_img(original,biggest_cnt)
        # img_warped_bin = warpImg_processing(img_warped)
        # cell_detected = detect_cell(img_warped_bin)
        # txt = detect_num(cell_detected,img_warped)

        numList = txt.split()
        numList = [int(i) for i in numList]
        matrix = [numList[i:i+9] for i in range(0, len(numList), 9)]
        
    
    if 'submit-solver' in request.POST:
        show_img = 1
        show_matrix = 1
        data = request.POST.dict()
        txt = data.get("submit-solver")
        txt = txt.replace('[', '').replace(',','').replace(']', '')

        numList = txt.split()
        numList = [int(i) for i in numList]
        matrix = [numList[i:i+9] for i in range(0, len(numList), 9)]
        objSolve = SudokuSolver(matrix)
        if objSolve.solveSudoku(0,0):
            matrix = objSolve.grid
        else:
            matrix = [numList[i:i+9] for i in range(0, len(numList), 9)]
            # print('fsfsdfsd')
            error_matrix = 1
            # print(error_update)

    
    if 'submit-edit-matrix' in request.POST:
        show_img = 1
        show_matrix = 1
        data = request.POST.dict()
        txt = data.get("update-matrix")
        # matrix = txt
        # print(txt)
        txt = txt.replace(',',' ')

        numList = txt.split()
        numList = [int(i) for i in numList]
        matrix = [numList[i:i+9] for i in range(0, len(numList), 9)]

    if show_img == 0:
        fs_empty = FileSystemStorage()
        fs_empty.delete('image.jpg')
    
    template = loader.get_template('sudokuDIP/index.html')
    context = {
        'show_img': show_img,
        'show_matrix': show_matrix,
        'error_matrix': error_matrix,
        'matrix': matrix,
        'range': range(9),
    }
    return HttpResponse(template.render(context, request))