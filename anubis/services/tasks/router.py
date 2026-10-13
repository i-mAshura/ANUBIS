from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from anubis.db import get_db
from anubis.services.tasks.schemas import TaskCreate, TaskResponse, TaskUpdate
from anubis.services.tasks.service import TaskService

router = APIRouter(tags=["Task Management"])


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    """Initialize a task on behalf of a human principal with an initial intent and scope boundary."""
    return TaskService.create_task(db, task_in)


@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    status: Optional[str] = Query(None, description="Filter by status: running, completed, failed, cancelled"),
    root_agent_id: Optional[str] = Query(None, description="Filter by root agent ID"),
    db: Session = Depends(get_db)
):
    """List tasks across all agent workflows."""
    return TaskService.list_tasks(db, status_filter=status, agent_id=root_agent_id)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    """Retrieve details and status for a specific task."""
    task = TaskService.get_task(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_id}' not found."
        )
    return TaskResponse.model_validate(task)


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, update_in: TaskUpdate, db: Session = Depends(get_db)):
    """Update task lifecycle status (completed, failed, cancelled)."""
    return TaskService.update_task(db, task_id, update_in)
