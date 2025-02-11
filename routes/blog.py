from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from db.database import direct_get_conn, context_get_conn
from sqlalchemy import text, Connection
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import Blog, BlogData
from utils import util

# Router 생성
router = APIRouter(prefix="/blogs", tags=["blogs"])
# jinja2 Template 엔진 생성
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_all_blogs(request: Request):
    conn = None
    try:
        conn = direct_get_conn()
        query = """
        SELECT id, title, author, content, image_loc, modified_dt FROM blog
        """
        result = conn.execute(text(query))

        all_blogs = [BlogData(id = row.id,
                     title = row.title,
                     author = row.author,
                     content = util.truncate_text(row.content),
                     image_loc = row.image_loc,     
                     modified_dt = row.modified_dt) 
                     for row in result]
        result.close()
        return templates.TemplateResponse(
            request = request,
            name = "index.html",
            context = {"all_blogs": all_blogs}
        )
    
    except SQLAlchemyError as e:
        print(e)
        raise(e)
    finally:
        if conn:
            conn.close()


@router.get("/show/{id}")
async def get_blog_by_id(request: Request, id: int, conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        SELECT id, title, author, content, image_loc, modified_dt from blog
        where id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)

        # 만약, 한 건도 찾지 못하면 오류를 던진다
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")

        row = result.fetchone()
        blog = BlogData(id=row[0], 
                        title=row[1], 
                        author=row[2], 
                        content=util.newline_to_br(row[3]),
                        image_loc=row[4], 
                        modified_dt=row[5])
        result.close()
        return templates.TemplateResponse(
            request = request,
            name = "show_blog.html",
            context = {"blog": blog}
        )
    
    except SQLAlchemyError as e:
        print(e)
        raise(e)


@router.get("/new")
def create_blog_ui(request: Request):
    return templates.TemplateResponse(
        request = request,
        name = "new_blog.html",
        context = {}    
    )


@router.post("/new")
def create_blog(request: Request
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        INSERT INTO blog(title, author, content, modified_dt)
        VALUES ('{title}', '{author}', '{content}', now())
        """
        conn.execute(text(query))
        conn.commit()

        return RedirectResponse("/blogs", status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e:
        print(e)
        conn.rollback()         # 사실 안해도 되지만,,


@router.get("/edit/{id}")
def update_blog_ui(request: Request, id: int, conn = Depends(context_get_conn)):
    try:
        query = f"""
        SELECT id, title, author, content from blog where id = :id
        """
        stmt = text(query)
        bind_stmt = stmt.bindparams(id=id)
        result = conn.execute(bind_stmt)

        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        
        row = result.fetchone()
        
        return templates.TemplateResponse(
            request = request,
            name = "edit_blog.html",
            context = {"id": row.id, "title": row.title, "author": row.author, "content": row.content}
        )
    except SQLAlchemyError as e:
        print(e)
        raise e
    

@router.post("/edit/{id}")
def update_blog(request: Request
                , id: int
                , title = Form(min_length=2, max_length=200)
                , author = Form(max_length=100)
                , content = Form(min_length=2, max_length=4000)
                , conn: Connection = Depends(context_get_conn)):
    try:
        query = f"""
        UPDATE blog 
        SET title = :title , author= :author, content= :content
        where id = :id
        """
        bind_stmt = text(query).bindparams(id=id, title=title, 
                                           author=author, content=content)
        result = conn.execute(bind_stmt)
        # 해당 id로 데이터가 존재하지 않아 update 건수가 없으면 오류를 던진다.
        if result.rowcount == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"해당 id {id}는(은) 존재하지 않습니다.")
        conn.commit()
        return RedirectResponse(f"/blogs/show/{id}", status_code=status.HTTP_302_FOUND)
    except SQLAlchemyError as e:
        print(e)
        raise e