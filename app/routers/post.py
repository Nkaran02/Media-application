from fastapi import requests,responses,Request, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    tags=['Posts']
)

@router.get("/posts",status_code=201, response_model=list[schemas.ReturnResponse])
def get_posts(db: Session = Depends(get_db),limit: int = 10, skip:int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/createposts", status_code=201, response_model=schemas.ReturnResponse)
def create_posts(post : schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title= post.title, content = post.content, relesed = post.relesed, modified = post.modified) instead of this which is inefficient for long model do unpacking
    print(current_user.email)
    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # to get the newely created data
    return new_post


@router.get("/posts/{id}", response_model=schemas.ReturnResponse)
def get_posts_of_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_by_id =  db.query(models.Post).filter(models.Post.id == id).first()
    return post_by_id


@router.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    delete_post = post.first()

    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with {id} dosent exists")
    
    if delete_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authoriaes to delete other post")
    
    delete_post.delete(synchronize_session=False)
    db.commit()


@router.put("/update_post/{id}")
def update_post(id: int, post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id {id} doesnt exists ")
    
    if update_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authoriaes to update other post")
    
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return{"data":f"successfully updated post with id {id}"}
