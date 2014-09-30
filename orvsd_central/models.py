import hashlib
import time

from sqlalchemy import (Boolean, Column, DateTime, Enum, Float, ForeignKey,
                        Integer, SmallInteger, String, Text, Table)
from sqlalchemy.orm import backref, relationship
from werkzeug.security import generate_password_hash, check_password_hash

from orvsd_central.database import Model

# A representation of the connection between the courses each site has
# installed, and information about those course details.
sites_courses = Table('sites_courses',
                      Model.metadata,
                      Column('site_id',
                             Integer,
                             ForeignKey(
                                 'sites.id',
                                 use_alter=True,
                                 name='fk_sites_courses_site_id')
                             ),
                      Column('course_id',
                             Integer,
                             ForeignKey(
                                 'courses.id',
                                 use_alter=True,
                                 name='fk_sites_courses_course_id')
                             ),
                      Column('celery_task_id',
                             String(255),
                             ForeignKey(
                                 'celery_taskmeta.task_id',
                                 use_alter=True,
                                 name='fk_sites_courses_celery_task_id')
                             ),
                      Column('students', Integer))


class User(Model):
    """
    A Model representation of your average User.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120))
    password = Column(String(768))
    # 1 = Standard User
    # 2 = Helpdesk
    # 3 = Admin
    role = Column(SmallInteger, default=1)
    # Possibly another column for current status

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password=password,
                                               method='pbkdf2:sha512',
                                               salt_length=128)
        self.role = role

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.name)

    def serialize(self):
        return {'id': self.id,
                'name': self.name,
                'email': self.email,
                # Don't reveal passwords
                'password': '********',
                'role': self.role}


class District(Model):
    """
    A Model representation of a District.
    * Districts have many schools.
    """
    __tablename__ = 'districts'

    id = Column(Integer, primary_key=True)
    # State given ID number
    state_id = Column(Integer)
    # Full name of the district
    name = Column(String(255))
    # short name/abbreviation
    shortname = Column(String(255))
    # root path in which school sites are stored - maybe redundant
    base_path = Column(String(255))

    def __repr__(self):
        return "<Disctrict('%s')>" % (self.name)

    def get_properties(self):
        return ['id', 'state_id', 'name', 'shortname', 'base_path']

    def serialize(self):
        return {'id': self.id,
                'state_id': self.state_id,
                'name': self.name,
                'shortname': self.shortname,
                'base_path': self.base_path}


class School(Model):
    """
    A Model representation of a School.
    * Schools belong to one district, may have many sites and courses.
    """
    __tablename__ = 'schools'

    id = Column(Integer, primary_key=True)
    # points to the owning district
    district_id = Column(Integer,
                         ForeignKey('districts.id',
                                    use_alter=True,
                                    name='fk_school_to_district_id'))
    # state assigned id
    state_id = Column(Integer)
    # school name
    name = Column(String(255))
    # short name or abbreviation
    shortname = Column(String(255))
    # the base domain name for this school's sites (possibly redundant)
    domain = Column(String(255))
    # list of tokens indicating licenses for some courses - courses with
    # license tokens in this list can be installed in this school
    license = Column(String(255))
    county = Column(String(255))

    district = relationship("District",
                            backref=backref('schools', order_by=id))

    def get_properties(self):
        return ['id', 'disctrict_id', 'name', 'shortname', 'domain', 'license',
                'county']

    def serialize(self):
        return {'id': self.id,
                'district_id': self.district_id,
                'state_id': self.state_id,
                'name': self.name,
                'shortname': self.shortname,
                'domain': self.domain,
                'license': self.license,
                'county': self.county}


class Site(Model):
    """
    A Model respresentation of a Site.
    * Sites belong to one school, and may have many SiteDetails.
    """
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True)
    # points to the owning school
    school_id = Column(Integer, ForeignKey('schools.id',
                                           use_alter=True,
                                           name="fk_sites_school_id"))
    # name of the site - (from siteinfo)
    name = Column(String(255))
    # Dev site?
    dev = Column(Boolean, default=False)
    # (from siteinfo)
    sitetype = Column(Enum('moodle', 'drupal', name='site_types'))
    # moodle or drupal's base_url - (from siteinfo)
    baseurl = Column(String(255))
    # site's path on disk - (from siteinfo)
    basepath = Column(String(255))
    # is there a jenkins cron job? If so, when did it last run?
    jenkins_cron_job = Column(DateTime)
    # what machine is this on, or is it in the moodle cloud?
    location = Column(String(255))
    api_key = Column(String(40))

    site_details = relationship("SiteDetail", backref=backref('sites'))
    courses = relationship("Course",
                           secondary='sites_courses',
                           backref='sites')

    def generate_new_key(self):
        self.api_key = hashlib.sha1(str(round(time.time() * 1000))).hexdigest()

    def __repr__(self):
        return "<Site('%s','%s','%s','%s','%s','%s','%s')>" % \
               (self.name, self.school_id, self.dev, self.sitetype,
                self.baseurl, self.basepath, self.jenkins_cron_job)

    def get_properties(self):
        return ['id', 'school_id', 'name', 'sitetype',
                'baseurl', 'basepath', 'jenkins_cron_job', 'location']

    def serialize(self):
        return {'id': self.id,
                'school_id': self.school_id,
                'name': self.name,
                'dev': self.dev,
                'sitetype': self.sitetype,
                'baseurl': self.baseurl,
                'basepath': self.basepath,
                'jenkins_cron_job': self.jenkins_cron_job,
                'location': self.location,
                'api_key': self.api_key}


class SiteDetail(Model):
    """
    Site_details belong to one site. This data is updated from the
    siteinfo tables, except the date - a new record is added with each
    update. See siteinfo notes.
    """
    __tablename__ = 'site_details'

    id = Column(Integer, primary_key=True)
    # points to the owning site
    site_id = Column(Integer, ForeignKey('sites.id',
                                         use_alter=True,
                                         name='fk_site_details_site_id'))
    courses = Column(Text())
    siteversion = Column(String(255))
    siterelease = Column(String(255))
    adminemail = Column(String(255))
    totalusers = Column(Integer)
    adminusers = Column(Integer)
    teachers = Column(Integer)
    activeusers = Column(Integer)
    totalcourses = Column(Integer)
    timemodified = Column(DateTime)

    def __repr__(self):
        return "<Site('%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % \
               (self.siteversion, self.siterelease, self.adminemail,
                self.totalusers, self.adminusers, self.teachers,
                self.activeusers, self.totalcourses, self.timemodified)

    def serialize(self):
        return {'id': self.id,
                'site_id': self.site_id,
                'courses': self.courses,
                'siteversion': self.siteversion,
                'siterelease': self.siterelease,
                'adminemail': self.adminemail,
                'totalusers': self.totalusers,
                'adminusers': self.adminusers,
                'teachers': self.teachers,
                'activeusers': self.activeusers,
                'totalcourses': self.totalcourses,
                'timemodified': self.timemodified}


class Course(Model):
    """
    A Model representation of a Course.
    * Courses belong to many schools
    """
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    serial = Column(Integer)
    name = Column(String(255))
    shortname = Column(String(255))
    # schools with a license token matching this can install this class
    license = Column(String(255))
    # moodle category for this class (probably "default")
    category = Column(String(255))
    source = Column(String(255))

    course_details = relationship("CourseDetail",
                                  backref=backref('course', order_by=id))

    def __repr__(self):
        return "<Site('%s','%s','%s','%s','%s','%s')>" % \
               (self.serial, self.name, self.shortname,
                self.license, self.category, self.source)

    def get_properties(self):
        return ['id', 'serial', 'name', 'shortname', 'license', 'category']

    def serialize(self):
        return {'id': self.id,
                'serial': self.serial,
                'name': self.name,
                'shortname': self.shortname,
                'license': self.license,
                'category': self.category,
                'source': self.source}


class CourseDetail(Model):
    """
    A Model representation of a Course's details.
    """
    __tablename__ = 'course_details'
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer,
                       ForeignKey('courses.id',
                                  use_alter=True,
                                  name='fk_course_details_site_id'))
    # just the name, with extension, no path
    filename = Column(String(255))
    # course version number (could be a string, ask client on format)
    version = Column(Float())
    # When the Course was last updated
    updated = Column(DateTime)
    active = Column(Boolean)
    moodle_version = Column(String(255))
    moodle_course_id = Column(Integer)

    def __repr__(self):
        return "<CourseDetail('%s','%s','%s','%s','%s','%s','%s','%s')>" % \
               (self.course_id, self.filename, self.version, self.updated,
                self.active, self.moodle_version, self.source,
                self.moodle_course_version)

    def serialize(self):
        return {'id': self.id,
                'course_id': self.course_id,
                'filename': self.filename,
                'version': self.version,
                'updated': self.updated,
                'active': self.active,
                'moodle_version': self.moodle_version,
                'moodle_course_id': self.moodle_course_id}
