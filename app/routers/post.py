from fastapi import  Response, status,HTTPException, Depends,APIRouter
from typing import  List,Optional
from . import oauth2
from sqlalchemy import func

# using orm now
from sqlalchemy.orm import Session 
from .. import schemas, models
from ..database import  get_db

router=APIRouter(
    prefix="/posts",
    tags=["Posts"]
)





@router.get("/")
async def root():
    return {"message":"Heelo "}



@router.get("/all", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10,skip:int=0,search:Optional[str]=""):
    #print(f"Fetching all posts with a limit of {limit}")

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #print(f"All posts retrieved with limit {limit}: {data}")

    if not posts:
        print("No posts found in the database")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    
    
    
    return posts

    



@router.get("/posts",response_model=List[schemas.PostOut]) 
def get_post(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute(" SELECT * FROM post")
    # post=cursor.fetchall();
    # print(post)
    # return {"post_yet":post}

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id==current_user.id).all()
    return posts




@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createpost(post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

#    cursor.execute(f"INSERT INTO post (title,content,published) VALUES ({post.title},{post.content},{post.published})")
# This can cause SQL Injection ex:- if attaker pass some injection query in title like INSERT ...


    # cursor.execute("INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING *",(post.title,post.content,post.published))

    # new_post=cursor.fetchone();
    # conn.commit();
    # return {"Post":new_post}
    # print(**post.model_dump())
    print(current_user.id)
    new_post=models.Post(
        # title=post.title,content=post.content,published=post.published not efficient way of doing this
        owner_id=current_user.id,
        **post.model_dump()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

 

@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM post WHERE id=%s ",(str(id),))
    # get_post=cursor.fetchone()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id==current_user.id,models.Post.id==id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"For this {id} nothing posted")

    return posts


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()