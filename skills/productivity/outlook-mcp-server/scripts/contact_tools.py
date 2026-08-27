"""
Contact management tools for Outlook MCP Server.
Provides MCP tools for managing contacts.
"""

import json
import logging
from typing import Optional, Dict, Any, List

from graph_client import graph_client

logger = logging.getLogger(__name__)


def get_contacts(folder: str = "contacts", top: int = 10) -> str:
    """
    Get contacts from a specific folder.
    
    Args:
        folder: Contact folder name or ID (default: "contacts")
        top: Number of contacts to retrieve (default: 10)
    
    Returns:
        JSON string with contact data
    """
    try:
        result = graph_client.get_contacts(folder=folder, top=top)
        contacts = result.get("value", [])
        
        formatted_contacts = []
        for contact in contacts:
            formatted_contacts.append({
                "id": contact.get("id"),
                "display_name": contact.get("displayName"),
                "email": contact.get("emailAddresses", [{}])[0].get("address") if contact.get("emailAddresses") else None,
                "phone": contact.get("businessPhones", [None])[0] if contact.get("businessPhones") else None,
                "company": contact.get("companyName"),
                "job_title": contact.get("jobTitle"),
                "created": contact.get("createdDateTime"),
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_contacts),
            "contacts": formatted_contacts,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting contacts: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def get_contact(contact_id: str) -> str:
    """
    Get a specific contact by ID.
    
    Args:
        contact_id: The ID of the contact to retrieve
    
    Returns:
        JSON string with contact data
    """
    try:
        result = graph_client.get_contact(contact_id=contact_id)
        
        contact = {
            "id": result.get("id"),
            "display_name": result.get("displayName"),
            "email": result.get("emailAddresses", [{}])[0].get("address") if result.get("emailAddresses") else None,
            "phone": result.get("businessPhones", [None])[0] if result.get("businessPhones") else None,
            "company": result.get("companyName"),
            "job_title": result.get("jobTitle"),
            "department": result.get("department"),
            "office_location": result.get("officeLocation"),
            "business_address": result.get("businessAddress"),
            "created": result.get("createdDateTime"),
            "last_modified": result.get("lastModifiedDateTime"),
        }
        
        return json.dumps({
            "success": True,
            "contact": contact,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting contact: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def create_contact(name: str, email: str, phone: str = None) -> str:
    """
    Create a new contact.
    
    Args:
        name: Contact display name
        email: Contact email address
        phone: Contact phone number (optional)
    
    Returns:
        JSON string with created contact data
    """
    try:
        result = graph_client.create_contact(name=name, email=email, phone=phone)
        
        contact = {
            "id": result.get("id"),
            "display_name": result.get("displayName"),
            "email": result.get("emailAddresses", [{}])[0].get("address") if result.get("emailAddresses") else None,
            "phone": result.get("businessPhones", [None])[0] if result.get("businessPhones") else None,
            "created": result.get("createdDateTime"),
        }
        
        return json.dumps({
            "success": True,
            "message": "Contact created successfully",
            "contact": contact,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error creating contact: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def update_contact(contact_id: str, name: str = None, email: str = None, phone: str = None) -> str:
    """
    Update an existing contact.
    
    Args:
        contact_id: The ID of the contact to update
        name: New display name (optional)
        email: New email address (optional)
        phone: New phone number (optional)
    
    Returns:
        JSON string with updated contact data
    """
    try:
        result = graph_client.update_contact(
            contact_id=contact_id,
            name=name,
            email=email,
            phone=phone,
        )
        
        return json.dumps({
            "success": True,
            "message": "Contact updated successfully",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error updating contact: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def delete_contact(contact_id: str) -> str:
    """
    Delete a contact.
    
    Args:
        contact_id: The ID of the contact to delete
    
    Returns:
        JSON string with operation result
    """
    try:
        result = graph_client.delete_contact(contact_id=contact_id)
        return json.dumps({
            "success": True,
            "message": "Contact deleted successfully",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error deleting contact: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })