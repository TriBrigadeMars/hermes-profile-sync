"""
Microsoft Graph API client for Outlook MCP Server.
Provides methods to interact with Microsoft Graph API for email, calendar, tasks, contacts, and SharePoint.
"""

import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

import requests
from auth import auth
from config import GRAPH_API_BASE_URL, get_sharepoint_config

logger = logging.getLogger(__name__)


class GraphClient:
    """Microsoft Graph API client."""

    def __init__(self):
        self.base_url = GRAPH_API_BASE_URL
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """Set up the requests session with authentication headers."""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _get_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        token = auth.get_access_token()
        if not token:
            raise ValueError("No access token available. Please authenticate first.")
        
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the Microsoft Graph API."""
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                **kwargs,
            )
            response.raise_for_status()
            
            if response.status_code == 204:
                return {"success": True, "status": "no_content"}
            
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            error_detail = {
                "status_code": e.response.status_code,
                "url": url,
                "method": method,
                "error": str(e),
            }
            try:
                error_detail["response"] = e.response.json()
            except Exception:
                error_detail["response"] = e.response.text
            
            logger.error(f"HTTP Error: {error_detail}")
            raise Exception(f"Graph API Error: {error_detail}")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Error: {e}")
            raise Exception(f"Request failed: {e}")

    # ==================== EMAIL METHODS ====================

    def get_emails(self, folder: str = "inbox", top: int = 10, filter_query: Optional[str] = None) -> Dict[str, Any]:
        """Get emails from a specific folder."""
        endpoint = f"/me/mailFolders/{folder}/messages"
        params = {"$top": top}
        if filter_query:
            params["$filter"] = filter_query
        
        return self._request("GET", endpoint, params=params)

    def get_email(self, email_id: str) -> Dict[str, Any]:
        """Get a specific email by ID."""
        endpoint = f"/me/messages/{email_id}"
        return self._request("GET", endpoint)

    def organize_emails(self, email_id: str, folder_id: str) -> Dict[str, Any]:
        """Move an email to a specific folder."""
        endpoint = f"/me/messages/{email_id}/move"
        data = {"destinationId": folder_id}
        return self._request("POST", endpoint, json=data)

    def create_email(self, to: List[str], subject: str, body: str, cc: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create and send an email."""
        endpoint = "/me/sendMail"
        email = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": body,
                },
                "toRecipients": [{"emailAddress": {"address": addr}} for addr in to],
            },
            "saveToSentItems": True,
        }
        if cc:
            email["message"]["ccRecipients"] = [{"emailAddress": {"address": addr}} for addr in cc]
        
        return self._request("POST", endpoint, json=email)

    def search_emails(self, query: str, folder: str = "inbox") -> Dict[str, Any]:
        """Search emails by query."""
        endpoint = f"/me/mailFolders/{folder}/messages"
        params = {"$search": query, "$top": 20}
        return self._request("GET", endpoint, params=params)

    def get_mail_folders(self) -> Dict[str, Any]:
        """Get all mail folders."""
        endpoint = "/me/mailFolders"
        return self._request("GET", endpoint)

    def get_mail_folder(self, folder_id: str) -> Dict[str, Any]:
        """Get a specific mail folder."""
        endpoint = f"/me/mailFolders/{folder_id}"
        return self._request("GET", endpoint)

    # ==================== CALENDAR METHODS ====================

    def get_calendar_events(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get calendar events within a date range."""
        endpoint = "/me/events"
        params = {
            "$filter": f"start/dateTime ge '{start_date}' and end/dateTime le '{end_date}'",
            "$orderby": "start/dateTime",
            "$top": 50,
        }
        return self._request("GET", endpoint, params=params)

    def get_calendar_event(self, event_id: str) -> Dict[str, Any]:
        """Get a specific calendar event by ID."""
        endpoint = f"/me/events/{event_id}"
        return self._request("GET", endpoint)

    def create_calendar_event(self, subject: str, start: str, end: str, location: str = "", attendees: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a calendar event."""
        endpoint = "/me/events"
        event = {
            "subject": subject,
            "start": {
                "dateTime": start,
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end,
                "timeZone": "UTC",
            },
        }
        if location:
            event["location"] = {"displayName": location}
        if attendees:
            event["attendees"] = [
                {"emailAddress": {"address": addr}, "type": "required"}
                for addr in attendees
            ]
        
        return self._request("POST", endpoint, json=event)

    def update_calendar_event(self, event_id: str, subject: str = None, start: str = None, end: str = None, location: str = None) -> Dict[str, Any]:
        """Update a calendar event."""
        endpoint = f"/me/events/{event_id}"
        data = {}
        if subject:
            data["subject"] = subject
        if start:
            data["start"] = {"dateTime": start, "timeZone": "UTC"}
        if end:
            data["end"] = {"dateTime": end, "timeZone": "UTC"}
        if location:
            data["location"] = {"displayName": location}
        
        return self._request("PATCH", endpoint, json=data)

    def delete_calendar_event(self, event_id: str) -> Dict[str, Any]:
        """Delete a calendar event."""
        endpoint = f"/me/events/{event_id}"
        return self._request("DELETE", endpoint)

    # ==================== TASK METHODS ====================

    def get_tasks(self, folder: str = "tasks", top: int = 10) -> Dict[str, Any]:
        """Get tasks from a specific folder."""
        endpoint = f"/me/outlook/tasks"
        params = {"$top": top}
        return self._request("GET", endpoint, params=params)

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Get a specific task by ID."""
        endpoint = f"/me/outlook/tasks/{task_id}"
        return self._request("GET", endpoint)

    def create_task(self, subject: str, due_date: str, body: str = "") -> Dict[str, Any]:
        """Create a new task."""
        endpoint = "/me/outlook/tasks"
        task = {
            "subject": subject,
            "dueDateTime": {"dateTime": due_date, "timeZone": "UTC"},
            "body": {"contentType": "HTML", "content": body},
        }
        return self._request("POST", endpoint, json=task)

    def update_task(self, task_id: str, subject: str = None, due_date: str = None, body: str = None) -> Dict[str, Any]:
        """Update an existing task."""
        endpoint = f"/me/outlook/tasks/{task_id}"
        data = {}
        if subject:
            data["subject"] = subject
        if due_date:
            data["dueDateTime"] = {"dateTime": due_date, "timeZone": "UTC"}
        if body is not None:
            data["body"] = {"contentType": "HTML", "content": body}
        
        return self._request("PATCH", endpoint, json=data)

    def complete_task(self, task_id: str) -> Dict[str, Any]:
        """Mark a task as complete."""
        endpoint = f"/me/outlook/tasks/{task_id}/complete"
        return self._request("POST", endpoint)

    def delete_task(self, task_id: str) -> Dict[str, Any]:
        """Delete a task."""
        endpoint = f"/me/outlook/tasks/{task_id}"
        return self._request("DELETE", endpoint)

    # ==================== CONTACT METHODS ====================

    def get_contacts(self, folder: str = "contacts", top: int = 10) -> Dict[str, Any]:
        """Get contacts from a specific folder."""
        endpoint = f"/me/contacts"
        params = {"$top": top}
        return self._request("GET", endpoint, params=params)

    def get_contact(self, contact_id: str) -> Dict[str, Any]:
        """Get a specific contact by ID."""
        endpoint = f"/me/contacts/{contact_id}"
        return self._request("GET", endpoint)

    def create_contact(self, name: str, email: str, phone: str = None) -> Dict[str, Any]:
        """Create a new contact."""
        endpoint = "/me/contacts"
        contact = {
            "displayName": name,
            "emailAddresses": [{"address": email, "name": name}],
        }
        if phone:
            contact["businessPhones"] = [phone]
        
        return self._request("POST", endpoint, json=contact)

    def update_contact(self, contact_id: str, name: str = None, email: str = None, phone: str = None) -> Dict[str, Any]:
        """Update an existing contact."""
        endpoint = f"/me/contacts/{contact_id}"
        data = {}
        if name:
            data["displayName"] = name
        if email:
            data["emailAddresses"] = [{"address": email, "name": name or ""}]
        if phone:
            data["businessPhones"] = [phone]
        
        return self._request("PATCH", endpoint, json=data)

    def delete_contact(self, contact_id: str) -> Dict[str, Any]:
        """Delete a contact."""
        endpoint = f"/me/contacts/{contact_id}"
        return self._request("DELETE", endpoint)

    # ==================== SHAREPOINT METHODS ====================

    def get_sharepoint_site(self) -> Dict[str, Any]:
        """Get SharePoint site information."""
        config = get_sharepoint_config()
        endpoint = f"/sites/{config['site_id']}"
        return self._request("GET", endpoint)

    def get_sharepoint_drive(self) -> Dict[str, Any]:
        """Get SharePoint drive information."""
        config = get_sharepoint_config()
        endpoint = f"/sites/{config['site_id']}/drives/{config['drive_id']}"
        return self._request("GET", endpoint)

    def get_workbook_sheet(self, sheet_name: str) -> Dict[str, Any]:
        """Get a worksheet from a SharePoint workbook."""
        config = get_sharepoint_config()
        endpoint = f"/sites/{config['site_id']}/drives/{config['drive_id']}/root:/{config['workbook_path']}:/workbook/worksheets('{sheet_name}')"
        return self._request("GET", endpoint)

    def get_workbook_rows(self, sheet_name: str) -> Dict[str, Any]:
        """Get rows from a worksheet."""
        config = get_sharepoint_config()
        endpoint = f"/sites/{config['site_id']}/drives/{config['drive_id']}/root:/{config['workbook_path']}:/workbook/worksheets('{sheet_name}')/usedRange/rows"
        return self._request("GET", endpoint)

    def append_workbook_rows(self, sheet_name: str, rows: List[List[Any]]) -> Dict[str, Any]:
        """Append rows to a worksheet."""
        config = get_sharepoint_config()
        endpoint = f"/sites/{config['site_id']}/drives/{config['drive_id']}/root:/{config['workbook_path']}:/workbook/worksheets('{sheet_name}')/usedRange/rows"
        data = {"values": rows}
        return self._request("POST", endpoint, json=data)

    def update_workbook_range(self, sheet_name: str, range_address: str, values: List[List[Any]]) -> Dict[str, Any]:
        """Update a range in a worksheet."""
        config = get_sharepoint_config()
        endpoint = f"/sites/{config['site_id']}/drives/{config['drive_id']}/root:/{config['workbook_path']}:/workbook/worksheets('{sheet_name}')/range(address='{range_address}')"
        data = {"values": values}
        return self._request("PATCH", endpoint, json=data)


# Global client instance
graph_client = GraphClient()