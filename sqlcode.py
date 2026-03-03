from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from fastapi import requests,responses,Request, Response, status, HTTPException, Depends
import psycopg2
import time 
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    relesed: bool = True
    modified : Optional[str] = None

class UpdatePost(BaseModel):
    title : str
    content : str
    relesed: bool = True
    modified : Optional[str] = None

while True:
    try:
        conn = psycopg2.connect(
            host='localhost', 
            database='media', user='postgres', 
            password='Newpassword@123', 
            cursor_factory=RealDictCursor
            )
        cursor = conn.cursor()
        print("Database connections was successfull")
        break
    except Exception as error:
        print("Connection failed ", error)
        time.sleep(2)



@app.get("/")
def display():
    return {"message":"hello world"}



@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts =cursor.fetchall()
    return {'data': posts}

@app.post("/createposts", status_code=201)
def create_posts(posts:Post):
    cursor.execute(""" INSERT INTO posts (title, content, relesed, modified) values (%s, %s, %s,%s) RETURNING * """, 
                    (posts.title, posts.content, posts.relesed, posts.modified)
                )
    new_post = cursor.fetchall()
    conn.commit()

    return {"data": new_post}



@app.get("/posts/{id}")
def get_posts_of_id(id: int):
    cursor.execute(""" SELECT * FROM posts where id = %s """, (str(id)))
    post_by_id = cursor.fetchone()
    return post_by_id


@app.delete("/delete_posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with {id} was dosent exists")
    return Response(detail = f"post with id {id} was deleted successfully.")



@app.put("/update_post/{id}")
def update_post(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, modified = %s, relesed = %s WHERE id = %s RETURNING *""" ,
                   (post.title, post.content, post.modified, post.relesed, id)
                   )
    
    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the post with id {id} doesnt exists ")
    return {"data": updated_post}

    
