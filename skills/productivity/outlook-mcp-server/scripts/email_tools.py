"""
Email management tools for Outlook MCP Server.
Provides MCP tools for reading, organizing, creating, and searching emails.
"""

import json
import logging
from typing import Optional, Dict, Any

from graph_client import graph_client

logger = logging.getLogger(__name__)


def get_emails(folder: str = "inbox", top: int = 10, filter_query: Optional[str] = None) -> str:
    """
    Read emails from Outlook.
    
    Args:
        folder: Mail folder name or ID (default: "inbox")
        top: Number of emails to retrieve (default: 10)
        filter_query: OData filter query (optional)
    
    Returns:
        JSON string with email data
    """
    try:
        result = graph_client.get_emails(folder=folder, top=top, filter_query=filter_query)
        emails = result.get("value", [])
        
        formatted_emails = []
        for email in emails:
            formatted_emails.append({
                "id": email.get("id"),
                "subject": email.get("subject"),
                "from": email.get("from", {}).get("emailAddress", {}).get("address"),
                "from_name": email.get("from", {}).get("emailAddress", {}).get("name"),
                "to": [r.get("emailAddress", {}).get("address") for r in email.get("toRecipients", [])],
                "received": email.get("receivedDateTime"),
                "is_read": email.get("isRead"),
                "body_preview": email.get("bodyPreview", "")[:200],
                "importance": email.get("importance"),
                "has_attachments": email.get("hasAttachments"),
                "conversation_id": email.get("conversationId"),
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_emails),
            "emails": formatted_emails,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting emails: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def organize_emails(email_id: str, folder_id: str) -> str:
    """
    Move an email to a specific folder.
    
    Args:
        email_id: The ID of the email to move
        folder_id: The ID of the destination folder
    
    Returns:
        JSON string with operation result
    """
    try:
        result = graph_client.organize_emails(email_id=email_id, folder_id=folder_id)
        return json.dumps({
            "success": True,
            "message": f"Email moved to folder {folder_id}",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error organizing email: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def create_email(to: list, subject: str, body: str, cc: Optional[list] = None) -> str:
    """
    Create and send an email.
    
    Args:
        to: List of recipient email addresses
        subject: Email subject
        body: Email body (HTML)
        cc: List of CC recipient email addresses (optional)
    
    Returns:
        JSON string with operation result
    """
    try:
        result = graph_client.create_email(to=to, subject=subject, body=body, cc=cc)
        return json.dumps({
            "success": True,
            "message": "Email sent successfully",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error creating email: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def search_emails(query: str, folder: str = "inbox") -> str:
    """
    Search emails by query.
    
    Args:
        query: Search query string
        folder: Mail folder to search in (default: "inbox")
    
    Returns:
        JSON string with search results
    """
    try:
        result = graph_client.search_emails(query=query, folder=folder)
        emails = result.get("value", [])
        
        formatted_emails = []
        for email in emails:
            formatted_emails.append({
                "id": email.get("id"),
                "subject": email.get("subject"),
                "from": email.get("from", {}).get("emailAddress", {}).get("address"),
                "from_name": email.get("from", {}).get("emailAddress", {}).get("name"),
                "received": email.get("receivedDateTime"),
                "is_read": email.get("isRead"),
                "body_preview": email.get("bodyPreview", "")[:200],
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_emails),
            "emails": formatted_emails,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error searching emails: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def get_mail_folders() -> str:
    """
    Get all mail folders.
    
    Returns:
        JSON string with folder list
    """
    try:
        result = graph_client.get_mail_folders()
        folders = result.get("value", [])
        
        formatted_folders = []
        for folder in folders:
            formatted_folders.append({
                "id": folder.get("id"),
                "display_name": folder.get("displayName"),
                "total_item_count": folder.get("totalItemCount"),
                "unread_item_count": folder.get("unreadItemCount"),
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_folders),
            "folders": formatted_folders,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting mail folders: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def get_email(email_id: str) -> str:
    """
    Get a specific email by ID.
    
    Args:
        email_id: The ID of the email to retrieve
    
    Returns:
        JSON string with email data
    """
    try:
        result = graph_client.get_email(email_id=email_id)
        
        email = {
            "id": result.get("id"),
            "subject": result.get("subject"),
            "from": result.get("from", {}).get("emailAddress", {}).get("address"),
            "from_name": result.get("from", {}).get("emailAddress", {}).get("name"),
            "to": [r.get("emailAddress", {}).get("address") for r in result.get("toRecipients", [])],
            "received": result.get("receivedDateTime"),
            "is_read": result.get("isRead"),
            "body": result.get("body", {}).get("content"),
            "importance": result.get("importance"),
            "has_attachments": result.get("hasAttachments"),
            "conversation_id": result.get("conversationId"),
        }
        
        return json.dumps({
            "success": True,
            "email": email,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting email: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })