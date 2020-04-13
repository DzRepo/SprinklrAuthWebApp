from flask import Flask
from flask import render_template
from datetime import datetime
from flask import request
import SprinklrClient as sc

app = Flask(__name__)

# These values come from the application configuration at developer.sprinklr.com
key = "APPLICATION_KEY"
secret = "APPLICATION_SECRET"
path = None # None for Production

# This is the exact path of this application
# This must be the same as the callback URL in the Application configuration at Developer.Sprinklr.com
url = "https://mydomain.com/auth"

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/auth/', methods=['GET'])
def auth_page_processor():
    access_token = None
    refresh_token = None
    error = None
    name = None
    email = None
    link = None

    # Initialize the Sprinklr Client
    client = sc.SprinklrClient(key=key, path=path)

    # See if the authorization ticket code has been passed as a parameter. If so, process and generate an access code
    code = request.args.get('code', default = None, type = str)                                                                                  
    if code is not None and secret is not None:                                                                                                  
        if client.fetch_access_token(secret, "https://www.sprinklr.com", code):      # the redirect URI here is not used.                                                            
            access_token = client.access_token                                                                                                   
            refresh_token = client.refresh_token                                                                                                 
                                                                                                                                                 
            if client.fetch_user():                                                                                                              
                result = client.result["data"]                                                                                                   
                name = result["name"]                                                                                                            
                email = result["email"]                                                                                                          
        else:                                                                                                                                    
            error = client.result
    else:
        # If no code was passed, generate the link to start the authorization process
        link = client.authorize(key, url, path)                                                                                                      

    return render_template(
            "auth.html",
            link = link,
            code = code,
            access_token = access_token,
            refresh_token = refresh_token,
            name = name,
            email = email,
            error = error
        )

@app.errorhandler(500)
def server_error(e):
    # logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500
                                                                                                                                                 
if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the                                                                             
    # application on Google App Engine. See entrypoint in app.yaml.                                                                              
    app.run(host='127.0.0.1', port=8080, debug=True)