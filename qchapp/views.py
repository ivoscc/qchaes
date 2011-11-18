#-*- coding:utf-8 -*-
from flask import url_for,render_template,request,redirect,session,make_response
from string import uppercase

from qchapp import app
from qchapp.models import Entry,Definition
from qchapp.forms import DefinitionForm
from qchapp.utils import slugEncode,Paginator

from settings import PAGE_SIZE
import re
import translitcodec
import simplejson


@app.route('/')
def main():
    samples = []

    e = Entry.objects.get(slug=Entry.get_random()['slug'])
    samples.append({'name':e.name,'definition':e.get_hero()})
    e = Entry.objects.get(slug=Entry.get_random()['slug'])
    samples.append({'name':e.name,'definition':e.get_hero()})
    e = Entry.objects.get(slug=Entry.get_random()['slug'])
    samples.append({'name':e.name,'definition':e.get_hero()})

    return render_template('main.html',letters=[x for x in uppercase],samples=samples)

#View for word
@app.route('/<word>')
def qchar(word):
  """
  
  """
    slug = slugEncode(word).lower()
    try:
        entry = Entry.objects.get(slug = slug)
        return render_template('word.html',entry=entry,definitions=entry.get_definitions(),word="todo bien")
    except Entry.DoesNotExist:
        return render_template('word.html',word=word.replace('_',' '))
    return render_template('404.html'), 404


@app.route('/definir/<slug>',methods=['GET','POST'])
def define(slug):
    captcha={'ip_address': request.remote_addr}
    form = DefinitionForm(request.form,captcha=captcha)
    if slug != 'x':
        form.entry.data = slug.replace('_',' ')

    if request.method == 'POST' and form.validate():
        #Check if entry exists previously
        slug = slugEncode(form.entry.data).lower()
        try:
            entry = Entry.objects.get(slug = slug)
        except Entry.DoesNotExist:
            entry = Entry(name=form.entry.data)
        d = Definition(content=form.definition.data,example=form.example.data)
        d.save()
        entry.definitions.append(d)
        entry.save()
        return redirect(url_for('qchar',word=slug))
    return render_template('new_definition.html',form=form)

#Resultados por letra
@app.route('/letra/<letra>/<int:page>/')
def by_letter(letra='A',page=0):
    if len (letra) != 1:
        return redirect(url_for('main'))
    letra = letra.upper()
    r = Entry.objects.filter(first_letter = letra)

    count = r.count()/PAGE_SIZE+1
    if page >= count:
        page = count-1
    results = r[page*PAGE_SIZE:PAGE_SIZE*(page+1)]
    paginator = Paginator(page,count)

    if results:
        return render_template('results.html',results=results,paginator=paginator)
    else:
        return render_template('results.html')
    

@app.route('/votar/<operation>/<def_id>/')
def voting(operation,def_id):

    resp = make_response(redirect(request.referrer))
    voted = request.cookies.get(def_id)
    if voted:
        return resp
    else:
        try:
            d = Definition.objects.get(id=def_id)
        except Definition.DoesNotExist:
            return redirect(request.referrer)
        if operation == "mas":
            d.points = d.points+1
        elif operation == "menos":
            d.points = d.points-1
        d.save()

	resp.set_cookie(def_id,value='1')
	return resp

@app.route('/def/<def_id>/')
def show_def(def_id):
    try:
        d = Definition.objects.get(id=def_id)
    except Definition.DoesNotExist:
        return render_template('404.html'), 404
    name = Entry.objects.filter(definitions__contains=d)[0].name 
    return render_template('standalone.html',definition=d,entry_name=name)

@app.route('/random')
def random():
    word = Entry.get_random()['slug']
    return redirect(url_for('qchar',word=word))

@app.route('/buscar/<int:page>/')
def search(page=0):
    id_list = Entry.search(''.join(request.args['b']))
    count = len(id_list)/PAGE_SIZE+1
    if page >= count:
        page = count-1

    r = [] 
    for i in id_list[page*PAGE_SIZE:PAGE_SIZE*(page+1)]:
        r.append(Entry.objects.get(id=i))

    paginator = Paginator(page,count)

    return render_template('results.html',results=r,paginator=paginator)

@app.route('/buscar/top/')
def searchbox():
    term = request.args['term']
    if not re.match(ur"^[a-zA-Z0-9\s_áéíóúÁÉÍÓÚñÑ]+$", term):
        return ""
    term = term.encode('translit/long')
    if len(term) >= 1:
        return simplejson.dumps(Entry.search_terms(term))
    else:
        return ""

""" make apache handle it later on """
@app.errorhandler(404)
def page_not_found(error):
        return render_template('404.html'), 404
@app.errorhandler(500)
def page_not_found(error):
        return render_template('404.html'), 500
        
if __name__ == "__main__":
  pass
  #blahtests
