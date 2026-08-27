"""
Calendar management tools for Outlook MCP Server.
Provides MCP tools for managing calendar events.
"""

import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from graph_client import graph_client

logger = logging.getLogger(__name__)


def get_calendar_events(start_date: str, end_date: str) -> str:
    """
    Get calendar events within a date range.
    
    Args:
        start_date: Start date in ISO format (e.g., "2024-01-01T00:00:00Z")
        end_date: End date in ISO format (e.g., "2024-01-31T23:59:59Z")
    
    Returns:
        JSON string with calendar events
    """
    try:
        result = graph_client.get_calendar_events(start_date=start_date, end_date=end_date)
        events = result.get("value", [])
        
        formatted_events = []
        for event in events:
            formatted_events.append({
                "id": event.get("id"),
                "subject": event.get("subject"),
                "start": event.get("start", {}).get("dateTime"),
                "end": event.get("end", {}).get("dateTime"),
                "location": event.get("location", {}).get("displayName"),
                "attendees": [
                    a.get("emailAddress", {}).get("address")
                    for a in event.get("attendees", [])
                ],
                "is_all_day": event.get("isAllDay"),
                "status": event.get("showAs"),
                "web_link": event.get("webLink"),
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_events),
            "events": formatted_events,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting calendar events: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def get_calendar_event(event_id: str) -> str:
    """
    Get a specific calendar event by ID.
    
    Args:
        event_id: The ID of the event to retrieve
    
    Returns:
        JSON string with event data
    """
    try:
        result = graph_client.get_calendar_event(event_id=event_id)
        
        event = {
            "id": result.get("id"),
            "subject": result.get("subject"),
            "start": result.get("start", {}).get("dateTime"),
            "end": result.get("end", {}).get("dateTime"),
            "location": result.get("location", {}).get("displayName"),
            "attendees": [
                a.get("emailAddress", {}).get("address")
                for a in result.get("attendees", [])
            ],
            "is_all_day": result.get("isAllDay"),
            "status": result.get("showAs"),
            "body": result.get("body", {}).get("content"),
            "web_link": result.get("webLink"),
            "recurrence": result.get("recurrence"),
        }
        
        return json.dumps({
            "success": True,
            "event": event,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting calendar event: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def create_calendar_event(subject: str, start: str, end: str, location: str = "", attendees: Optional[List[str]] = None) -> str:
    """
    Create a calendar event.
    
    Args:
        subject: Event subject/title
        start: Start time in ISO format (e.g., "2024-01-01T10:00:00Z")
        end: End time in ISO format (e.g., "2024-01-01T11:00:00Z")
        location: Event location (optional)
        attendees: List of attendee email addresses (optional)
    
    Returns:
        JSON string with created event data
    """
    try:
        result = graph_client.create_calendar_event(
            subject=subject,
            start=start,
            end=end,
            location=location,
            attendees=attendees,
        )
        
        event = {
            "id": result.get("id"),
            "subject": result.get("subject"),
            "start": result.get("start", {}).get("dateTime"),
            "end": result.get("end", {}).get("dateTime"),
            "location": result.get("location", {}).get("displayName"),
            "web_link": result.get("webLink"),
        }
        
        return json.dumps({
            "success": True,
            "message": "Calendar event created successfully",
            "event": event,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error creating calendar event: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def update_calendar_event(event_id: str, subject: str = None, start: str = None, end: str = None, location: str = None) -> str:
    """
    Update a calendar event.
    
    Args:
        event_id: The ID of the event to update
        subject: New subject (optional)
        start: New start time in ISO format (optional)
        end: New end time in ISO format (optional)
        location: New location (optional)
    
    Returns:
        JSON string with updated event data
    """
    try:
        result = graph_client.update_calendar_event(
            event_id=event_id,
            subject=subject,
            start=start,
            end=end,
            location=location,
        )
        
        return json.dumps({
            "success": True,
            "message": "Calendar event updated successfully",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error updating calendar event: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def delete_calendar_event(event_id: str) -> str:
    """
    Delete a calendar event.
    
    Args:
        event_id: The ID of the event to delete
    
    Returns:
        JSON string with operation result
    """
    try:
        result = graph_client.delete_calendar_event(event_id=event_id)
        return json.dumps({
            "success": True,
            "message": "Calendar event deleted successfully",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error deleting calendar event: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })