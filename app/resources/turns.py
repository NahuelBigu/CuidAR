from flask import redirect, render_template, request, url_for, session, abort, flash
from app.models.turn import Turn
from app.models.configuration import Configuration
from app.helpers.control_decorator import control
from app.helpers.permission import check as has_permission
from app.helpers.turn import all_turns2
from app.models.forms.turn import TurnNewForm
from datetime import date, datetime, timedelta, time
from app.models.helpcenter import HelpCenter
from flask.json import jsonify

# Protected resources


@control
def indexApi(centro, date):
    if not has_permission(session, "turn_index"):  # Check permission
        return redirect(url_for("home"))

    centro = HelpCenter.find(centro)
    bt = str(centro.opening_time)
    et = str(centro.closing_time)
    hourAux = int(bt[0:2])
    minAux = int(bt[3:5])
    times = []
    while hourAux < int(et[0:2]):
        times.append(time(hour=hourAux, minute=minAux))
        hourAux = hourAux+1 if minAux == 30 else hourAux
        minAux = 0 if (minAux == 30) else 30
    takenTurns = Turn.horas_ocupadas(centro.id, date)
    for turns in takenTurns:
        hour = str(turns)[0:2]
        minu = str(turns)[3:5]
        tt = time(hour=int(hour), minute=int(minu))
        if tt in times:
            times.remove(tt)
    print(times)
    return str(times)


@control
def indexTodayApi(centro):
    if not has_permission(session, "turn_index"):  # Check permission
        return redirect(url_for("home"))

    turns = Turn.findByDateAndCenter(date.today(), centro)
    return render_template("turns/index.html", turns=turns)


@control
def index(centro):
    if not has_permission(session, "turn_index"):  # Check permission
        return redirect(url_for("home"))
    hc=HelpCenter.find(centro)
    if hc == None:
        return render_template("error.html"), 404
    turns = Turn.index(centro)

    elementsPerPage = Configuration.last().elementsPerPage

    return render_template("turns/index.html", turns=turns, elementsPerPage=elementsPerPage,estado=hc.status, center=centro)


@control
def new(helpcenter_id):
    if not has_permission(session, "turn_index"):  # Check permission
        return redirect(url_for("home"))
    hc = HelpCenter.find(helpcenter_id)
    if hc == None:
        return render_template("error.html"), 404
    if hc.accept != True or hc.status == False:
        return render_template("error.html"), 401
    centro = HelpCenter.find(helpcenter_id)

    form = TurnNewForm()
    form.helpcenter_id.data = helpcenter_id
    form.date.data = form.date.data if form.date.data != None else date.today()
    turnos = all_turns2(helpcenter_id, (str(form.date.data).replace('-', '')))
    form.opening_time.choices = [(str(t), str(t))for t in turnos]

    if form.validate_on_submit():
        turn = Turn.create(form)
        flash("Se creo el turno!", category="success")
        return redirect(url_for("turns_index", centro=helpcenter_id))

    return render_template("turns/new.html", form=form, helpcenter_id=helpcenter_id)


@control
def edit(turn_id):
    if not has_permission(session, "turn_update"):  # Check permission
        return redirect(url_for("home"))
    tur = Turn.find(turn_id)
    centro = tur.helpcenter[0]
    if centro.accept != True or centro.status == False:
        return render_template("error.html"), 401
    aux = Turn.find(turn_id)
    form = TurnNewForm()
    form.helpcenter_id.data = centro.id
    form.date.data = aux.date if request.method == 'GET' else form.date.data
    turnos = all_turns2(form.helpcenter_id.data,
                        (str(form.date.data).replace('-', '')))
    form.opening_time.choices = [(str(t), str(t))for t in turnos]
    form.opening_time.choices.append(
        (str(aux.opening_time), str(aux.opening_time)))

    turnos = all_turns2(centro.id, (str(form.date.data).replace('-', '')))

    if form.validate_on_submit():
        turn = Turn.edit(form, turn_id)
        flash("Se edito el turno!", category="success")
        return redirect(url_for("turns_index", centro=aux.helpcenter[0].id))
    form.user.data = aux.user
    form.phone.data = aux.phone
    f = str(aux.date.year)+str(aux.date.month)+str(aux.date.day)

    return render_template("turns/edit.html", form=form, turn_id=turn_id, center=aux.helpcenter[0].id, fecha=f, h=aux.opening_time)


@ control
def delete(turn_id):
    if not has_permission(session, "turn_delete"):  # Check permission
        return redirect(url_for("home"))
    aux = Turn.find(turn_id)
    if aux == None:
        return render_template("error.html"), 404
    aux = aux.helpcenter[0].id
    Turn.delete(turn_id)
    flash('Turno eliminado correctamente', category="success")
    return redirect(url_for("turns_index", centro=aux))

def api_fechas_turnos():
    
    fechaInicio = request.args.get("fechaIni")
    fechaFin = request.args.get("fechaFin")
    if(not fechaInicio or not fechaFin):
        return jsonify({})
    aux=Turn.cantTurnsInRange(fechaInicio,fechaFin)
    return jsonify(aux)

def api_centro_turnos():
    aux=Turn.agrupados()
    return jsonify(aux)
