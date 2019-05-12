from flask import Flask, request, render_template, send_from_directory


app = Flask(__name__)
# app.jinja_env.auto_reload = True
# app.config['TEMPLATES_AUTO_RELOAD'] = True
# app.secret_key = "super secret key"

# ~~~~~~~~~~~~~~~~~~~~ Example function -- need db communication.

def get_auth_id(user_name, password):
    return 3


def add_user(name, password):
    return 4


def get_contacts(user_id):
    return [{"id": 234, "name": "Eric"}, {"id": 345, "name": "Rita"}, {"id": 456, "name": "Tony"}]


def has_name(username):
    return False


def get_name(user_id):
    return "Noy"

def get_info(user_id):
    return {"id": 456, "name": "Tony"}
# ~~~~~~~~~~~~~~~~~~~~



@app.route('/', methods=["GET", "POST"])
def hello():
    return render_template("main.html", log_msg='', reg_msg='')


@app.route('/contacts', methods=["GET", "POST"])
def contacts():
    if request.method == "POST":
        user_name, password, rep_password = request.form.get("user_name"), \
                                            request.form.get("password"), \
                                            request.form.get("repeated_password")
        # register
        if rep_password:
            if rep_password == password:
                if has_name(user_name):
                    new_u_id = add_user(user_name, password)
                    return render_template("contacts.html", contacts=get_contacts(new_u_id))
                else:
                    return render_template("main.html", log_msg="", reg_msg="Sorry. This name is already taken.")
            else:
                return render_template("main.html", log_msg="", reg_msg="You didn't repeat your password correctly.")
        # log in
        else:
            u_id = get_auth_id(user_name, password)
            if u_id:
                return render_template("contacts.html", contacts=get_contacts(u_id))
            else:
                return render_template("main.html", reg_msg="", log_msg="Wrong username or password. Try again.")
    else:  # if request.method == "GET"
        return render_template("main.html", reg_msg="", log_msg="")


@app.route('/send/<int:from_id>/<int:to_id>', methods=["GET", "POST"])
def send(from_id, to_id):
    # access to db --> info about both users
    return render_template("send.html", users=[get_info(from_id), get_info(to_id)])


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
