from flask import request, render_template, flash, g, session, redirect, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user
from werkzeug import check_password_hash, generate_password_hash
from orvsd_central import db, app
from forms import LoginForm, AddDistrict, AddSchool, AddUser
from models import District, School, Site, SiteDetail, Course, CourseDetail, User
import re

@app.route("/")
#@login_required
def main_page():
    return redirect('/report')

@app.route("/add_district", methods=['GET', 'POST'])
def add_district():
    form = AddDistrict()
    if request.method == "POST":
        #Add district to db.
        db.session.add(District(form.name.data, form.shortname.data,
                        form.base_path.data))
        db.session.commit()

    return render_template('add_district.html', form=form)

#@login_required
@app.route("/add_school", methods=['GET', 'POST'])
def add_school():
    form = AddSchool()
    error_msg = ""

    if request.method == "POST":
        #The district_id is supposed to be an integer
        #try:
            #district = District.query.filter_by(id=int(form.district_id)).all()
            #if len(district) == 1:
                #Add School to db
        db.session.add(School(int(form.district_id.data),
                        form.name.data, form.shortname.data,
                        form.domain.data. form.license.data))
        db.session.commit()
            #else:
            #    error_msg= "A district with that id doesn't exist!"
        #except:
        #    error_msg= "The entered district_id was not an integer!"
    return render_template('add_school.html', form=form,
                        error_msg=error_msg)


@app.route('/me')
@login_required
def home():
    """
    Loads a users home information page
    """
    return render_template('users/templates/profile.html', user=current_user) #not sure current_user works this way, write test

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Successful Login!")
            return redirect("/users/me/")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route("/report", methods=['GET', 'POST'])
#@login_required
def report():

    all_districts = District.query.order_by("name").all()

    if request.method == "GET":
        dist_count = District.query.count()
        school_count = School.query.count()
        course_count = Course.query.count()
        site_count = SiteDetail.query.count()


        return render_template("report_overview.html", dist_count=dist_count,
                                                       school_count=school_count,
                                                       course_count=course_count,
                                                       site_count=site_count,
                                                       all_districts=all_districts)

    elif request.method == "POST":
        all_schools = School.query.order_by("name").all()
        all_courses = Course.query.order_by("name").all()
        all_sites = SiteDetail.query.all()



#    for item in all_sites:
#        print item
#
#    districts = all_districts
#    schools = all_schools
#    courses = all_courses
#
#    # Once filters have been applied
#    if request.method== "POST":
#        form = request.form
#        # Check to see if the user wants to see district info
#        if request.form['all_districts'] != "None":
#        # Getting district related information
#            if request.form['all_districts'] != "All":
#                districts = District.query.filter_by(name=request.form['filter_districts'])
#            for district in districts:
#                district.schools = School.query.filter_by(disctrict_id=district.id).order_by("name").all()
#                for school in district.schools:
#                    school.sites = Site.query.filter_by(school_id=school.id).order_by("name").all()
#                    for site in sites:
#                        related_courses = Session.execute("select course_id where site_id="+sites.id+" from sites_courses")
#                        site.courses = []
#                        site.courses.append(Course.query.get(course))
#
#            districts = None
#            # Check to see if the user wanted school information
#            if request.form['all_schools'] != "None":
#                if request.form['all_schools'] != "All":
#                    schools = School.query.filter_by(name=request.form['filter_schools']).order_by("name").all()
#                for school in schools:
#                    school.sites = Site.query.filter_by(school_id=school.id).order_by("name").all()
#                    for site in sites:
#                        related_courses = Session.execute("select course_id where site_id="+sites.id+" from sites_courses")
#                        for course in related_courses:
#                            # course is the primary key which is used to relate a site's course to a specific course.
#                            site.courses.append(Course.query.get(course))
#                        for course in site.courses:
#                            # Parse information from SiteDetails
#                            continue
#
#            else:
#                schools = None
#                # Check to see if the user wanted course information
#                if request.form['all_courses'] != "None":
#                    if request.form['all_courses'] != "All":
#                        courses = Course.query.filter_by(name=request.form['filter_courses']).order_by("name").all()
#                    for course in courses:
#                        #Calculate num of users in total
#                        continue
#                else:
#                    return "Error: No filter provided!!"
#    else:
#        districts = all_districts
#        schools = all_schools
#        courses = all_courses
#
        return render_template("report.html", all_districts=all_districts,
                                             all_schools=all_schools,
                                             all_courses=all_courses,
                                             all_sites=all_sites)

@app.route("/add_user", methods=['GET', 'POST'])
#@login_required
def register():
    form = AddUser()
    message = ""

    if request.method == "POST":
        if form.password.data != form.confirm_pass.data:
            message="The passwords provided did not match!\n"
        elif not re.match('^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', form.email.data):
            message="Invalid email address!\n"
        else:
            #Add user to db
            db.session.add(User(name=form.user.data,
                email = form.email.data, password=form.password.data))

            message = form.user.data+" has been added successfully!\n"

    return render_template('add_user.html', form=form, message=message)

@app.route("/display/<category>")
def remove(category):
    obj = get_obj_by_category(category)
    objects = obj.query.all()
    if objects:
        # fancy way to get the properties of an object
        properties = objects[0].get_properties()
        return render_template('removal.html', category=category, objects=objects, properties=properties)


@app.route("/remove/<category>", methods=['POST'])
def remove_objects(category):
    obj = get_obj_by_category(category)
    remove_ids = request.form.getlist('remove')
    for remove_id in remove_ids:
        # obj.query returns a list, but should only have one element because
        # ids are unique.
        remove = obj.query.filter_by(id=remove_id)[0]
        db.session.delete(remove)

    db.session.commit()

    return redirect('display/'+category)

def get_obj_by_category(category):
    if category == "District":
        return District
    elif category == "School":
        return School
    elif category == "Site":
        return Site
    elif category == "Course":
        return Course
    else:
        raise Exception('Invalid category: '+category)



