from app.db import db
from app.models.typecenter import TypeCenter
import os
helpcenter_typecenter = db.Table('helpcenter_typecenter',
                                 db.Column('helpcenter_id', db.Integer, db.ForeignKey(
                                     'helpcenter.id'), primary_key=True),
                                 db.Column('typecenter_id', db.Integer, db.ForeignKey(
                                     'typecenter.id'), primary_key=True)
                                 )


class HelpCenter(db.Model):
    __tablename__ = 'helpcenter'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
    type_center = db.relationship('TypeCenter', secondary=helpcenter_typecenter,
                                  lazy='subquery', backref=db.backref('helpcenter', lazy=True))
    # uno a muchos db.Column(db.Integer, db.ForeignKey('helpcenter.id'))
    # muchos a muchos db.relationship('TypeCenter', secondary=helpcenter_typecenter ,lazy='subquery', backref=db.backref('helpcenter', lazy=True))
    municipio = db.Column(db.Integer, nullable=False)
    web = db.Column(db.String(255))
    email = db.Column(db.String(255))
    status = db.Column(db.Boolean)
    accept = db.Column(db.Boolean, nullable=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    view_protocol= db.Column(db.String(255),nullable=True) 

    def __init__ (self,name,address,phone,opening_time,closing_time,municipio,web,email,latitude,longitude):
        self.name=name
        self.address=address
        self.phone=phone
        self.opening_time=opening_time
        self.closing_time=closing_time
        self.municipio=municipio
        self.web=web
        self.email=email
        self.status=False
        self.accept=None
        self.latitude=latitude
        self.longitude=longitude
        
    
    def __getitem__(self, field):
        return self.__dict__[field]

   
    def addFileName(self,filename):
        self.view_protocol =filename
        db.session.commit()
        return self

    @classmethod
    def all(cls):
        helpcenters = HelpCenter.query.all()
        return helpcenters

    @classmethod
    def allAccepted(cls, page, ele):
        helpcenters = HelpCenter.query.filter_by(accept=True, status=True).paginate(page, per_page=ele)
        return helpcenters.items

    @classmethod
    def isAccepted(cls, idcentro):
        acceptedCenters= HelpCenter.query.filter_by(accept=True, status=True).all()
        ids=[]
        for i in acceptedCenters:
            ids.append(i.id)
        #print(ids)
        #print(idcentro in ids)
        return idcentro in ids

    @classmethod
    def cant(cls):
        cantidad = HelpCenter.query.filter_by(accept=True, status=True).count()
        return cantidad

    @classmethod
    def find(cls, helpcenter_id):
        helpcenter = HelpCenter.query.get(helpcenter_id)
        return helpcenter

    @classmethod
    def create(cls, form):
        helpcenter = HelpCenter(form.name.data,
                                form.address.data,
                                form.phone.data,
                                form.opening_time.data,
                                form.closing_time.data,
                                form.municipio.data,
                                form.web.data,
                                form.email.data,
                                form.latitude.data,
                                form.longitude.data
                                )
        type_centerData = form.type_center.data
        typecenter = TypeCenter.query.filter(
            TypeCenter.id.in_(type_centerData)).all()
        helpcenter.type_center = typecenter
        db.session.add(helpcenter)
        db.session.commit()
        return helpcenter

    @classmethod
    def accepted(cls, helpcenter_id):
        helpcenter = HelpCenter.find(helpcenter_id)
        if helpcenter == None:
            return None
        helpcenter.accept = True
        db.session.commit()
        return helpcenter

    @classmethod
    def reject(cls, helpcenter_id):
        helpcenter = HelpCenter.find(helpcenter_id)
        if helpcenter == None:
            return None
        helpcenter.accept = False
        db.session.commit()
        return helpcenter

    @classmethod
    def publish(cls, helpcenter_id):
        helpcenter = HelpCenter.find(helpcenter_id)
        if helpcenter == None:
            return None
        helpcenter.status = True
        db.session.commit()
        return helpcenter

    @classmethod
    def unpublish(cls, helpcenter_id):
        helpcenter = HelpCenter.find(helpcenter_id)
        if helpcenter == None:
            return None
        helpcenter.status = False
        db.session.commit()
        return helpcenter

    @classmethod
    def delete(cls, helpcenter_id):
        helpcenter = HelpCenter.find(helpcenter_id)
        if helpcenter is None:
            return None
        if (helpcenter.view_protocol != None):
            os.remove('app/static/uploads/'+ helpcenter.view_protocol)  
        db.session.delete(helpcenter)
        db.session.commit()
        return helpcenter

    @classmethod
    def edit(cls,form):
        h=HelpCenter.find(form.helpcenter_id.data)        
        type_centerData=form.type_center.data
        typecenter=TypeCenter.query.filter(TypeCenter.id.in_(type_centerData)).all()
        h.type_center=typecenter
        h.name=form.name.data
        h.address=form.address.data
        h.phone=form.phone.data
        h.opening_time=form.opening_time.data
        h.closing_time=form.closing_time.data
        h.municipio=form.municipio.data
        h.web=form.web.data
        h.email=form.email.data      
        h.latitude=form.latitude.data 
        h.longitude=form.longitude.data 
        db.session.commit()
        return h

    def check_status(self):
        return self.status

    def check_accepted(self):
        return self.accept
