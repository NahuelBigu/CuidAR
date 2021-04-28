from app.db import db
from datetime import date, datetime, timedelta, time
from app.models.helpcenter import HelpCenter
from sqlalchemy import func
turn_helpcenter = db.Table('turn_helpcenter',
                           db.Column('helpcenter_id', db.Integer, db.ForeignKey(
                               'helpcenter.id'), primary_key=True),
                           db.Column('turn_id', db.Integer, db.ForeignKey(
                               'turn.id'), primary_key=True)
                           )


class Turn(db.Model):
    __tablename__ = 'turn'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(255), nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
    nombre = db.Column(db.String(255))
    apellido = db.Column(db.String(255))
    date = db.Column(db.DateTime, nullable=False)
    phone = db.Column(db.String(255))
    helpcenter = db.relationship('HelpCenter', secondary=turn_helpcenter,
                                 lazy='subquery', backref=db.backref('turn', lazy=True,uselist=False))

    def __init__(self, opening_time, date, user, phone, nombre, apellido):
        self.user = user
        self.opening_time = opening_time
        if int(opening_time[3:4]) == 0:
            self.closing_time = time(hour=int(opening_time[0:2]), minute=30)
        else:
            self.closing_time = time(hour=int(opening_time[0:2])+1, minute=0)
        self.date = date
        self.phone = phone
        if nombre != "":
            self.nombre = nombre
        if apellido != "":
            self.apellido = apellido

    def __getitem__(self, field):
        return self.__dict__[field]

    @ classmethod
    def all(cls):
        turns = Turn.query.all()
        return turns

    @ classmethod
    def index(cls, center):
        ret = []
        end_date = datetime.now() + timedelta(days=2)
        end_date = end_date.date()
        turns = Turn.query.all()
        for t in turns:
            if date.today() <= t.date.date() and t.date.date() <= end_date:
                t.date = t.date.date()
                for h in t.helpcenter:
                    if h.id == center:
                        ret.append(t)
        ret = sorted(ret, key=lambda x: (x.date, x.opening_time))
        return ret

    @ classmethod
    def find(cls, turn_id):
        t = Turn.query.get(turn_id)
        if not t.helpcenter[0].accept:
            return None
        return t

    @ classmethod
    def findByDateAndCenter(cls, dateIn, turn_id):
        turn = Turn.query.filter_by(date=dateIn, id=turn_id).all()
        return turn

    @ classmethod
    def create(cls, form):

        turn = Turn(form.opening_time.data,
                    form.date.data,
                    form.user.data,
                    form.phone.data,
                    form.nombre.data,
                    form.apellido.data)

        turn.helpcenter.append(HelpCenter.find(form.helpcenter_id.data))

        db.session.add(turn)
        db.session.commit()

    @classmethod
    def apiCreate(cls, form):
        turn = Turn(form.hora_inicio.data,
                    form.fecha.data,
                    form.email_donante.data,
                    form.telefono_donante.data,
                    form.nombre.data,
                    form.apellido.data)

        turn.helpcenter.append(HelpCenter.find(form.centro_id.data))

        db.session.add(turn)
        db.session.commit()
        return turn

    @ classmethod
    def edit(cls, form, id_turn):
        t = cls.find(id_turn)
        t.opening_time = form.opening_time.data
        if int(t.opening_time[3:4]) == 0:
            t.closing_time = time(hour=int(t.opening_time[0:2]), minute=30)
        else:
            t.closing_time = time(hour=int(t.opening_time[0:2])+1, minute=0)
        t.date = form.date.data
        t.user = form.user.data
        t.phone = form.phone.data
        t.nombre = form.nombre.data
        t.apellido = form.apellido.data
        db.session.commit()
        return t

    @ classmethod
    def horas_ocupadas(cls, helpcenter_id, turn_date):
        turns = Turn.query.filter_by(date=turn_date).all()
        ret = []
        for t in turns:
            if len(t.helpcenter) > 0:
                if t.helpcenter[0].id == helpcenter_id:
                    ret.append(t.opening_time)
        return ret

    @ classmethod
    def delete(cls, turn_id):
        t = cls.find(turn_id)
        if t is None:
            return None
        db.session.delete(t)
        db.session.commit()
        return t

    @classmethod
    def cantTurnsInRange(cls,fechaInicio,fechaFin):
        turnosAux = Turn.query.filter(Turn.date.between(fechaInicio,fechaFin)).all()
        aux={}
        for t in turnosAux:
            aux2={}
            aux2["Fecha"]=str(t.date)
            for h in t.helpcenter:
                aux2["Municipio"]=str(h.municipio)
            aux[str(t.id)]=aux2
        return aux

    @classmethod
    def agrupados(cls):
        aux={}
        todos=Turn.query.all()
        for t in todos:
            for h in t.helpcenter:
                if (not h.name in aux.keys()):
                    aux[h.name]=0
                aux[h.name]+=1
        return aux