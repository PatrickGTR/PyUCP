from modules.connect_sql import MySQL

def writePost(title: str, content: str, author: int):
    with MySQL() as c:
       c.execute("INSERT INTO posts (post_title, post_content, post_date, author_id) VALUES (%s, %s, NOW(), %s)", (title, content, author))
    
def editPost(postid: int):
    with MySQL() as c:
        c.execute("SELECT post_id, post_title, post_content FROM posts WHERE post_id = %s", postid)
        result = c.fetchone()
    # returns the first result from the database.
    return result

def updatePost(content: str, title: str, postid: int):
     with MySQL() as c:
            c.execute("UPDATE posts SET post_content=%s, post_title=%s WHERE post_id=%s", (content, title, postid))

def deletePost(postid: int):
    with MySQL() as c:
        c.execute("DELETE FROM posts WHERE post_id=%s", postid)
    