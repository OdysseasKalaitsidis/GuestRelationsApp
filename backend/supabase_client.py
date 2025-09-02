# Supabase Client Configuration
import os
import logging
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Supabase configuration - use ANON_KEY for now since service role key is invalid
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

# Use service role key since it's now working
SUPABASE_KEY = SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY

# Initialize Supabase client
supabase = None

def initialize_supabase():
    """Initialize Supabase client"""
    global supabase
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY/SUPABASE_ANON_KEY environment variables")
        return False
    
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized successfully")
        logger.info(f"Using key type: {'Service Role' if SUPABASE_SERVICE_ROLE_KEY else 'Anon'}")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize Supabase client: {e}")
        return False

def get_supabase():
    """Get Supabase client instance"""
    global supabase
    if supabase is None:
        if not initialize_supabase():
            raise RuntimeError("Supabase client not configured. Check environment variables.")
    return supabase

async def test_supabase_connection():
    """Test Supabase connection"""
    try:
        client = get_supabase()
        
        # Test connection by making a simple query
        response = client.table("users").select("id").limit(1).execute()
        
        logger.info("Supabase connection test successful")
        return True
    except Exception as e:
        logger.error(f"Supabase connection test failed: {e}")
        return False

# Network connectivity test as requested
def test_network_connectivity():
    """Test network connectivity to Supabase"""
    import requests
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Missing SUPABASE_URL or SUPABASE_KEY")
        return False
    
    url = SUPABASE_URL + "/rest/v1/"
    key = SUPABASE_KEY
    
    try:
        r = requests.get(url, headers={
            "apikey": key, 
            "Authorization": f"Bearer {key}"
        })
        logger.info(f"Supabase reachable, status: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        logger.error(f"Network error: {e}")
        return False
