"""
Authentication module for Outlook MCP Server.
Uses MSAL (Microsoft Authentication Library) for OAuth2 authentication with Microsoft Graph API.
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

import msal
from config import (
    AZURE_CLIENT_ID,
    AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET,
    GRAPH_API_SCOPES,
    TOKEN_CACHE_FILE,
    ensure_cache_dir,
)

logger = logging.getLogger(__name__)


class OutlookAuth:
    """Handles OAuth2 authentication with Microsoft Graph API using MSAL."""

    def __init__(self):
        self.client_id = AZURE_CLIENT_ID
        self.tenant_id = AZURE_TENANT_ID
        self.client_secret = AZURE_CLIENT_SECRET
        self.scopes = GRAPH_API_SCOPES
        self.cache = self._load_cache()
        self.app = self._build_app()
        self._accounts = None

    def _load_cache(self) -> msal.SerializableTokenCache:
        """Load the token cache from disk."""
        cache = msal.SerializableTokenCache()
        if TOKEN_CACHE_FILE.exists():
            try:
                cache.deserialize(TOKEN_CACHE_FILE.read_text(encoding="utf-8"))
                logger.debug("Token cache loaded successfully.")
            except Exception as e:
                logger.warning(f"Failed to load token cache: {e}")
        return cache

    def _save_cache(self):
        """Save the token cache to disk."""
        ensure_cache_dir()
        if self.cache.has_state_changed:
            TOKEN_CACHE_FILE.write_text(
                self.cache.serialize(), encoding="utf-8"
            )
            logger.debug("Token cache saved successfully.")

    def _build_app(self) -> msal.ConfidentialClientApplication:
        """Build the MSAL confidential client application."""
        if not self.client_id or not self.tenant_id:
            raise ValueError(
                "AZURE_CLIENT_ID and AZURE_TENANT_ID must be set."
            )

        return msal.ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}",
            token_cache=self.cache,
        )

    def get_accounts(self) -> list:
        """Get all accounts from the cache."""
        if self._accounts is None:
            self._accounts = self.app.get_accounts()
        return self._accounts

    def acquire_token_silent(self, scopes: Optional[list] = None) -> Optional[Dict[str, Any]]:
        """Try to acquire token silently from cache."""
        scopes = scopes or self.scopes
        accounts = self.get_accounts()
        
        if not accounts:
            logger.debug("No accounts found in cache.")
            return None

        result = self.app.acquire_token_silent(
            scopes=scopes,
            account=accounts[0],
        )
        
        if result and "access_token" in result:
            self._save_cache()
            return result
        
        return None

    def acquire_token_interactive(self, scopes: Optional[list] = None) -> Optional[Dict[str, Any]]:
        """Acquire token interactively (requires user consent)."""
        scopes = scopes or self.scopes
        
        result = self.app.acquire_token_interactive(
            scopes=scopes,
            prompt="consent",
        )
        
        if result and "access_token" in result:
            self._save_cache()
            self._accounts = self.app.get_accounts()
            return result
        
        logger.error(f"Interactive auth failed: {result.get('error_description', 'Unknown error')}")
        return None

    def acquire_token_with_client_credentials(self, scopes: Optional[list] = None) -> Optional[Dict[str, Any]]:
        """Acquire token using client credentials (for app-only access)."""
        scopes = scopes or self.scopes
        
        result = self.app.acquire_token_for_client(
            scopes=scopes,
        )
        
        if result and "access_token" in result:
            self._save_cache()
            return result
        
        logger.error(f"Client credentials auth failed: {result.get('error_description', 'Unknown error')}")
        return None

    def get_access_token(self, scopes: Optional[list] = None) -> Optional[str]:
        """Get a valid access token, trying silent first, then interactive."""
        scopes = scopes or self.scopes
        
        # Try silent acquisition first
        result = self.acquire_token_silent(scopes)
        if result:
            return result["access_token"]
        
        # Try client credentials (for app-only scenarios)
        if self.client_secret:
            result = self.acquire_token_with_client_credentials(scopes)
            if result:
                return result["access_token"]
        
        # Fall back to interactive auth
        result = self.acquire_token_interactive(scopes)
        if result:
            return result["access_token"]
        
        logger.error("Failed to acquire access token.")
        return None

    def is_authenticated(self) -> bool:
        """Check if we have a valid access token."""
        token = self.get_access_token()
        return token is not None

    def clear_cache(self):
        """Clear the token cache."""
        self.cache = msal.SerializableTokenCache()
        if TOKEN_CACHE_FILE.exists():
            TOKEN_CACHE_FILE.unlink()
        self._accounts = None
        logger.info("Token cache cleared.")


# Global auth instance
auth = OutlookAuth()