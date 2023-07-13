from flask import (flash, Flask, redirect, render_template, request,
                   session, url_for, send_file)
import os
from werkzeug.utils import secure_filename
import pandas as pd
from threading import Thread

import smtplib
from email.mime.text import MIMEText
from pymongo import MongoClient
from email.mime.multipart import MIMEMultipart
import datetime
from email.mime.base import MIMEBase
from email import encoders

from flaskwebgui import FlaskUI
import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "sdfsf65416534sdfsdf4653"
app.config["expire_plan"] = 1
app.config["back_color"] = "#f2f2f2"
secure_type = "http"

def sending_email(extension, to_m, subject_main, body_text, username, password_to, host_main, port_main, attachment_all_file):
    try:
        if extension=="gmail.com":
            sender_email = username
            sender_password = password_to  
            receiver_email = to_m  
            subject = subject_main
            message = body_text

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach the message to the email
            msg.attach(MIMEText(message, 'plain'))

            # Attach the files
            for file_path in attachment_all_file:
                attachment = MIMEBase('application', 'octet-stream')
                with open(file_path, 'rb') as file:
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                filename = os.path.basename(file_path)
                attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                message.attach(attachment)

            # SMTP connection
            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with the Hostinger SMTP server and port
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print('Email sent successfully!')
            except Exception as e:
                print('Error sending email:', str(e))
            finally:
                server.quit()
                output_file_path = os.path.abspath("log_main.txt")
                current_date_time = datetime.datetime.now()
                with open(output_file_path, "a") as file:
                    file.write(str(current_date_time) + ":" +to_m+"    :  Success\n")
        elif extension=="webapphealing.com":
            sender_email = username
            sender_password = password_to  
            receiver_email = to_m  
            subject = subject_main
            message = body_text

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach the message to the email
            msg.attach(MIMEText(message, 'plain'))

            # Attach the files
            for file_path in attachment_all_file:
                attachment = MIMEBase('application', 'octet-stream')
                with open(file_path, 'rb') as file:
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                filename = os.path.basename(file_path)
                attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(attachment)

            # SMTP connection
            try:
                server = smtplib.SMTP('mail.webapphealing.com', 587)  # Replace with the Hostinger SMTP server and port
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print('Email sent successfully!')
            except Exception as e:
                print('Error sending email:', str(e))
            finally:
                server.quit()
                output_file_path = os.path.abspath("log_main.txt")
                current_date_time = datetime.datetime.now()
                with open(output_file_path, "a") as file:
                    file.write(str(current_date_time) + ":" +to_m+"    :  Success\n")
        elif extension=="yahoo.com":
            # Email configuration
            sender_email = username
            sender_password = password_to  
            receiver_email = to_m  
            subject = subject_main
            message = body_text

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach the message to the email
            msg.attach(MIMEText(message, 'plain'))

            # Attach the files
            for file_path in attachment_all_file:
                attachment = MIMEBase('application', 'octet-stream')
                with open(file_path, 'rb') as file:
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                filename = os.path.basename(file_path)
                attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                message.attach(attachment)

            # SMTP connection
            try:
                server = smtplib.SMTP('smtp.mail.yahoo.com', 587)  # Replace with the Yahoo SMTP server and port
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print('Email sent successfully!')
            except Exception as e:
                print('Error sending email:', str(e))
            finally:
                server.quit()
                output_file_path = os.path.abspath("log_main.txt")
                current_date_time = datetime.datetime.now()
                with open(output_file_path, "a") as file:
                    file.write(str(current_date_time) + ":" +to_m+"    :  Success\n")
                    
        elif extension=="outlook.com":
            # Email configuration
            sender_email = username
            sender_password = password_to  
            receiver_email = to_m  
            subject = subject_main
            message = body_text

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach the message to the email
            msg.attach(MIMEText(message, 'plain'))

            # Attach the files
            for file_path in attachment_all_file:
                attachment = MIMEBase('application', 'octet-stream')
                with open(file_path, 'rb') as file:
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                filename = os.path.basename(file_path)
                attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                msg.attach(attachment)

            # SMTP connection
            try:
                server = smtplib.SMTP('smtp.office365.com', 587)  # Replace with the Outlook SMTP server and port
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print('Email sent successfully!')
            except Exception as e:
                print('Error sending email:', str(e))
            finally:
                server.quit()
                output_file_path = os.path.abspath("log_main.txt")
                current_date_time = datetime.datetime.now()
                with open(output_file_path, "a") as file:
                    file.write(str(current_date_time) + ":" +to_m+"    :  Success\n")
        else:
            sender_email = username
            sender_password = password_to  
            receiver_email = to_m  
            subject = subject_main
            message = body_text

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject

            # Attach the message to the email
            msg.attach(MIMEText(message, 'plain'))

            # Attach the files
            for file_path in attachment_all_file:
                attachment = MIMEBase('application', 'octet-stream')
                with open(file_path, 'rb') as file:
                    attachment.set_payload(file.read())
                encoders.encode_base64(attachment)
                filename = os.path.basename(file_path)  
                attachment.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                message.attach(attachment)

            # SMTP connection
            try:
                server = smtplib.SMTP(host_main, port_main)  # Replace with the Hostinger SMTP server and port
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
                print('Email sent successfully!')
            except Exception as e:
                print('Error sending email:', str(e))
            finally:
                server.quit()
                output_file_path = os.path.abspath("log_main.txt")
                current_date_time = datetime.datetime.now()
                with open(output_file_path, "a") as file:
                    file.write(str(current_date_time) + ":" +to_m+"    :  Success\n")

    except Exception as e:
        print(e)

client = MongoClient("mongodb+srv://harshitgadhiya:Hgadhiya8980@codescatter.04ufqjh.mongodb.net/?retryWrites=true&w=majority")

db = client["email_sending_tool"]

def register_data(coll_name, new_dict):
    try:
        coll = db[coll_name]
        coll.insert_one(new_dict)

        return "add_data"

    except Exception as e:
        print(e)

def find_all_cust_details():
    try:
        coll = db["customer_details"]
        res = coll.find({})
        return res

    except Exception as e:
        print(e)

def find_all_cust_details_coll(coll_name):
    try:
        coll = db[coll_name]
        res = coll.find({})
        return res

    except Exception as e:
        print(e)


def find_all_specific_user(coll_name, di):
    try:
        coll = db[coll_name]
        res = coll.find(di)
        return res

    except Exception as e:
        print(e)

def delete_data(coll_name, di):
    try:
        coll = db[coll_name]
        res = coll.delete_one(di)
        return res

    except Exception as e:
        print(e)

def update_data(coll_name, prev_data, update_data):
    try:
        coll = db[coll_name]
        coll.update_one(prev_data, update_data)
        return "updated"

    except Exception as e:
        print(e)


# symdbvuacrezywff

def folder_messgae_file():
    try:
        folder_path = os.path.abspath('data/message_file')
        filenames = os.listdir(folder_path)
        return filenames

    except Exception as e:
        print(e)

def folder_sending_file():
    try:
        folder_path1 = os.path.abspath('data/sending_file')
        filenames1 = os.listdir(folder_path1)
        return filenames1

    except Exception as e:
        print(e)


def folder_attach_file():
    try:
        folder_path2 = os.path.abspath('data/attachment_file')
        filenames2 = os.listdir(folder_path2)
        return filenames2

    except Exception as e:
        print(e)


@app.route("/", methods=["GET", "POST"])
def login_main():
    try:
        return render_template("auth/login.html")

    except Exception as e:
        print(e)


@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        if request.method=="POST":
            username = request.form["username"]
            apikey = request.form["pwd"]

            all_response = find_all_cust_details()
            li = []
            for a in all_response:
                if username==a["username"] and apikey == a["api_key"]:
                    app.config["role"] = a["role"]
                li.append([a["username"], a["api_key"]])

            if [username, apikey] in li:
                flash("login successfully......")
                return redirect(url_for('home', _external=True, _scheme=secure_type))
            else:
                flash("Please get your subscription......")
                return render_template("auth/login.html")
        else:
            return render_template("login.html")

    except Exception as e:
        print(e)

# That is logout route and clear the current session
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """
    That funcation was logout session and clear user session
    """

    try:
        session.clear()
        return redirect(url_for('login_main', _external=True, _scheme=secure_type))

    except Exception as e:
        flash("Please try again.......................................")
        return redirect(url_for('login_main', _external=True, _scheme=secure_type))

@app.route("/home", methods=["GET", "POST"])
def home():
    try:
        color = app.config["back_color"]
        session["color"] = color
        message_file = folder_messgae_file()
        sending_file = folder_sending_file()
        attachment_file = folder_attach_file()
        role = app.config.get("role", "")
        if role and role=="admin":
            role_main = role
        else:
            role_main=""

        return render_template("index.html", message_file=message_file, sending_file=sending_file, attachment_file=attachment_file, role_main=role_main)

    except Exception as e:
        print(e)

@app.route("/process", methods=["GET", "POST"])
def process():
    try:
        color = app.config["back_color"]
        session["color"] = color
        message_file = folder_messgae_file()
        sending_file = folder_sending_file()
        role = app.config.get("role", "")
        if role and role=="admin":
            role_main = role
        else:
            role_main = ""
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            host = request.form["host"]
            port = request.form["port"]
            subject = request.form["subject"]

            message_file = request.files['message_file']
            mail_file = request.files['mail_file']
            attachment_file = request.files.getlist('attachment_file')
            msg_save_dir = os.path.abspath("static/uploaded/msg_file")
            send_save_dir = os.path.abspath("static/uploaded/send_file")
            attach_save_dir = os.path.abspath("static/uploaded/attach_file")

            
            send_name = mail_file.filename
            exten = send_name.split(".")[-1]
            sp_data_path = os.path.join(send_save_dir, mail_file.filename)
            if send_name.split(".")[-1] == "xlsx" or send_name.split(".")[-1] == "csv":
                mail_file.save(sp_data_path)
            else:
                flash("Email sent successfully......")
                return redirect(url_for('home', _external=True, _scheme=secure_type))


            msg_data_path = os.path.join(msg_save_dir, message_file.filename)
            message_file.save(msg_data_path)

            attachment_all_file = []
            for file in attachment_file:
                attach_file_path = os.path.join(attach_save_dir, file.filename)
                attachment_all_file.append(attach_file_path)
                file.save(attach_file_path)

            if port:
                port = int(port)

            if exten == "xlsx":
                df = pd.read_excel(sp_data_path)
            else:
                df = pd.read_csv(sp_data_path)
            
            ex1 = username.split("@")[-1]

            threads = []
            for em, cus_name in zip(df["Emails"], df["name"]):
                body_text = ""
                html_text = ""
                line_count = 0
                with open(msg_data_path, 'r') as f:
                    for line in f:
                        if line_count==0:
                            body_text1 = line.replace(",\n", "")
                            body_text = body_text+str(body_text1)+" "+str(cus_name)+",\n"
                        else:
                            body_text = body_text+str(line)
                        line_count+=1
                        if line == "\n":
                            html_text = html_text+"<br>"
                        else:
                            html_text = html_text+"<p>"+str(line).replace("\n", "") + "</p>"

                if ex1.lower() not in ["email.com", "yahoo.com", "outlook.com", "webapphealing.com"]:
                    t = Thread(target=sending_email, args=(ex1, em, subject, body_text, username, password, host, port, attachment_all_file))
                    threads.append(t)
                    t.start()
                else:
                    t = Thread(target=sending_email, args=(ex1, em, subject, body_text, username, password, host, port, attachment_all_file))
                    threads.append(t)
                    t.start()

            for t in threads:
                t.join()

            flash("Email sent successfully......")

            return redirect(url_for('home', _external=True, _scheme=secure_type))
        else:
            return render_template("index.html", message_file=message_file, sending_file=sending_file, role_main=role_main)

    except Exception as e:
        print(e)
        return redirect(url_for('home', _external=True, _scheme=secure_type))
    
@app.route("/admin_panel", methods=["GET", "POST"])
def admin_panel():
    try:
        return render_template("home.html")
    except Exception as e:
        print(e)
        return redirect(url_for('admin_panel', _external=True, _scheme=secure_type))

@app.route("/user_admin_panel", methods=["GET", "POST"])
def user_admin_panel():
    try:
        return render_template("user_admin_panel.html")
    except Exception as e:
        print(e)
        return redirect(url_for('user_admin_panel', _external=True, _scheme=secure_type))
    
@app.route("/color_change/<role>", methods=["GET", "POST"])
def color_change(role):
    try:
        if request.method == "POST":
            color = request.form["color"]
            app.config["back_color"] = color
            if role=="admin":
                return render_template("color_changes.html")
            else:
                return render_template("color_changes_admin.html")
        else:
            if role=="admin":
                return render_template("color_changes.html")
            else:
                return render_template("color_changes_admin.html")
    except Exception as e:
        print(e)
        return redirect(url_for('color_change', _external=True, _scheme=secure_type))
    
@app.route("/background_change/<role>", methods=["GET", "POST"])
def background_change(role):
    try:
        if request.method == "POST":
            file = request.files['resume_link']  # Access the uploaded file using the 'file' key
            file_path = os.path.join("static/",  "pexels-photo-1591062.jpeg")  # Create the full file path
            print(file_path)

            if os.path.exists(file_path):  # Check if the file exists
                os.remove(file_path)  # Delete the file
            
            file_path1 = os.path.join("static/", "pexels-photo-1591062.jpeg")  # Create the full file path
            file.save(file_path1)
            if role=="admin":
                return render_template("background_changes.html")
            else:
                return render_template("background_changes_admin.html")

        else:
            if role=="admin":
                return render_template("background_changes.html")
            else:
                return render_template("background_changes_admin.html")
    except Exception as e:
        print(e)
        return redirect(url_for('background_change', _external=True, _scheme=secure_type))
    

@app.route("/logo_change/<role>", methods=["GET", "POST"])
def logo_change(role):
    try:
        if request.method == "POST":
            file = request.files['resume_link']  # Access the uploaded file using the 'file' key
            file_path = os.path.join("static/", "main_logo.png")  # Create the full file path
            print(file_path)

            if os.path.exists(file_path):  # Check if the file exists
                os.remove(file_path)  # Delete the file
            
            
            file_path1 = os.path.join("static/", "main_logo.png")  # Create the full file path
            file.save(file_path1)
            if role=="admin":
                return render_template("logo_changes.html")
            else:
                return render_template("logo_changes_admin.html")
        else:
            if role=="admin":
                return render_template("logo_changes.html")
            else:
                return render_template("logo_changes_admin.html")
    except Exception as e:
        print(e)
        return redirect(url_for('logo_change', _external=True, _scheme=secure_type))

    
@app.route("/user_panel", methods=["GET", "POST"])
def user_panel():
    try:
        all_response = find_all_cust_details()
        if request.method == "POST":
            username = request.form["username"]
            api_key = request.form["api_key"]
            role = request.form["role"]

            all_response1 = find_all_cust_details()
            li = []
            for a in all_response1:
                li.append(a["username"])

            if username not in li:
                di = {"username":username, "api_key": api_key, "role": role}
                res = register_data(coll_name="customer_details", new_dict=di)
                return render_template("user_panel.html", all_response=all_response)
            else:
                flash("username already exits..")
                return render_template("user_panel.html", all_response=all_response)

        else:
            return render_template("user_panel.html", all_response=all_response)
    except Exception as e:
        print(e)
        return redirect(url_for('user_panel', _external=True, _scheme=secure_type))
    
@app.route("/deletedata/<id_num>", methods=["GET", "POST"])
def deletedata(id_num):
    try:
        di = {}
        di["api_key"] = id_num
        res = delete_data(coll_name="customer_details", di=di)
        return redirect(url_for('user_panel', _external=True, _scheme=secure_type))

    except Exception as e:
        print(e)
        return redirect(url_for('user_panel', _external=True, _scheme=secure_type))


@app.route("/view_logs", methods=['GET'])
def view_logs():
    try:
        file = os.path.abspath("log_main.txt")    
        lines = []
        with open(file, "r") as f:
            lines+=f.readlines()
        return render_template("logs.html", lines=lines)
    
    except Exception as e:
        print(e)

@app.route("/download_logs", methods=['GET'])
def download_logs():
    file = os.path.abspath("log_main.txt")
    return send_file(file, as_attachment=True)


if __name__ == "__main__":
    # db.create_all()
    FlaskUI(app=app, server="flask").run()