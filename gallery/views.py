from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from PIL import Image as PilImage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Image


def is_ajax(self):
    # check whether the request is ajax, replacement of default is_ajax method
    return self.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def upload(request):

    # if this is a POST request we need to process the form data
    if request.method == "POST":
        images = request.FILES.getlist('images')
        tags = request.POST.getlist('tags')
        for image in images:
            image_object = Image.objects.create(image=image)
            for tag in tags:
                image_object.tags.add(tag)

    # handle AJAX Call
    if is_ajax(request):
        tag_list = request.GET.get('value').split(',')
        if tag_list[0] == '':
            filtered_image = Image.objects.all()
        else:
            filtered_image = Image.objects.filter(tags__name__in=tag_list)
        image_urls = [p.image.url for p in filtered_image]
        # print(image_urls)
        return JsonResponse({'data': image_urls })

    images = Image.objects.all()
    tags = Image.tags.all()
    page = request.GET.get('page', 1)

    # pagination for 8 images per page
    paginator = Paginator(images, 8)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
        
    return render(request, 'index.html', {'images': images, 'tags': tags})


def specific_image(request, pk):
    # filter images by pk
    image = Image.objects.get(id = pk)
    
    return render(request, 'specific_image.html', {'image': image})


def save_rotated_image(request):
    # rotation value and image id
    rotationAmt = request.GET.get('value')
    image_id = request.GET.get('image_id')

     #getting instance of the model
    item=Image.objects.get(pk=image_id)

    #opening image for PIL to access
    im = PilImage.open(item.image)

    #rotating it by built in PIL command
    rotated_image = im.rotate(-int(rotationAmt), PilImage.NEAREST, expand = True)

    #saving rotated image instead of original. Overwriting is on. 
    rotated_image.save(item.image.file.name, overwrite=True)

    return HttpResponse(str(item.image))
  