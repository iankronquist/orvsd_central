from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
course_details = Table('course_details', post_meta,
    Column('course_id', Integer, primary_key=True, nullable=False),
    Column('shortname', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('filename', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('version', Float(precision=None, asdecimal=False)),
    Column('updated', DateTime(timezone=False)),
    Column('active', Boolean(create_constraint=True, name=None)),
    Column('moodle_version', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('source', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
)

courses = Table('courses', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('serial', Integer),
    Column('name', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('shortname', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('license', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('category', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
)

districts = Table('districts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('shortname', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('base_path', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
)

moodle_plugin_types = Table('moodle_plugin_types', post_meta,
    Column('tid', Integer, primary_key=True, nullable=False),
    Column('ptype', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
)

moodleplugins = Table('moodleplugins', post_meta,
    Column('plugin_id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('shortname', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('version', Float(precision=None, asdecimal=False)),
    Column('ptypeid', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
)

schools = Table('schools', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('district_id', Integer),
    Column('name', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('shortname', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('domain', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('license', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
)

site_details = Table('site_details', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('site_id', Integer),
    Column('siteversion', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('siterelease', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('adminemail', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('totalusers', Integer),
    Column('adminusers', Integer),
    Column('teachers', Integer),
    Column('activeusers', Integer),
    Column('totalcourses', Integer),
    Column('timemodified', DateTime(timezone=False)),
)

sites = Table('sites', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('school_id', Integer),
    Column('sitename', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('sitetype', Enum),
    Column('baseurl', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('basepath', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('jenkins_cron_job', DateTime(timezone=False)),
    Column('location', String(length=255, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
)

sites_courses = Table('sites_courses', post_meta,
    Column('site_id', Integer),
    Column('course_id', Integer),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('email', String(length=120, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('password', String(length=20, convert_unicode=False, assert_unicode=None, unicode_error=None, _warn_on_bytestring=False)),
    Column('role', SmallInteger, default=ColumnDefault(1)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['course_details'].create()
    post_meta.tables['courses'].create()
    post_meta.tables['districts'].create()
    post_meta.tables['moodle_plugin_types'].create()
    post_meta.tables['moodleplugins'].create()
    post_meta.tables['schools'].create()
    post_meta.tables['site_details'].create()
    post_meta.tables['sites'].create()
    post_meta.tables['sites_courses'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['course_details'].drop()
    post_meta.tables['courses'].drop()
    post_meta.tables['districts'].drop()
    post_meta.tables['moodle_plugin_types'].drop()
    post_meta.tables['moodleplugins'].drop()
    post_meta.tables['schools'].drop()
    post_meta.tables['site_details'].drop()
    post_meta.tables['sites'].drop()
    post_meta.tables['sites_courses'].drop()
    post_meta.tables['users'].drop()
