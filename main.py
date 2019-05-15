import os
import cv2
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename


from Screte_PRIVATE.screte_database.database import Database
import Screte_PRIVATE.screte_cryptography.example_from_Oles as eo
from Screte_PRIVATE.screte_cryptography.image import Image, ImageLoaderAndSaver, diffie_hellman_key, form_secret_key


app = Flask(__name__)
# os.makedirs(os.path.join(app.instance_path, 'image_store'), True)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "s_ec%re^t#k*ey**su-pe!r"

db = Database()


@app.route('/', methods=["GET", "POST"])
def hello():
    return render_template("main.html", log_msg='', reg_msg='')


@app.route('/contacts', methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        # return render_template("contacts.html", contacts=["name", "No contacts - it's a new user"])

        rep_password = request.form.get("new_password_repeated")
        if rep_password:
            user_name, f_name, l_name, password = request.form.get("new_user_name"),\
                                                  request.form.get("first_name"),\
                                                  request.form.get("last_name"), \
                                                  request.form.get("new_password")
            if rep_password == password:
                if not db.get_user_id(user_name):
                    u_info = {"username": user_name,
                              "first_name": f_name,
                              "last_name": l_name,
                              "password": password}
                    if db.add_user(u_info):
                        return render_template("contacts.html", contacts=[], self_name=user_name)
                    return render_template("main.html", log_msg="", reg_msg="Sorry. This name is already taken.")
                return render_template("main.html", log_msg="", reg_msg="You didn't repeat your password correctly.")
        # # log in
        else:
            user_name, password = request.form.get("user_name"), \
                                  request.form.get("password")

            print(db.check_password(user_name, password))
            if db.check_password(user_name, password):
                return render_template("contacts.html", contacts=db.get_contacts(user_name), self_name=user_name)
            return render_template("main.html", reg_msg="", log_msg="Wrong username or password. Try again.")
    return render_template("main.html", reg_msg="", log_msg="")  # if request.method == "GET"


@app.route('/send/<string:from_name>/<string:to_name>', methods=["GET", "POST"])
def send(from_name, to_name):
    return render_template("send.html", from_name=from_name, to_name=to_name)


@app.route('/result/<string:from_name>/<string:to_name>', methods=["GET", "POST"])
def result(from_name, to_name):
    if request.method == "POST":
        # img = request.form.get("img")
        img = request.files["img"]
        print(img)
        if img is not None:

            # save image to "instance" directory
            img_path = os.path.join(app.instance_path, secure_filename(img.filename))
            img.save(img_path)

            # read
            img_data = ImageLoaderAndSaver.load_image_locally(img_path)

            fk = db.get_user_info_for_encryption(from_name)["sh_key"]
            tk = db.get_user_info_for_encryption(to_name)["sh_key"]

            sh_key = diffie_hellman_key(fk, tk)
            the_key = form_secret_key(img_data, sh_key)
            print(type(the_key))
            print(the_key)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            encr_img = Image.encrypt_img(img_data, the_key)
            ImageLoaderAndSaver.save_image_locally(encr_img, img_path)

            # decrypt
            enc_img = ImageLoaderAndSaver.load_image_locally("secret.bmp")
            new_the_key = form_secret_key(enc_img, sh_key)

            our_img = Image.decrypt_img(enc_img, new_the_key)
            ImageLoaderAndSaver.save_image_locally(our_img, img.filename)

        return render_template("result.html", img_name=img.filename)
    else:
        return render_template("result.html", img_url="")


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=True)
