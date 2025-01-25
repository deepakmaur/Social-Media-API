from fastapi import  APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from .. import database, schemas,models,utilis
from ..routers import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    tags=["Authentication"]
)

@router.post("/login",response_model=schemas.Token)
def log(user_credentials:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid_Credentials")
    
    if not utilis.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Incorrect Password")
    
    #create token
    # return token

    access_token=oauth2.create_access_token({"user_id":user.id})
    token_type="bearer"

    return {"access_token": access_token, "token_type": token_type}
