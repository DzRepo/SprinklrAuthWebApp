from flask import Flask
from flask import render_template
from datetime import datetime
from flask import request, session
import SprinklrClient as sc

app = Flask(__name__)
app.secret_key = "My name is groot!" + str(datetime.now())

key = "APIKEY HERE"
secret = "APPLICATION SECRET HERE"
path = None # None for Production
url = "https://thisdomain.com/auth"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/auth/', methods=['GET','POST'])
def auth_page_processor():
    
    access_token = None
    refresh_token = None
    error = None
    name = None
    email = None

    # Get posted fields from form & request url if present
    
    """ 
    key=None
    path=None
    url=None
    secret = None
    
    if "key" in request.values:
        key = request.values["key"]
        session["key"] = key
    elif "key" in session.keys():
        key = session["key"]

    if "path" in request.values:
        path = request.values["path"]
        session["path"] = path
    elif "path" in session.keys():
        path = session["path"]

    if "secret" in request.values:
        secret = request.values["secret"]
        session["secret"] = secret
    elif "secret" in session.keys():
        secret = session["secret"]

    if "url" in request.values:
        url = request.values["url"]
        session["url"] = url
    elif "url" in session.keys():
        url = session["url"] """

    client = sc.SprinklrClient(key=key, path=path)
    link = client.authorize(key, url, path)
    
    code = request.args.get('code', default = None, type = str)
    if code is not None and secret is not None:
        if client.fetch_access_token(secret, "https://www.sprinklr.com", code):
            access_token = client.access_token
            refresh_token = client.refresh_token

            if client.fetch_user():
                result = client.result["data"]
                name = result["name"]
                email = result["email"]
        else:
            error = client.result

    return render_template(
            "auth.html",
            key=key,
            path=path,
            secret=secret,
            url=url,
            link = link,
            code = code,
            access_token = access_token,
            refresh_token = refresh_token,
            name = name,
            email = email,
            error = error
        )
    