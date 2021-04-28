from app.db import db

class Configuration(db.Model):
    __tablename__="configuration"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    elementsPerPage = db.Column(db.Integer, nullable=False)
    habilitate = db.Column(db.Boolean, nullable=False)

    def __init__ (self, title, description, email, elementsPerPage, habilitate):
        self.title=title
        self.description=description
        self.email=email
        self.elementsPerPage=elementsPerPage
        self.habilitate=habilitate
    
    @classmethod
    def all(cls):
        con=Configuration.query.all()
        return con

    @classmethod
    def last(cls):
        con=Configuration.query.all()
        if con:
            return con[len(con)-1]
        else:
            config= Configuration(
            title='default',
            description='default',
            email='aMail@mail.com',
            elementsPerPage=10,
            habilitate=True
            )
            db.session.add(config)
            db.session.commit()
            return config

    @classmethod
    def create(cls, form):
        config= Configuration(
            title=form.title.data,
            description=form.description.data,
            email=form.email.data,
            elementsPerPage=form.elementsPerPage.data,
            habilitate=form.habilitate.data
        )
        db.session.add(config)
        db.session.commit()

        return config