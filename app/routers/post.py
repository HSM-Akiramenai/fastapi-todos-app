from typing import List, Optional
from fastapi import Depends, HTTPException, status, Response, APIRouter
from app import models, oauth2, schemas
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# Path Operation to get all posts
# @router.get("/", 
#             response_model=List[schemas.PostOut])
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 3,
              skip: int = 0,
              search: Optional[str] = ""):
    
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id, models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all() 

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.owner_id == current_user.id, models.Post.title.ilike(f"%{search}%")).limit(limit).offset(skip).all()

    return [schemas.PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                published=post.published,
                created_at=post.created_at,
                owner_id=post.owner_id,
                owner=schemas.UserBase(
                    first_name=post.owner.first_name,
                    last_name=post.owner.last_name,
                    email=post.owner.email
                ),
                votes=votes
            ) for post, votes in posts]


# Path Operation to create a new post
@router.post("/", 
             status_code=status.HTTP_201_CREATED, 
             response_model=schemas.PostOut)
def create_posts(post: schemas.PostCreate, 
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# Path Operation to get a specific post by ID
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, 
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    result = db.query(models.Post, func.count(models.Vote.user_id).label("votes")) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == id) \
        .first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: '{id}' was not found.") 

    post, votes = result

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this post.") 

    # Create response model directly from SQLAlchemy model and additional data
    return schemas.PostResponse(
        **post.__dict__,
        owner=schemas.UserBase(
            first_name=post.owner.first_name,
            last_name=post.owner.last_name,
            email=post.owner.email
        ),
        votes=votes
    )

# Path Operation to delete a post by ID
@router.delete("/{id}", 
               status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, 
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: '{id}' does not exist."
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action.")
    
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Path Operation to update a post by ID
@router.put("/{id}",
            status_code=status.HTTP_200_OK, 
            response_model=schemas.PostOut)
def update_post(id: int, 
                updated_post: schemas.PostCreate, 
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)

    post = query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: '{id}' does not exist."
        )
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action.")
    
    query.update(updated_post.model_dump(), 
                 synchronize_session=False)
    
    db.commit()
    return query.first()