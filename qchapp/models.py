from mongoengine import *
import re
from operator import attrgetter
from random import random
from qchapp.utils import slugEncode

connect('qchapp',username='',password='',host='',port=10094)

class Example:
    body = StringField(max_length=300)
    points = IntField(default=0)


class Definition(Document):
    """
    examples debe ser una a una 'estructura'
    """
    points = IntField(default=0)
    content = StringField(min_length=15,max_length=300)
    examples = ListField( EmbeddedDocumentField(Example) )
    #example = StringField(max_length=300)

    def __repr__(self):
        return u'Def: %r' % (self.content[:15]+"...")
        
class Old_definition(Document):
    """
    Antigua_def
    """
    points = IntField(default=0)
    content = StringField(min_length=15,max_length=300)
    example = StringField(max_length=300)

    def __repr__(self):
        return u'Def: %r' % (self.content[:15]+"...")


class Entry(Document):
    name = StringField(unique=True,min_length=3,max_length=100)
    slug = StringField(unique=True,min_length=3,max_length=100)
    first_letter = StringField(max_length=1)
    definitions = ListField(ReferenceField(Definition,reverse_delete_rule=CASCADE))
    keywords = ListField(StringField())
    random = FloatField(min_value=0,max_value=1)


    #Use this method instead of attribute to get sorted definition list
    def get_definitions(self):
        return sorted(self.definitions,\
                      key=attrgetter('points'),\
                      reverse=True)

    #Returns the definition with the most points
    def get_hero(self):
        return sorted(self.definitions,\
                      key=attrgetter('points'),\
                      reverse=True)[0]

    def save(self, *args, **kwargs):
        slug = slugEncode(self.name)
        self.slug = slug.lower()
        self.first_letter = self.slug[0].upper()
        self.random = random()
        keywords = slug.split('_')
        [keywords.pop(keywords.index(x)) for x in [i for i in keywords if len(i)<3]]
        self.keywords = keywords
        super(Entry, self).save(*args, **kwargs)

    def __repr__(self):
        return u'Entry: %r' % (self.slug)



    @staticmethod
    def search(query):
        query = re.sub(r'\W+',' ',query)
        lista = query.split()
        lista = [i+"|" for i in lista if len(i)>2]
        terms = ''.join(lista)[:-1]
        if len(terms)>0:
            code = """
            r = [];
            var result = db.entry.find({keywords: /(%s)/i},{_id:true});
            for (var i=0;i < result.length(); i++){
                r.push(result[i]['_id']);
            }
            return r;
            """ % terms
            results =  Entry.objects.exec_js(code)
            return [str(i) for i in results]
        else:
            return []

    @staticmethod
    def search_terms(characters):
        code = """
        r = [];
        result = db.entry.find({slug:/.*^%s/},{name:true}).limit(5);
        for (var i=0;i < result.length(); i++){
            r.push(result[i]['name']);
        }
        return r;
        """ % characters
        return  Entry.objects.exec_js(code)

    @staticmethod
    def get_random():
        code = """
        rand = Math.random()
        cmp = Math.random()
        result = db.entry.findOne( {random : { $gte : rand } } )
        if ( result == null ) {
            result = db.entry.findOne( {random : { $lte : rand } } )
        }
        return result;
        """
        return Entry.objects.exec_js(code)
 
