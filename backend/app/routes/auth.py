from fastapi import APIRouter,HTTPException
from pydantic import BaseModel,Field
from app.db.mongo import users
from app.utils.security import hash_password,verify_password,create_token
router=APIRouter()
class Auth(BaseModel):
    username:str=Field(min_length=3,max_length=50)
    password:str=Field(min_length=6,max_length=100)
@router.post("/register")
def register(x:Auth):
    if users.find_one({"username":x.username}): raise HTTPException(409,"Username already exists")
    r=users.insert_one({"username":x.username,"password_hash":hash_password(x.password)})
    return {"token":create_token(str(r.inserted_id)),"username":x.username}
@router.post("/login")
def login(x:Auth):
    u=users.find_one({"username":x.username})
    if not u or not verify_password(x.password,u["password_hash"]): raise HTTPException(401,"Invalid username or password")
    return {"token":create_token(str(u["_id"])),"username":u["username"]}
