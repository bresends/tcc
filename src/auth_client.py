import os
import json
import time
import base64
import requests
from typing import Optional
from datetime import datetime, timedelta


class OAuth2Client:
    def __init__(self, client_id: str, client_secret: str, token_endpoint: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self._access_token = None
        self._token_expires_at = None
        
    def _encode_credentials(self) -> str:
        """Encode client credentials for Basic Auth"""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()
        return f"Basic {encoded}"
    
    def _is_token_expired(self) -> bool:
        """Check if current token is expired or about to expire"""
        if not self._access_token or not self._token_expires_at:
            return True
        
        # Add 30 seconds buffer before actual expiration
        buffer_time = timedelta(seconds=30)
        return datetime.now() >= (self._token_expires_at - buffer_time)
    
    def _parse_token_expiration(self, token: str) -> Optional[datetime]:
        """Parse JWT token to get expiration time"""
        try:
            # JWT tokens have 3 parts separated by dots
            parts = token.split('.')
            if len(parts) != 3:
                return None
            
            # Decode payload (second part)
            payload = parts[1]
            # Add padding if needed
            payload += '=' * (4 - len(payload) % 4)
            decoded = base64.b64decode(payload)
            jwt_payload = json.loads(decoded)
            
            # Get expiration timestamp
            exp = jwt_payload.get('exp')
            if exp:
                return datetime.fromtimestamp(exp)
                
        except Exception:
            # If parsing fails, use default expiration
            pass
        
        # Default to 1 hour from now if we can't parse
        return datetime.now() + timedelta(hours=1)
    
    def _fetch_new_token(self) -> str:
        """Fetch a new access token using Client Credentials flow"""
        headers = {
            'Authorization': self._encode_credentials(),
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        data = {
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(
            self.token_endpoint,
            headers=headers,
            data=data,
            timeout=30
        )
        
        response.raise_for_status()
        token_data = response.json()
        
        access_token = token_data['access_token']
        self._access_token = access_token
        self._token_expires_at = self._parse_token_expiration(access_token)
        
        return access_token
    
    def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary"""
        if self._is_token_expired():
            return self._fetch_new_token()
        
        return self._access_token


def create_oauth_client() -> OAuth2Client:
    """Create OAuth2 client from environment variables"""
    client_id = os.getenv('NORMA_OAUTH_CLIENT_ID')
    client_secret = os.getenv('NORMA_OAUTH_CLIENT_SECRET')
    token_endpoint = os.getenv('NORMA_OAUTH_TOKEN_ENDPOINT', 'https://api.go.gov.br/token')

    if not client_id or not client_secret:
        raise ValueError(
            "Missing OAuth2 credentials. Please set NORMA_OAUTH_CLIENT_ID and NORMA_OAUTH_CLIENT_SECRET environment variables."
        )

    return OAuth2Client(client_id, client_secret, token_endpoint)


# Global OAuth client instance
_oauth_client = None

def get_oauth_client() -> OAuth2Client:
    """Get singleton OAuth2 client"""
    global _oauth_client
    if _oauth_client is None:
        _oauth_client = create_oauth_client()
    return _oauth_client


def get_access_token() -> str:
    """Get current access token"""
    return get_oauth_client().get_access_token()


# Example usage and testing
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    try:
        token = get_access_token()
        print(f"Access token obtained: {token[:50]}...")
        
        # Test that we can get it again (should use cached version)
        token2 = get_access_token()
        print(f"Second call (cached): {token2[:50]}...")
        print(f"Same token: {token == token2}")
        
    except Exception as e:
        print(f"Error: {e}")