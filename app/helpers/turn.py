from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.turn import Turn
from app.models.helpcenter import HelpCenter
from app.helpers.permission import check as has_permission
from flask import jsonify
from datetime import datetime, timedelta, time

from datetime import date as lafecha


def all_turns(helpcenter_id, date):
    return jsonify(all_turns2(helpcenter_id, date))


def all_turns2(helpcenter_id, date):

    centro = HelpCenter.find(helpcenter_id)
    if (not centro):
        return redirect(url_for("home"))
    dateA = str(date)
    dateAux = lafecha(int(dateA[0:4]), int(dateA[4:6]), int(dateA[6:8]))
    if (dateAux < lafecha.today()):
        return abort(404)
    bt = str(centro.opening_time)
    et = str(centro.closing_time)
    if dateAux == lafecha.today():
        hourAux = datetime.now().hour if datetime.now(
        ).minute <= 30 else (datetime.now().hour + 1)
        minAux = 0 if datetime.now().minute >= 30 else 30
    else:
        hourAux = int(bt[0:2])
        minAux = int(bt[3:5])
    times = []
    i = 1
    while hourAux < int(et[0:2]):
        times.append(time(hour=hourAux, minute=minAux))
        hourAux = hourAux+1 if minAux == 30 else hourAux
        minAux = 0 if (minAux == 30) else 30
        i += 1
    takenTurns = Turn.horas_ocupadas(centro.id, date)
    for turns in takenTurns:
        hour = str(turns)[0:2]
        minu = str(turns)[3:5]
        tt = time(hour=int(hour), minute=int(minu))
        if tt in times:
            times.remove(tt)
    arr = []
    for t in times:
        arr.append(str(t))
    return arr

def all_turns3(helpcenter_id, date):

    centro = HelpCenter.find(helpcenter_id)
    if (not centro):
        return redirect(url_for("home"))
    dateA = str(date)
    dateAux = lafecha(int(dateA[0:4]), int(dateA[4:6]), int(dateA[6:8]))
    if (dateAux < lafecha.today()):
        return abort(404)
    bt = str(centro.opening_time)
    et = str(centro.closing_time)
    if dateAux == lafecha.today():
        hourAux = datetime.now().hour if datetime.now(
        ).minute <= 30 else (datetime.now().hour + 1)
        minAux = 0 if datetime.now().minute >= 30 else 30
    else:
        hourAux = int(bt[0:2])
        minAux = int(bt[3:5])
    times = []
    i = 1
    while hourAux < int(et[0:2]):
        times.append(time(hour=hourAux, minute=minAux))
        hourAux = hourAux+1 if minAux == 30 else hourAux
        minAux = 0 if (minAux == 30) else 30
        i += 1
    takenTurns = Turn.horas_ocupadas(centro.id, date)
    for turns in takenTurns:
        hour = str(turns)[0:2]
        minu = str(turns)[3:5]
        tt = time(hour=int(hour), minute=int(minu))
        if tt in times:
            times.remove(tt)
    arr = []
    for t in times:
        arr.append(str(t))
    return arr
