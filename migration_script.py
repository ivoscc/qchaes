from mongoengine import *
from qchaapp.models.model import Definition, Old_definition

connect('qchapp',username='',password='',host='',port=10094)

for item in Old_definition.objects:
  print item.content

