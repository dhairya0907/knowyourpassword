from flask import Blueprint, jsonify
from globalImports import limiter
from globalImports import cache
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import importlib
import string


PasswordHashes = Blueprint("PasswordHashes", __name__)
providers = {"haveibeenpwned", "rockyou", "topmillion"}
# StaticPath = "mysite/api/v1/static/"
# StaticImport = importlib.import_module("mysite.api.v1.static.IdDictionary")
StaticPath = "api/v1/static/"
StaticImport = importlib.import_module("api.v1.static.IdDictionary")


def authorize_drive():
    gAuth = GoogleAuth()
    gAuth.DEFAULT_SETTINGS['client_config_file'] = StaticPath + "client_secret.json"
    gAuth.LoadCredentialsFile(StaticPath + "myCredentials.txt")
    return GoogleDrive(gAuth)

def getHashFileIDs(provider):
    if provider == 'haveibeenpwned':
        return StaticImport.haveibeenpwned
    elif provider == 'rockyou':
        return StaticImport.rockyou
    elif provider == 'topmillion':
        return StaticImport.topmillion

def gethashes(provider, prehash):
    if len(prehash) != 5:
        return jsonify({"error": "The hash prefix was not in a valid format", "status": 400}) , 400
    elif not all(c in string.hexdigits for c in prehash):
        return jsonify({"error": "The hash prefix was not valid hexadecimal", "status": 400}) , 400
    elif provider not in  providers:
        return jsonify({"error": "The hash provider was not valid", "status": 400}) , 400
    else:
        gAuth = GoogleAuth()
        gAuth.LoadCredentialsFile(StaticPath + "myCredentials.txt")
        if gAuth.credentials is None:
            gAuth.LocalWebserverAuth()
        elif gAuth.access_token_expired:
            gAuth.Refresh()
        else:
            gAuth.Authorize()
        gAuth.SaveCredentialsFile(StaticPath + "myCredentials.txt")
        drive = authorize_drive()

        hash_file_ids = getHashFileIDs(provider)

        hash_file = drive.CreateFile({'id': hash_file_ids[prehash[:2]]})
        data = hash_file.GetContentString().split('\n')

        hash_found = []
        flag = 0
        prehash = prehash[2:]

        for line in data:
            if line.startswith(prehash.upper()):
                flag = 1
                hash_found.append(line[3:].rstrip("\n"))
            elif flag == 1:
                return jsonify({"hashes": hash_found,"hashcount": len(hash_found), "status": 200}), 200

        return jsonify({"hashes": hash_found,"hashcount": len(hash_found), "status": 200}), 200


@PasswordHashes.route("/api/v1/<string:provider>/<string:prehash>", methods=['GET'])
@cache.cached(timeout=604800)  # 604800 cache set to 1 week in seconds
@limiter.limit("1/2 seconds")  # rate limit set to 1 requests per 10 seconds
def getresult(provider, prehash):
    return gethashes(provider, prehash)

@PasswordHashes.route("/api/v1/haveibeenpwned/<string:prehash>", methods=['GET'])
@cache.cached(timeout=604800)  # 604800 cache set to 1 week in seconds
@limiter.limit("1/10 seconds")  # rate limit set to 1 requests per 20 seconds
def gethaveibeenpwned(prehash):
    return gethashes("haveibeenpwned", prehash)


