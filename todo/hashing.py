from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    def bcrypt(password: str):
        hashedPass = pwd_cxt.hash(password)
        return hashedPass
