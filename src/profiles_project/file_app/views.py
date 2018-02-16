from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from . import serializers
import sys, zipfile, os, os.path
from django.conf import settings
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'home.html'

class FileView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  def post(self, request, *args, **kwargs):
    file_serializer = serializers.FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()

      # Convert file and dir into absolute paths
      fullpath = settings.MEDIA_ROOT+"/Retention_Dashboard.zip"
      dirname = os.path.dirname(fullpath)

      # Unzip the file, creating subdirectories as needed
      zfobj = zipfile.ZipFile(fullpath, 'r')
      for name in zfobj.namelist():
          if not os.path.isdir(os.path.join(dirname, 'links')):
              os.mkdir(os.path.join(dirname, 'links'))
          if name.endswith('/'):
              try: # Don't try to create a directory if exists
                  os.mkdir(os.path.join(dirname, name))
              except:
                  pass
          else:
              outfile = open(os.path.join(dirname, name), 'wb')
              outfile.write(zfobj.read(name))
              outfile.close()

      # Now try and delete the uploaded .zip file and the
      # stub __MACOSX dir if they exist.
      try:
          os.remove(fullpath)
      except:
          pass
      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
