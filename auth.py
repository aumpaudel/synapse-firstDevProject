import bcrypt
from sqlalchemy.orm import Session
from models import User

def registerUser(db: Session, user_id: str, name: str, email: str, password: str):
    existing_email = db.query(User).filter(User.email == email).first()
    existing_id = db.query(User).filter(User.id == user_id).first()
    if existing_email or existing_id:
        return {"message": "User with this email or ID already exists"}
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = User(id=user_id, name=name, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user": new_user}

def authenticateUser(db: Session, identifier: str, password: str):
    user = db.query(User).filter((User.email == identifier) | (User.id == identifier)).first()
    if not user:
        return {"message": "User not found"}
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return {"message": "Authentication successful", "user": user}
    else:
        return {"message": "Invalid password"}
    
def deleteUser(db: Session, identifier: str, password: str):
    user = db.query(User).filter((User.email == identifier) | (User.id == identifier)).first()
    if not user:
        return {"message": "User not found"}
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        return {"message": "Invalid password"}  