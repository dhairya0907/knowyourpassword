from flask import Flask, jsonify, render_template, request
from globalImports import limiter
from globalImports import cache
from api.v1.blueprints.PasswordHashes import PasswordHashes


app = Flask(__name__)
limiter.init_app(app)
cache.init_app(app)
app.register_blueprint(PasswordHashes)


@app.route("/")
def home():
    return render_template('home.html')


@app.errorhandler(429)
def ratelimit_handler(error):
    if request.path.startswith("/api/v1/haveibeenpwned/"):
        return (jsonify({"error": "Too many requests", "message": "1 per 20 seconds", "status": 429}), 429,)
    else:
        return (jsonify({"error": "Too many requests", "message": "1 per 10 seconds", "status": 429}), 429,)

@app.errorhandler(500)
def internal_error(error):
    return (jsonify({"error": "An internal error occurred", "status": 500}), 500,)

@app.errorhandler(404)
def not_found(error):
    return (jsonify({"error": "The requested resource was not found", "status": 404}), 404,)
