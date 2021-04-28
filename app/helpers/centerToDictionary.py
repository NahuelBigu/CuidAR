from app.models.helpcenter import HelpCenter


def dictionaryPerPage(centros, cantidad, page):
    dic={}
    dic['helpcenters']=lisOfCenters(centros)
    dic['total']=cantidad
    dic['page']=page
    return dic

def lisOfCenters(centros):
    arr=[]
    for centro in centros:
        arr.append(toDictionary(centro))
    return arr

def toDictionary(centro):
    d={}
    d['id']=centro.id
    d['name']=centro.name
    d['address']=centro.address
    d['phone']=centro.phone
    d['lng']=centro.longitude
    d['lat']=centro.latitude
    d['opening_time']=str(centro.opening_time)
    d['closing_time']=str(centro.closing_time)
    arr=[]
    for t in centro.type_center:
        arr.append(t.name)
    d['type_center']=arr
    d['web']=centro.web
    d['email']=centro.email
    return d
