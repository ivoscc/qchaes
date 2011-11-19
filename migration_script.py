from mongoengine import *
from qchapp.models import Definition,Example

#connect('qchaes',username='qcha',password='qchaestapasando',host='dbh85.mongolab.com',port=27857)
#pymongo.Connection( host='mongodb://qcha:qchaestapasando@dbh85.mongolab.com/qchaes:27857')
connect('qchaes',username='qcha',password='qchaestapasando',host='dbh85.mongolab.com',port=27857)

for item in Definition.objects:
  tmp = Example( body=item.example,points=0)
  item.examples.append(Example( body=item.example,points=0))
  item.save()

print '############START################'
  
for item in Definition.objects:
  for ite in item.examples:
    print ite.body
    print ite.points