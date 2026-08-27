"""
Outreach tracking tools for Outlook MCP Server.
Provides MCP tools for tracking outreach to individuals and generating reports.
Uses SharePoint/Excel for data storage.
"""

import json
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from graph_client import graph_client
from config import get_sharepoint_config, OUTREACH_WORKSHEET_NAME

logger = logging.getLogger(__name__)


def track_outreach(name: str, email: str, status: str, notes: str = "") -> str:
    """
    Track outreach to an individual.
    
    Args:
        name: Name of the individual
        email: Email address of the individual
        status: Outreach status (e.g., "initial", "follow_up", "completed", "no_response")
        notes: Additional notes about the outreach
    
    Returns:
        JSON string with operation result
    """
    try:
        config = get_sharepoint_config()
        worksheet_name = config["worksheet_name"]
        
        # Prepare row data
        row = [
            datetime.now().isoformat(),  # Date
            name,
            email,
            status,
            notes,
            "Pending",  # Response status
            "",  # Response date
        ]
        
        result = graph_client.append_workbook_rows(sheet_name=worksheet_name, rows=[row])
        
        return json.dumps({
            "success": True,
            "message": f"Outreach tracked for {name}",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error tracking outreach: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def get_outreach_status(name: str) -> str:
    """
    Get the status of outreach to an individual.
    
    Args:
        name: Name of the individual to check
    
    Returns:
        JSON string with outreach status
    """
    try:
        config = get_sharepoint_config()
        worksheet_name = config["worksheet_name"]
        
        result = graph_client.get_workbook_rows(sheet_name=worksheet_name)
        rows = result.get("value", [])
        
        # Filter rows by name
        matching_rows = []
        for row in rows:
            if len(row) > 1 and row[1] == name:
                matching_rows.append(row)
        
        if not matching_rows:
            return json.dumps({
                "success": False,
                "error": f"No outreach records found for {name}",
            })
        
        # Get the most recent record
        latest = matching_rows[-1]
        
        return json.dumps({
            "success": True,
            "outreach": {
                "date": latest[0],
                "name": latest[1],
                "email": latest[2],
                "status": latest[3],
                "notes": latest[4],
                "response_status": latest[5],
                "response_date": latest[6],
            },
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting outreach status: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def update_outreach(name: str, status: str = None, notes: str = None) -> str:
    """
    Update outreach status for an individual.
    
    Args:
        name: Name of the individual
        status: New outreach status (optional)
        notes: New notes (optional)
    
    Returns:
        JSON string with operation result
    """
    try:
        config = get_sharepoint_config()
        worksheet_name = config["worksheet_name"]
        
        # First get current records
        result = graph_client.get_workbook_rows(sheet_name=worksheet_name)
        rows = result.get("value", [])
        
        # Find the latest record for this person
        latest_row = None
        latest_row_index = -1
        for i, row in enumerate(rows):
            if len(row) > 1 and row[1] == name:
                latest_row = row
                latest_row_index = i
        
        if latest_row is None:
            return json.dumps({
                "success": False,
                "error": f"No outreach records found for {name}",
            })
        
        # Update the record
        if status:
            latest_row[3] = status
        if notes:
            latest_row[4] = notes
        latest_row[0] = datetime.now().isoformat()  # Update date
        
        # Update the row in the worksheet
        range_address = f"A{latest_row_index + 1}:G{latest_row_index + 1}"
        result = graph_client.update_workbook_range(
            sheet_name=worksheet_name,
            range_address=range_address,
            values=[latest_row],
        )
        
        return json.dumps({
            "success": True,
            "message": f"Outreach updated for {name}",
            "result": result,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error updating outreach: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def get_outreach_report() -> str:
    """
    Generate an outreach report.
    
    Returns:
        JSON string with outreach report
    """
    try:
        config = get_sharepoint_config()
        worksheet_name = config["worksheet_name"]
        
        result = graph_client.get_workbook_rows(sheet_name=worksheet_name)
        rows = result.get("value", [])
        
        # Process data
        total = len(rows)
        statuses = {}
        for row in rows:
            if len(row) > 3:
                status = row[3] if row[3] else "Unknown"
                statuses[status] = statuses.get(status, 0) + 1
        
        # Get recent outreach (last 10)
        recent = rows[-10:] if len(rows) > 10 else rows
        
        formatted_recent = []
        for row in recent:
            formatted_recent.append({
                "date": row[0] if len(row) > 0 else "",
                "name": row[1] if len(row) > 1 else "",
                "email": row[2] if len(row) > 2 else "",
                "status": row[3] if len(row) > 3 else "",
                "notes": row[4] if len(row) > 4 else "",
                "response_status": row[5] if len(row) > 5 else "",
                "response_date": row[6] if len(row) > 6 else "",
            })
        
        report = {
            "total_outreach": total,
            "status_breakdown": statuses,
            "recent_outreach": formatted_recent,
            "generated_at": datetime.now().isoformat(),
        }
        
        return json.dumps({
            "success": True,
            "report": report,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error generating outreach report: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })


def get_outreach_list(status_filter: Optional[str] = None) -> str:
    """
    Get a list of all outreach records, optionally filtered by status.
    
    Args:
        status_filter: Filter by status (optional)
    
    Returns:
        JSON string with outreach list
    """
    try:
        config = get_sharepoint_config()
        worksheet_name = config["worksheet_name"]
        
        result = graph_client.get_workbook_rows(sheet_name=worksheet_name)
        rows = result.get("value", [])
        
        # Filter by status if provided
        if status_filter:
            rows = [row for row in rows if len(row) > 3 and row[3] == status_filter]
        
        formatted_rows = []
        for row in rows:
            formatted_rows.append({
                "date": row[0] if len(row) > 0 else "",
                "name": row[1] if len(row) > 1 else "",
                "email": row[2] if len(row) > 2 else "",
                "status": row[3] if len(row) > 3 else "",
                "notes": row[4] if len(row) > 4 else "",
                "response_status": row[5] if len(row) > 5 else "",
                "response_date": row[6] if len(row) > 6 else "",
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_rows),
            "outreach": formatted_rows,
        }, indent=2)
    
    except Exception as e:
        logger.error(f"Error getting outreach list: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
        })