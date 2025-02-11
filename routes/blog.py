from fastapi import APIRouter, Request, Depends, status
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
