from fastapi import APIRouter, Request
from db.database import direct_get_conn
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from schemas.blog_schema import Blog

# Router 생성
router = APIRouter(prefix="/blogs", tags=["blogs"])

"/blogs"
@router.get("/")
async def get_all_blogs(request: Request):
    conn = None
    try:
        conn = direct_get_conn()
        query = """
        SELECT id, title, author, content, image_loc, modified_dt FROM blog
        """
        result = conn.execute(text(query))

        rows = [Blog(id = row.id,
                     title = row.title,
                     author = row.author,
                     content = row.content,
                     image_loc = row.image_loc,
                     modified_dt = row.modified_dt) 
                     for row in result]
        result.close()
        return rows
    except SQLAlchemyError as e:
        print(e)
        raise(e)
    finally:
        if conn:
            conn.close()
