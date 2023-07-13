from datetime import datetime
import random

from flask import (flash, Flask, redirect, render_template, request,
                   session, url_for)
from pymongo import MongoClient
from flask_mail import Mail


app = Flask(__name__)

# SqlAlchemy Database Configuration With Mysql
app.config.from_pyfile('config.py')

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'codescatter8980@gmail.com'
app.config['MAIL_PASSWORD'] = 'qrnvtobwftsippyd'
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

secure_type = "http"


# That is route for register page and save customer data
@app.route("/register", methods=["GET","POST"])
def register():
    """
    That function was register for new user
    """

    try:
        if request.method=="POST":
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]
            address = request.form["address"]
            username = request.form["username"]
            pwd = request.form["pwd"]
            re_pwd = request.form["re_pwd"]

            if pwd == re_pwd:

                res = find_all_cust_details()
                username_list = [data.get("username", "") for data in res]
                if username in username_list:
                    flash("Username is already availble!!!! Please try with another username....")
                    return redirect(url_for('register', _external=True, _scheme=secure_type))
                else:
                    session["username"] = username
                    created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                    new_dict = {"name":name, "email":email, "phone": int(phone), "address": address, "username": username, "password": pwd, "created_on":created_on, "updated_on":updated_on}
                    add_data = register_data(coll_name="customer_details", new_dict=new_dict)

                    flash("You are successfully register......Enjoy with that product...")
                    mail.send_message("Successfully Register",
                                      sender="harshitgadhiya8980@gmail.com",
                                      recipients = [email],
                                      body = "Hello {} \n you have successfully register!...".format(username))
                    return redirect(url_for('login', _external=True, _scheme=secure_type))
            else:
                flash("Password doesn't match!!")
                return render_template("auth/register.html")
        else:
            return render_template("auth/register.html")

    except Exception as e:
        flash("Please try again......................")
        return render_template("auth/register.html")


# That function should be login into that product
@app.route("/login", methods=["GET","POST"])
def login():
    """
    That route can use login user
    """

    try:
        if request.method=="POST":
            username = request.form["username"]
            pwd = request.form["pwd"]

            session["username"] = username
            res = find_all_cust_details()
            username_list = [[data.get("username", ""), data.get("password", "")] for data in res]
            email_list = [[data.get("email", ""), data.get("password", "")] for data in res]

            if [username,pwd] in username_list or [username,pwd] in email_list:
                session["username"] = username
                flash("Successfully Login")
                return redirect(url_for('dash_home', _external=True, _scheme=secure_type))
            else:
                flash("Your credentials doesn't match! Please enter correct Username and password...")
                return render_template("auth/login.html")
        else:
            return render_template("auth/login.html")

    except Exception as e:
        flash("Please try again..............................")
        return render_template("auth/login.html")


# That is route for sending forget mail for user
@app.route("/sending_forget_mail", methods=["GET","POST"])
def sending_forget_mail():
    """
    That function was sending forget mail while user can forget password
    """

    try:
        username = session.get("username", "")

        if request.method=="POST":
            username = request.form["username"]
            email = request.form["email"]

            res = find_all_cust_details()
            username_list = [data.get("username", "") for data in res]
            email_list = [data.get("email", "") for data in res]
            if username in username_list or username in email_list:
                flash("Pleas check your mail............")
                mail.send_message("Forget_Password",
                                  sender="harshitgadhiya8980@gmail.com",
                                  recipients=[email],
                                  body='Hello user\nChange Password\nclick that link https://codedresume.pythonanywhere.com/forget_password')

                return redirect(url_for('sending_forget_mail', _external=True, _scheme=secure_type))
            else:
                flash("That {0} is not availble First you can register!!".format(username))
                return redirect(url_for('sending_forget_mail', _external=True, _scheme=secure_type))
        else:
            return render_template("auth/sending_forget_mail.html")

    except Exception as e:
        flash("Please try again.........................")
        return render_template("auth/sending_forget_mail.html")


# That is route for otp sending mail for user
@app.route("/otp_sending", methods=["GET","POST"])
def otp_sending():
    """
    That funcation was sending a otp for user
    """

    try:
        otp = random.randint(100000, 999999)
        session["otp"] = otp
        mail.send_message("OTP Received",
                          sender="harshitgadhiya8980@gmail.com",
                          recipients=[session.get("email", "")],
                          body='Hello {0}\nYour OTP is {1}\nThis OTP is valid only 10 miniuts....'.format(session["username"], otp))

        return redirect(url_for('forget_password', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again.......................................")
        return redirect(url_for('forget_password', _external=True, _scheme=secure_type))


# That is route for otp verification and sending new_password created link
@app.route("/forget_password", methods=["GET","POST"])
def forget_password():
    """
    That funcation can use otp_verification and new_password set link generate
    """

    try:
        if request.method=="POST":
            get_otp = request.form["otp"]
            get_otp = int(get_otp)
            send_otp = session.get("otp", "")
            if get_otp == int(send_otp):
                return redirect(url_for('change_password', _external=True, _scheme=secure_type))
            else:
                flash("OTP is wrong. Please enter correct otp")
                return redirect(url_for('forget_password', _external=True, _scheme=secure_type))
        else:
            return render_template("auth/forget_password.html")

    except Exception as e:
        flash("Please try again.......................................")
        return redirect(url_for('forget_password', _external=True, _scheme=secure_type))


# That is route for new_password generation
@app.route("/change_password", methods=["GET","POST"])
def change_password():
    """
    That function was create a new password and update that data
    """
    try:
        if request.method=="POST":
            new_pwd = request.form["new_pwd"]
            re_new_pwd = request.form["re_new_pwd"]
            username = session.get("username","")
            
            if new_pwd==re_new_pwd:
                prev_data = {"username":username}
                next_data = {'$set':{"password": new_pwd}}
                update_data(coll_name="customer_details", prev_data=prev_data, update_data=next_data)
                
                flash("Record was updated..................")
                return redirect(url_for('login', _external=True, _scheme=secure_type))
            else:
                flash("Password doesn't match!!")
                return redirect(url_for('change_password', _external=True, _scheme=secure_type))
        else:
            return render_template("auth/new_password.html")

    except Exception as e:
        flash("Please try again...................")
        return redirect(url_for('change_password', _external=True, _scheme=secure_type))

# That is logout route and clear the current session
@app.route('/logout/<key>', methods=['GET', 'POST'])
def logout(key):
    """
    That funcation was logout session and clear user session
    """

    try:
        session.clear()
        if key=="user":
            # clear the session when user logout
            return redirect(url_for('login', _external=True, _scheme=secure_type))
        else:
            return redirect(url_for('admin_login', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again.......................................")
        return redirect(url_for('login', _external=True, _scheme=secure_type))

# That is home page like scrapping tool and scrape the data into given website urls
@app.route("/dash_home", methods=["GET","POST"])
def dash_home():
    """
    That function was register for new user
    """
    try:
        return render_template("home.html")

    except Exception as e:
        flash("Please try again.......................................")
        return render_template("home.html")

@app.route("/", methods=["GET","POST"])
def home():
    """
    That function was register for new user
    """
    try:
        return render_template("onepage-3.html")

    except Exception as e:
        flash("Please try again.......................................")
        return render_template("onepage-3.html")

@app.route("/home/<username>", methods=["GET","POST"])
def website(username):
    """
    That function was register for new user
    """
    try:
        # theme selected
        di = {"username": username}
        ret = find_all_specific_user(coll_name="theme_selected", di=di)
        all_theme = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2] not in all_theme:
                all_theme.append(li_list[2])

        ret = find_all_specific_user(coll_name="personal_info", di=di)
        all_personal = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_personal:
                all_personal.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="education", di=di)
        all_education = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_education:
                all_education.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="experience", di=di)
        all_experience = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_experience:
                all_experience.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="skills", di=di)
        all_skills = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_skills:
                all_skills.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="social_media_link", di=di)
        all_sm = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_sm:
                all_sm.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="projects", di=di)
        all_project = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_project:
                all_project.append(li_list[2:-2])

        if all_theme:
            temp1 = all_theme[0]
            if all_sm and all_education and all_skills and all_personal:
                data_added = session.get("data_added")
                return render_template("main_templete/{}/index.html".format(temp1), all_sm=all_sm, all_project=all_project, all_skills=all_skills, all_experience=all_experience, all_personal=all_personal, all_education=all_education)
            else:
                return render_template("main_templete/{}/index_theme.html".format(temp1))
        else:
            return render_template("sample.html")

    except Exception as e:
        print(e)
        flash("Please try again.......................................")
        return render_template("home.html")

@app.route("/theme_selection", methods=["GET","POST"])
def theme_selection():
    """
    That function was register for new user
    """
    try:
        return render_template("theme.html")

    except Exception as e:
        flash("Please try again.......................................")
        return render_template("theme.html")


@app.route("/selected_theme/<temp1>", methods=["GET","POST"])
def selected_theme(temp1):
    """
    That function was register for new user
    """
    try:
        session["templete"] = temp1
        username = session.get("username", "")
        di = {"username": username}

        ret = find_all_specific_user(coll_name="theme_selected", di=di)
        all_response = [var for var in ret]
        if all_response:
            prev = {"username": username}
            next = {'$set':{"theme": temp1}}
            msg = update_data(coll_name="theme_selected", prev_data=prev, update_data=next)
        else:
            new_dict = {"username": username, "theme": temp1}
            data = register_data(coll_name="theme_selected", new_dict=new_dict)

        return redirect(url_for('personal_info', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again.......................................")
        return render_template("theme.html")

@app.route("/experience", methods=["GET","POST"])
def experience():
    try:
        if request.method=="POST":
            college_since = request.form["since"]
            company_name = request.form["com_name"]
            experience = request.form["experience"]
            degination = request.form["degination"]
            employment_type = request.form["emp_type"]
            description = request.form["description"]

            username = session.get("username", "")
            if username:
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                new_dict = {"username":username, "college_since": college_since, "company_name": company_name, "experience": experience,
                            "degination": degination, "employment_type": employment_type,
                            "description": description, "created_on": created_on, "updated_on": updated_on}
                add_data = register_data(coll_name="experience", new_dict=new_dict)
                flash("data added succefully..................")
            else:
                flash("This user is not availble! Please first login....")
                return redirect(url_for('experience', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again......................")

    finally:
        username = session.get("username", "")
        if username:
            di = {"username": session.get("username", "")}
            ret = find_all_specific_user(coll_name="experience", di=di)
            all_response = []
            for var in ret:
                li_list = list(var.values())
                if li_list[2:-2] not in all_response:
                    all_response.append(li_list[2:-2])
            return render_template("experience.html", all_response=all_response)
        else:
            return render_template("experience.html")

@app.route("/education", methods=["GET","POST"])
def education():
    try:
        if request.method=="POST":
            college_since = request.form["since"]
            college_name = request.form["clg_name"]
            degree_name = request.form["degree_name"]
            university = request.form["university"]
            description = request.form["description"]

            username = session.get("username", "")
            if username:
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                new_dict = {"username":username, "college_since": college_since, "college_name": college_name, "degree_name": degree_name,
                            "university": university, "description": description, "created_on": created_on, "updated_on": updated_on}
                add_data = register_data(coll_name="education", new_dict=new_dict)
                flash("data added succefully..................")

            else:
                flash("This user is not availble! Please first login....")
                return redirect(url_for('education', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again......................")

    finally:
        username = session.get("username", "")
        if username:
            di = {"username": session.get("username", "")}
            ret = find_all_specific_user(coll_name="education", di=di)
            all_response = []
            for var in ret:
                li_list = list(var.values())
                if li_list[2:-2] not in all_response:
                    all_response.append(li_list[2:-2])
            return render_template("education.html", all_response=all_response)
        else:
            return render_template("education.html")

@app.route("/user_admin_panel", methods=["GET","POST"])
def user_admin_panel():
    """
    That route can show landing page while user can login
    """
    try:
        username = session.get("username", "")
        if username:
            di = {"username": username}
            ret = find_all_specific_user(coll_name="user_data", di=di)
            all_response = []
            all_keys = []
            for var in ret:
                li_list = list(var.values())
                li_list1 = list(var.keys())
                if li_list[2:-2] not in all_response:
                    all_response.append(li_list[2:-2])

                if li_list1[2:-2] not in all_keys:
                    all_keys.append(li_list1[2:-2])

            return render_template("user_admin_panel.html", all_response=all_response, all_keys=all_keys)
        else:
            return render_template("user_admin_panel.html")

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("user_admin_panel.html")


@app.route("/project", methods=["GET","POST"])
def project():
    try:
        if request.method=="POST":
            project_image_url = request.form["img_url"]
            project_name = request.form["pro_name"]
            language = request.form["language"]
            code_link = request.form["code_link"]
            description = request.form["description"]

            username = session.get("username", "")
            if username:
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                new_dict = {"username":username, "project_image_url": project_image_url, "project_name": project_name,
                            "language": language, "description":description, "code_link": code_link, "created_on": created_on, "updated_on": updated_on}
                add_data = register_data(coll_name="projects", new_dict=new_dict)
                flash("data added succefully..................")

            else:
                flash("This user is not availble! Please first login....")
                return redirect(url_for('project', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again......................")

    finally:
        username = session.get("username", "")
        if username:
            di = {"username": session.get("username", "")}
            ret = find_all_specific_user(coll_name="projects", di=di)
            all_response = []
            for var in ret:
                li_list = list(var.values())
                if li_list[2:-2] not in all_response:
                    all_response.append(li_list[2:-2])
            return render_template("project.html", all_response=all_response)
        else:
            return render_template("project.html")


@app.route("/skill", methods=["GET","POST"])
def skill():
    try:
        if request.method=="POST":
            skill = request.form["skill"]
            expertice = request.form["expertice"]

            username = session.get("username", "")
            if username:
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                new_dict = {"username":username, "skill": skill, "expertice": expertice, "created_on": created_on, "updated_on": updated_on}
                add_data = register_data(coll_name="skills", new_dict=new_dict)
                flash("data added succefully..................")

            else:
                flash("This user is not availble! Please first login....")
                return redirect(url_for('skill', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again......................")

    finally:
        username = session.get("username", "")
        if username:
            di = {"username": session.get("username", "")}
            ret = find_all_specific_user(coll_name="skills", di=di)
            all_response = []
            for var in ret:
                li_list = list(var.values())
                if li_list[2:-2] not in all_response:
                    all_response.append(li_list[2:-2])
            return render_template("skill.html", all_response=all_response)
        else:
            return render_template("skill.html")


@app.route("/social_media", methods=["GET","POST"])
def social_media():
    try:
        if request.method=="POST":
            social_media_name = request.form["sm_name"]
            sm_link = request.form["sm_link"]

            username = session.get("username", "")
            if username:
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                new_dict = {"username":username, "social_media_name": social_media_name, "social_media_link": sm_link,
                            "created_on": created_on, "updated_on": updated_on}
                add_data = register_data(coll_name="social_media_link", new_dict=new_dict)
                flash("data added succefully..................")

            else:
                flash("This user is not availble! Please first login....")
                return redirect(url_for('social_media', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again......................")

    finally:
        username = session.get("username", "")
        if username:
            di = {"username": session.get("username", "")}
            ret = find_all_specific_user(coll_name="social_media_link", di=di)
            all_response = []
            for var in ret:
                li_list = list(var.values())
                if li_list[2:-2] not in all_response:
                    all_response.append(li_list[2:-2])
            return render_template("social_media.html", all_response=all_response)
        else:
            return render_template("social_media.html")

@app.route("/personal_info", methods=["GET","POST"])
def personal_info():
    try:
        if request.method=="POST":
            photo_link = request.form["photo_link"]
            name = request.form["name"]
            age = request.form["age"]
            email = request.form["email"]
            phone = request.form["phone"]
            designation = request.form["designation"]
            language = request.form["language"]
            resume_link = request.form["resume_link"]
            description = request.form["description"]
            address = request.form["address"]

            username = session.get("username", "")
            if username:
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                new_dict = {"username":username, "photo_link": photo_link, "name": name,
                            "age": age, "email": email, "phone": phone, "designation":designation, "address":address,
                            "language": language, "resume_link": resume_link, "description": description,
                            "created_on": created_on, "updated_on": updated_on}
                add_data = register_data(coll_name="personal_info", new_dict=new_dict)
                flash("data added succefully..................")

            else:
                flash("This user is not availble! Please first login....")
                return redirect(url_for('personal_info', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again......................")

    finally:
        username = session.get("username", "")
        if username:
            di = {"username": session.get("username", "")}
            ret = find_all_specific_user(coll_name="personal_info", di=di)
            all_response = []
            for var in ret:
                li_list = list(var.values())
                if li_list[2:-2] not in all_response:
                    all_response.append(li_list[2:-2])
            return render_template("personal_info.html", all_response=all_response)
        else:
            return render_template("personal_info.html")

@app.route("/theme_form", methods=["GET","POST"])
def theme_form():
    try:
        username = session.get("username", "")
        di = {"username": username}

        ret = find_all_specific_user(coll_name="theme_selected", di=di)
        all_theme = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2] not in all_theme:
                all_theme.append(li_list[2])

        ret = find_all_specific_user(coll_name="personal_info", di=di)
        all_personal = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_personal:
                all_personal.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="education", di=di)
        all_education = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_education:
                all_education.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="experience", di=di)
        all_experience = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_experience:
                all_experience.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="skills", di=di)
        all_skills = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_skills:
                all_skills.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="social_media_link", di=di)
        all_sm = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_sm:
                all_sm.append(li_list[2:-2])

        ret = find_all_specific_user(coll_name="projects", di=di)
        all_project = []
        for var in ret:
            li_list = list(var.values())
            if li_list[2:-2] not in all_project:
                all_project.append(li_list[2:-2])

        if request.method=="POST":
            name = request.form["name"]
            email = request.form["email"]
            subject = request.form["subject"]
            message = request.form["message"]

            created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

            new_dict = {"username":username, "name": name, "email": email, "subject": subject, "message":message,
                        "created_on": created_on, "updated_on": updated_on}
            add_data = register_data(coll_name="user_data", new_dict=new_dict)

    except Exception as e:
        flash("Please try again......................")
        return redirect(url_for('dash_home', _external=True, _scheme=secure_type))

    finally:
        if all_theme:
            temp1 = all_theme[0]
            if all_sm and all_education and all_skills and all_personal:
                data_added = session.get("data_added")
                return render_template("main_templete/{}/index.html".format(temp1), all_sm=all_sm,
                                       all_project=all_project, all_skills=all_skills,
                                       all_experience=all_experience, all_personal=all_personal,
                                       all_education=all_education)
            else:
                return render_template("main_templete/{}/index_theme.html".format(temp1))
        else:
            return render_template("sample.html")


@app.route("/help", methods=["GET","POST"])
def help():
    try:
        if request.method=="POST":
            query = request.form["query"]

            created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

            new_dict = {"query": query, "created_on": created_on, "updated_on": updated_on}
            add_data = register_data(coll_name="help_form", new_dict=new_dict)
            flash("data added succefully..................")
            return render_template("help_form.html")
        else:
            return render_template("help_form.html")

    except Exception as e:
        flash("Please try again......................")
        return render_template("help_form.html")

@app.route("/pricing", methods=["GET","POST"])
def pricing():
    """
        That route can show all product plans....
    """
    return render_template("pricing.html")

# That is route for update pricing plan data
@app.route("/product_form", methods=["GET","POST"])
def product_form():
    """
    That function can add data for product plan subscripation and send a mail admin
    """

    try:
        if request.method=="POST":
            email = request.form["email"]
            phone = request.form["phone"]
            product_selection = request.form["product_selection"]
            username = session.get("username", [])

            if username:
                created_on = updated_on = datetime.now().strftime("%Y/%m/%d %H:%M")

                new_dict = {"username": username, "email": email, "phone": phone, "product_selection": product_selection, "created_on": created_on, "updated_on": updated_on}
                add_data = register_data(coll_name="product_purshase_data", new_dict=new_dict)
                flash("data added successfully.....................")
                return render_template("product_form.html")

            else:
                flash("Username is not availble! Please try out after login...")
                return redirect(url_for('product_form', _external=True, _scheme=secure_type))
        else:
            return render_template("product_form.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('product_form', _external=True, _scheme=secure_type))


@app.route("/admin_login", methods=["GET","POST"])
def admin_login():
    """
    That route can use login user
    """

    try:
        if request.method=="POST":
            username = request.form["username"]
            pwd = request.form["pwd"]

            session["admin_user"] = username
            session["admin_username"] = username
            res = find_all_cust_details_coll(coll_name="admin user")
            username_list = [[data.get("username", ""), data.get("password", "")] for data in res]

            if [username, pwd] in username_list:
                return redirect(url_for('admin_home', _external=True, _scheme=secure_type))
            else:

                flash("Your credentials doesn't match! Please enter correct Username and password...")
                return redirect(url_for('admin_login', _external=True, _scheme=secure_type))
        else:
            return render_template("admin/admin_login.html")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('admin_login', _external=True, _scheme=secure_type))

@app.route("/admin_home", methods=["GET","POST"])
def admin_home():
    """
    That route can show landing page while user can login
    """

    return render_template("admin/admin_home.html")

##  admin section

@app.route("/admin/<table_name>", methods=["GET","POST"])
def admin(table_name):
    """
    That route can show landing page while user can login
    """
    try:
        all_response, all_keys = all_data_fetching(table_name=table_name)
        return render_template("admin/{}.html".format(table_name), all_response=all_response, all_keys=all_keys, table_name=table_name)

    except Exception as e:
        print(e)
        flash("Sorry for that issue....Please try again!")
        return render_template("admin/{}.html".format(table_name))


@app.route("/admin_user", methods=["GET","POST"])
def admin_user():
    """
    That route can use login user
    """

    try:
        all_response, all_keys = all_data_fetching(table_name="admin user")
        if request.method=="POST":
            username = request.form["username"]
            pwd = request.form["pwd"]

            di = {"username": username, "password": pwd}
            msg = register_data(coll_name="admin user", new_dict="di")
            flash("data will added successfully.................")
            return render_template("admin/admin_user.html", all_keys=all_keys, all_response=all_response, table_name="admin user")
        else:
            return render_template("admin/admin_user.html", all_keys=all_keys, all_response=all_response, table_name="admin user")

    except Exception as e:
        flash("Sorry for that issue....Please try again!")
        return redirect(url_for('admin_home', _external=True, _scheme=secure_type))

def all_data_fetching(table_name):
    try:
        di = {}
        ret = find_all_specific_user(coll_name=table_name, di=di)

        if table_name not in ["admin user", "theme_selected"]:
            all_response = []
            all_keys = []
            for var in ret:
                li_list = list(var.values())
                if li_list[1:-2] not in all_response:
                    all_response.append(li_list[1:-2])

                li_key = list(var.keys())
                if li_key[1:-2] not in all_keys:
                    all_keys.append(li_key[1:-2])
        else:
            all_response = []
            all_keys = []
            for var in ret:
                li_list = list(var.values())
                if li_list[1:] not in all_response:
                    all_response.append(li_list[1:])

                li_key = list(var.keys())
                if li_key[1:] not in all_keys:
                    all_keys.append(li_key[1:])

        return all_response, all_keys

    except Exception as e:
        print(e)

if __name__ == "__main__":
    # db.create_all()
    app.run(
        host="127.0.0.1",
        port="5000",
        debug=True)

