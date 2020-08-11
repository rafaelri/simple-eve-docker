import os
from eve import Eve
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property, relationship

from eve_sqlalchemy import SQL
from eve_sqlalchemy.config import DomainConfig, ResourceConfig
from eve_sqlalchemy.validation import ValidatorSQL

Base = declarative_base()

class CommonColumns(Base):
    __abstract__ = True
    _created = Column(DateTime, default=func.now())
    _updated = Column(DateTime, default=func.now(), onupdate=func.now())
    _etag = Column(String(40))


class People(CommonColumns):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(80))
    lastname = Column(String(120))
    fullname = column_property(firstname + " " + lastname)


class Invoices(CommonColumns):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer)
    people_id = Column(Integer, ForeignKey('people.id'))
    people = relationship(People, uselist=False)



SETTINGS = {
    'DEBUG': False,
    'SQLALCHEMY_DATABASE_URI': os.environ.get('DB_URL') or 'sqlite:////tmp/teste.db',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'DOMAIN': DomainConfig({
        'people': ResourceConfig(People)
    }).render(),
    'RESOURCE_METHODS' : ['GET', 'POST', 'DELETE']
}

app = Eve(auth=None, settings=SETTINGS, validator=ValidatorSQL, data=SQL)

db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()

if not db.session.query(People).count():
    db.session.add_all([
        People(firstname=u'George', lastname=u'Washington'),
        People(firstname=u'John', lastname=u'Adams'),
        People(firstname=u'Thomas', lastname=u'Jefferson')])
    db.session.commit()

app.run(host= '0.0.0.0')