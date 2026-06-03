import datetime
import jwt

MINHACHAVE="M1nh4ch4v3qu3s3r4ut1l1z4d4p4r4cr1pt0gr4f14d0t0k3nJWT"

def jwtDecode(encoded):
    return jwt.decode(encoded, MINHACHAVE, algorithms=["HS256"])

def jwtEncode(username):
    expiry = datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
    dados = {"cpf":username, "exp": int(expiry.timestamp())}
    token = jwt.encode(dados, MINHACHAVE, algorithm="HS256")
    return token