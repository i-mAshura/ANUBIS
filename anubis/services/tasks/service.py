import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from anubis.services.tasks.models import Task
from anubis.services.tasks.schemas import TaskCreate, TaskUpdate
from anubis.services.registry.models import Agent


class TaskService:
    @staticmethod
    def create_task(db: Session, task_in: TaskCreate) -> Task:
        agent = db.query(Agent).filter(Agent.id == task_in.root_agent_id).first()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Root agent '{task_in.root_agent_id}' does not exist in registry."
            )
        if agent.status != "active":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Agent '{agent.id}' is '{agent.status}'. Cannot initiate new tasks."
            )

        task_id = f"task_{uuid.uuid4().hex[:12]}"
        task = Task(
            id=task_id,
            root_agent_id=task_in.root_agent_id,
            on_behalf_of=task_in.on_behalf_of,
            intent=task_in.intent,
            requested_scope=task_in.requested_scope or ["tools:read"],
            status="running",
            started_at=datetime.utcnow()
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def get_task(db: Session, task_id: str) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()

    @staticmethod
    def list_tasks(
        db: Session,
        status_filter: Optional[str] = None,
        agent_id: Optional[str] = None
    ) -> List[Task]:
        query = db.query(Task)
        if status_filter:
            query = query.filter(Task.status == status_filter)
        if agent_id:
            query = query.filter(Task.root_agent_id == agent_id)
        return query.order_by(Task.started_at.desc()).all()

    @staticmethod
    def update_task(db: Session, task_id: str, update_in: TaskUpdate) -> Task:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        if update_in.status:
            task.status = update_in.status
            if update_in.status in ["completed", "failed", "cancelled"]:
                task.completed_at = datetime.utcnow()

        db.commit()
        db.refresh(task)
        return task
