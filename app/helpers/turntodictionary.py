from datetime import datetime, time, timedelta
from app.models.turn import Turn

def listOfTurns(center, fecha):
    bt = str(center.opening_time)
    et = str(center.closing_time)
    hourAux = int(bt[0:2])
    minAux = int(bt[3:5])
    times = []
    while hourAux < int(et[0:2]):
        times.append(time(hour=hourAux, minute=minAux))
        hourAux = hourAux+1 if minAux == 30 else hourAux
        minAux = 0 if (minAux == 30) else 30
    takenTurns = Turn.horas_ocupadas(center.id, fecha)
    for turns in takenTurns:
        hour = str(turns)[0:2]
        minu = str(turns)[3:5]
        tt = time(hour=int(hour), minute=int(minu))
        if tt in times:
            times.remove(tt)
    arr=[]
    for t in times:
        aux= str(t)
        minAux = 0 if (int(aux[3:5]) == 30) else 30
        hourAux= int(aux[0:2]) if minAux == 30 else (int(aux[0:2]) + 1) 
        endTurn= time(hour=hourAux, minute=minAux)
        arr.append(createDictionary(t,endTurn, center.id, fecha))
    
    return arr

def createDictionary(beginTime, endTime, idcenter, fecha):
    d={}
    d['centro_id']=str(idcenter)
    d['hora_inicio']=str(beginTime)
    d['hora_fin']=str(endTime)
    d['fecha']=str(fecha)
    return d

def turnToDictionary(turn):
    d={}
    arr=[]
    for h in turn.helpcenter:
        arr.append(h.id)
    d["centro_id"]=str(arr[0])
    d["email_donante"]=turn.user
    d["telefono_donante"]=turn.phone
    d["hora_inicio"]=str(turn.opening_time)
    if str(turn.opening_time)[3:4]=='0':
        t=time(hour=int(str(turn.opening_time)[0:2]),minute=30)
    else:
        t=time(hour=int(str(turn.opening_time)[0:2])+1,minute=0)
    d["hora_fin"]=str(t)
    d["fecha"]=str(turn.date)
    return d
