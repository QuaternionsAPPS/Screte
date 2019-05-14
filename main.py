from flask import Flask, request, render_template, send_from_directory


from Screte_PRIVATE.screte_database.database import Database
#/home/anastasiia/AL_Projects/Screte/Screte_PRIVATE/screte_database/database.py

# import sys
# print(sys.path)
# sys.path.insert(0, "Documents/Screte_2/Screte/Screte_PRIVATE/screte_database")
# print(sys.path)
#
# import Database


app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "s ec re t k ey su pe r"

db = Database()


@app.route('/', methods=["GET", "POST"])
def hello():
    return render_template("main.html", log_msg='', reg_msg='')


@app.route('/contacts', methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        user_name, password, rep_password = request.form.get("user_name"), \
                                            request.form.get("password"), \
                                            request.form.get("password_repeated")
        # register
        if rep_password:
            f_name, l_name = request.form.get("first_name"), request.form.get("last_name")
            if rep_password == password:
                if not db.get_user_id(user_name):   # check if such name exists in db
                    u_info = {"username": user_name,
                              "first_name": f_name,
                              "last_name": l_name,
                              "password": password}
                    if db.add_user(u_info):
                        return render_template("contacts.html", contacts=db.get_contacts(user_name))
                else:
                    return render_template("main.html", log_msg="", reg_msg="Sorry. This name is already taken.")
            else:
                return render_template("main.html", log_msg="", reg_msg="You didn't repeat your password correctly.")
        # log in
        else:
            if db.check_password(user_name, password):
                return render_template("contacts.html", contacts=db.get_contacts(user_name))
            else:
                return render_template("main.html", reg_msg="", log_msg="Wrong username or password. Try again.")
    else:
        return render_template("main.html", reg_msg="", log_msg="")  # if request.method == "GET"


@app.route('/send/<string:u_name>/<int:to_id>', methods=["GET", "POST"])
def send(u_name, to_id):
    return render_template("send.html", users=[db.get_contacts(username="Gilly")])


@app.route('/result/<int:from_id>/<int:to_id>', methods=["GET", "POST"])
def result(from_id, to_id):
    if request.method == "POST":
        img = request.form.get("img")
        if img:
            # process, save, give url
            res_url = "https://instagram.fiev21-2.fna.fbcdn.net/vp/ab053c540461f0765c71c72a2d615125/5D666C46/t51.2885-19/s150x150/51939312_838258313180447_8972914188674400256_n.jpg?_nc_ht=instagram.fiev21-2.fna.fbcdn.net"
            return render_template("result.html", img_url=res_url)
    else:
        return render_template("result.html", img_url="")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True, use_reloader=True)

    # import os
    # print(os.path.curdir)
