"""
Task management tools for Outlook MCP Server.
Provides MCP tools for managing tasks.
"""

import json
import logging
from typing import Optional, Dict, Any, List

from graph_client import graph_client

logger = logging.getLogger(__name__)


def get_tasks(folder: str = "tasks", top: int = 10) -> str:
    """
    Get tasks from a specific folder.
    
    Args:
        folder: Task folder name or ID (default: "tasks")
        top: Number of tasks to retrieve (default: 10)
    
    Returns:
        JSON string with task data
    """
    try:
        result = graph_client.get_tasks(folder=folder, top=top)
        tasks = result.get("value", [])
        
        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append({
                "id": task.get("id"),
                "subject": task.get("subject"),
                "due_date": task.get("dueDateTime", {}).get("dateTime"),
                "status": task.get("status"),
                "importance": task.get("importance"),
                "is_completed": task.get("isCompleted"),
                "body_preview": task.get("bodyPreview", "")[:200],
                "created": task.get("createdDateTime"),
                "last_modified": task.get("lastModifiedDateTime"),
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_tasks),
            "tasks": formatted_tasks,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting tasks: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def get_task(task_id: str) -> str:
    """
    Get a specific task by ID.
    
    Args:
        task_id: The ID of the task to retrieve
    
    Returns:
        JSON string with task data
    """
    try:
        result = graph_client.get_task(task_id=task_id)
        
        task = {
            "id": result.get("id"),
            "subject": result.get("subject"),
            "due_date": result.get("dueDateTime", {}).get("dateTime"),
            "status": result.get("status"),
            "importance": result.get("importance"),
            "is_completed": result.get("isCompleted"),
            "body": result.get("body", {}).get("content"),
            "created": result.get("createdDateTime"),
            "last_modified": result.get("lastModifiedDateTime"),
            "completed_date": result.get("completedDateTime"),
        }
        
        return json.dumps({
            "success": True,
            "task": task,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting task: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def create_task(subject: str, due_date: str, body: str = "") -> str:
    """
    Create a new task.
    
    Args:
        subject: Task subject/title
        due_date: Due date in ISO format (e.g., "2024-01-01T00:00:00Z")
        body: Task description/body (optional)
    
    Returns:
        JSON string with created task data
    """
    try:
        result = graph_client.create_task(subject=subject, due_date=due_date, body=body)
        
        task = {
            "id": result.get("id"),
            "subject": result.get("subject"),
            "due_date": result.get("dueDateTime", {}).get("dateTime"),
            "status": result.get("status"),
            "created": result.get("createdDateTime"),
        }
        
        return json.dumps({
            "success": True,
            "message": "Task created successfully",
            "task": task,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def update_task(task_id: str, subject: str = None, due_date: str = None, body: str = None) -> str:
    """
    Update an existing task.
    
    Args:
        task_id: The ID of the task to update
        subject: New subject (optional)
        due_date: New due date in ISO format (optional)
        body: New description/body (optional)
    
    Returns:
        JSON string with updated task data
    """
    try:
        result = graph_client.update_task(
            task_id=task_id,
            subject=subject,
            due_date=due_date,
            body=body,
        )
        
        return json.dumps({
            "success": True,
            "message": "Task updated successfully",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def complete_task(task_id: str) -> str:
    """
    Mark a task as complete.
    
    Args:
        task_id: The ID of the task to mark as complete
    
    Returns:
        JSON string with operation result
    """
    try:
        result = graph_client.complete_task(task_id=task_id)
        return json.dumps({
            "success": True,
            "message": "Task marked as complete",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error completing task: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })