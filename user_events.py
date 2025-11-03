#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from typing import Optional, Dict, Any
from supabase import create_client, Client

logger = logging.getLogger(__name__)

# Supabase config
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY') or os.getenv('SUPABASE_KEY') or ''

_supabase: Optional[Client] = None

def _get_client() -> Optional[Client]:
    global _supabase
    if _supabase is not None:
        return _supabase
    try:
        if not SUPABASE_URL or not SUPABASE_KEY:
            logger.warning("Supabase credentials missing; user_events logging disabled")
            return None
        _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        return _supabase
    except Exception as e:
        logger.error(f"Failed to init Supabase client for user_events: {e}")
        return None

def log_user_event(user_id: str, event_type: str, source: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> None:
    """Log a user event to Supabase user_events table. Best-effort; non-blocking on failure."""
    try:
        client = _get_client()
        if client is None:
            return
        payload = {
            'user_id': user_id,
            'event_type': event_type,
            'source': source,
            'metadata': metadata or {}
        }
        client.table('user_events').insert(payload).execute()
        logger.info(f"📝 user_event logged: {user_id} {event_type} from {source}")
    except Exception as e:
        logger.warning(f"Failed to log user_event ({event_type}) for {user_id}: {e}")



