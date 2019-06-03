import os

from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename

from screte_database.database import Database
from screte_cryptography.image import Image, ImageLoaderAndSaver, form_secret_key
from screte_cryptography.diffie_hellman_keys import diffie_hellman_shared_key


db = Database()


def start_app():
    app = Flask(__name__)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.secret_key = "s_ec%re^t#k*ey**su-pe!r"
    return app


app = start_app()


@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


@app.route('/', methods=["GET", "POST"])
def start():
    return render_template("main.html")


@app.route('/contacts', methods=["GET", "POST"])
def contacts():
    if request.method == "POST":

        # new user
        rep_password = request.form.get("new_pass_rep")
        if rep_password:
            user_name, f_name, l_name, password = request.form.get("new_name"),\
                                                  request.form.get("first_name"),\
                                                  request.form.get("last_name"),\
                                                  request.form.get("new_pass")
            if rep_password == password:
                u_info = {"username": user_name, "first_name":f_name, "last_name": l_name, "password": password}
                if db.add_user(u_info):
                    return render_template("contacts.html", contacts=[user_name], self_name=user_name)
            return render_template("main.html", log_msg="", reg_msg="You didn't repeat your password correctly.")

        # log in
        else:
            user_name, password = request.form.get("name"), request.form.get("password")
            print(user_name, password)

            if db.check_password(user_name, password):
                return render_template("contacts.html", contacts=db.get_contacts(user_name), self_name=user_name)
            return render_template("main.html", reg_msg="", log_msg="Wrong username or password. Try again.")

    elif request.method == "GET":
        return render_template("main.html", reg_msg="", log_msg="")


@app.route('/send/<string:from_name>/<string:to_name>', methods=["GET", "POST"])
def send(from_name, to_name):
    return render_template("send.html", from_name=from_name, to_name=to_name)


@app.route('/result/<string:from_name>/<string:to_name>', methods=["GET", "POST"])
def result(from_name, to_name):

    # send image
    if request.method == "POST":
        print("post")

        img = request.files["img"]
        print(img)
        if img is not None:

            # read, encrypt
            img_data = ImageLoaderAndSaver.load_uploaded_image(img)

            fk = db.get_user_info_for_encryption(from_name)["sh_key"]
            tk = db.get_user_info_for_encryption(to_name)["sh_key"]

            sh_key = diffie_hellman_shared_key(fk, tk)
            the_key = form_secret_key(img_data, sh_key)
            encr_img = Image.encrypt_img(img_data, the_key)

            # img_file_name = secure_filename(img.filename)[:img.filename.rfind(".")] + ".bmp"
            # img_path = os.path.join(app.instance_path, img_file_name)

            # save image
            enr_img_id = db.add_picture({"from_user": from_name, "to_user": to_name, "info_from_user": ""})
            ImageLoaderAndSaver.upload_image_to_filesystem(encr_img, enr_img_id)
            ImageLoaderAndSaver.download_image_from_filesystem(enr_img_id, "./static/")

            # decrypt
            '''
            enc_img = ImageLoaderAndSaver.load_image_locally(img_path)
            new_the_key = form_secret_key(enc_img, sh_key)

            our_img = Image.decrypt_img(enc_img, new_the_key)
            ImageLoaderAndSaver.save_image_locally(our_img, img.filename)
            '''
            return render_template("result.html", img_name=str(enr_img_id)+".jpg")
        else:
            return render_template("result.html", img_id=None)

    # read image
    elif request.method == "GET":
        print("get")
        img_id = 33
        ImageLoaderAndSaver.download_image_from_filesystem(img_id, 'static')
        return render_template("result.html", img_name=str(img_id)+".jpg")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(host='0.0.0.0', port=8080, debug=True)
