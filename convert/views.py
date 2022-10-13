from rest_framework.views import APIView
from rest_framework import status
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from .serializers import *
from helpers.api_helper import *
from helpers.enum_helper import *
from helpers.authentication_helper import *
from helpers.auth_helper import login_required
from helpers.views_helper import *
from django.core.files.storage import FileSystemStorage
# Create your views here.
class Upload(APIView):
    @method_decorator(login_required())
    def patch(self, request):
        try:
            uploaded_file = Uploads.objects.create(user=request.user)
            myfile=request.FILES['uploaded_image']
            fs = FileSystemStorage()
            file = fs.save(myfile.name,myfile)
            fileurl = fs.url(file)
            uploaded_file.uploaded_image=fileurl

            #Thumbnail(200x300)
            uploaded_file.thumbnail_image=resize_img(uploaded_file,fileurl,(200,300),1,myfile.name)

            #Medium
            uploaded_file.medium_image=resize_img(uploaded_file,fileurl,(500,500),2,myfile.name)

            #Large
            uploaded_file.large_image=resize_img(uploaded_file,fileurl,(1024,768),3,myfile.name)

            #Grayscale
            uploaded_file.grayscale_image=convert_img(uploaded_file,fileurl,4,myfile.name)

            uploaded_file.save()
            serializer = ConvertSerializer(uploaded_file, many=False)
            data=add_urls(serializer.data)
            return Response(api_response(ResponseType.SUCCESS, API_Messages.PROFILE_UPDATED,data), status=status.HTTP_200_OK)
        except Exception as exception:
            return Response(api_response(ResponseType.FAILED, str(exception)), status=status.HTTP_400_BAD_REQUEST)
