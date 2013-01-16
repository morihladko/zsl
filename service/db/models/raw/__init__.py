#autogenerated by sqlautocode

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.engine
from application import service_application
import db.models.app
from sqlalchemy.orm import relation, backref, relationship
from sqlalchemy.dialects.mysql.base import BIT
from db.models.raw.model_helper import ModelHelper

if not service_application.is_initialized():
    print "Application is not initialized."
    quit()

DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = service_application.get_injector().get(sqlalchemy.engine.Engine)

class ModelBase:
    def update(self, app_model, forbidden_keys = [], inverse = False):
        ModelHelper.update_model(self, app_model, forbidden_keys, inverse)

class Sport(DeclarativeBase, ModelBase):
    __tablename__ = 'sport'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)

    #relation definitions

    def get_app_model(self):
        return db.models.app.Sport(self.__dict__)


class SportClub(DeclarativeBase, ModelBase):
    __tablename__ = "sport_club"

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    magazine_id = Column(u'magazine_id', INTEGER(), nullable=False)
    name = Column(u'name', VARCHAR(length=255), nullable=False)
    url = Column(u'url', VARCHAR(length=255), nullable=False)
    regexp = Column(u'regexp', TEXT())
    added = Column(u'added', DATETIME(), nullable=False)
    created = Column(u'created', DATETIME())
    flag_created_year = Column(u'flag_created_year', BIT(), nullable=False)
    sport_id = Column(u'sport_id', INTEGER(), ForeignKey('sport.id'))
    stadium = Column(u'stadium', VARCHAR(length=255), nullable=False)
    president = Column(u'president', VARCHAR(length=255), nullable=False)
    coach = Column(u'coach', VARCHAR(length=255), nullable=False)
    league = Column(u'league', VARCHAR(length=255), nullable=False)
    state_id = Column(u'state_id', INTEGER(), ForeignKey('state.id'))
    city = Column(u'city', VARCHAR(length=255), nullable=False)
    achievements = Column(u'achievements', TEXT())
    homepage = Column(u'homepage', VARCHAR(length=255), nullable=False)
    active = Column(u'active', BIT(), nullable=False)
    current_squad = Column(u'current_squad', BIT(), nullable=False)

    #relation definitions
    sport = relation('Sport', primaryjoin='SportClub.sport_id==Sport.id')
    state = relation('State', primaryjoin='SportClub.state_id==State.id')
    sport_club_fields = relationship("SportClubField", order_by="SportClubField.id", backref="sport_club")


    def get_app_model(self):
        m = db.models.app.SportClub(self.__dict__)
        if self.created != None:
            m.created = '{0.day:{1}}. {0.month:{1}}. {0.year}'.format(self.created, '02');
        else:
            m.presentation_created = None

        if self.created != None and self.flag_created_year:
            m.presentation_created = '{0.year}'.format(self.created)
        else:
            m.presentation_created = m.created

        m.sport_club_fields = []
        if self.sport_club_fields != None:
            for scf in self.sport_club_fields:
                m.sport_club_fields.append(scf.get_app_model())

        return m

    def update_url(self):
        self.url = "/sportove-kluby/{0}/{1}".format(self.id, self.name)

class SportClubField(DeclarativeBase, ModelBase):
    __tablename__ = 'sport_club_field'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    name = Column(u'name', VARCHAR(length=256), nullable=False)
    sport_club_id = Column(u'sport_club_id', INTEGER(), ForeignKey('sport_club.id'), nullable=False)
    value = Column(u'value', VARCHAR(length=256), nullable=False)

    #relation definitions
    #sport_club = relationship("SportClub", backref=backref('sport_club_fields', order_by=id))

    def get_app_model(self):
        return db.models.app.SportClubField(self.__dict__)

class State(DeclarativeBase, ModelBase):
    __tablename__ = 'state'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False)
    name_en = Column(u'name_en', VARCHAR(length=64), nullable=False)
    name_sk = Column(u'name_sk', VARCHAR(length=64), nullable=False)

    #relation definitions

    def get_app_model(self):
        return db.models.app.State(self.__dict__)
