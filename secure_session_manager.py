#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全的Session管理系統
- JWT token生成和驗證
- HttpOnly Cookie設置
- 刷新機制
- 安全標頭
"""

import os
import jwt
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from flask import Response, request, session
import logging

logger = logging.getLogger(__name__)

class SecureSessionManager:
    """安全的Session管理器"""
    
    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = secret_key or os.getenv('JWT_SECRET_KEY', secrets.token_hex(32))
        self.algorithm = 'HS256'
        self.access_token_expire_minutes = 15  # 15分鐘
        self.refresh_token_expire_days = 7     # 7天
    
    def create_access_token(self, user_id: str, additional_claims: Optional[Dict] = None) -> str:
        """創建訪問token"""
        now = datetime.utcnow()
        payload = {
            'sub': user_id,  # subject (user ID)
            'iat': now,      # issued at
            'exp': now + timedelta(minutes=self.access_token_expire_minutes),
            'type': 'access'
        }
        
        if additional_claims:
            payload.update(additional_claims)
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """創建刷新token"""
        now = datetime.utcnow()
        payload = {
            'sub': user_id,
            'iat': now,
            'exp': now + timedelta(days=self.refresh_token_expire_days),
            'type': 'refresh',
            'jti': secrets.token_hex(16)  # JWT ID for revocation
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str, token_type: str = 'access') -> Optional[Dict[str, Any]]:
        """驗證token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # 檢查token類型
            if payload.get('type') != token_type:
                logger.warning(f"❌ Token類型不匹配: expected {token_type}, got {payload.get('type')}")
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("❌ Token已過期")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"❌ 無效token: {e}")
            return None
    
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        """使用刷新token獲取新的訪問token"""
        payload = self.verify_token(refresh_token, 'refresh')
        if not payload:
            return None
        
        user_id = payload.get('sub')
        if not user_id:
            return None
        
        return self.create_access_token(user_id)
    
    def set_secure_cookies(self, response: Response, access_token: str, refresh_token: str) -> Response:
        """設置安全的Cookie"""
        # 設置訪問token cookie
        response.set_cookie(
            'access_token',
            access_token,
            max_age=self.access_token_expire_minutes * 60,
            httponly=True,
            secure=True,  # 只在HTTPS下傳輸
            samesite='Lax',
            path='/'
        )
        
        # 設置刷新token cookie
        response.set_cookie(
            'refresh_token',
            refresh_token,
            max_age=self.refresh_token_expire_days * 24 * 60 * 60,
            httponly=True,
            secure=True,
            samesite='Lax',
            path='/'
        )
        
        return response
    
    def clear_cookies(self, response: Response) -> Response:
        """清除Cookie"""
        response.set_cookie('access_token', '', expires=0, path='/')
        response.set_cookie('refresh_token', '', expires=0, path='/')
        return response
    
    def get_user_from_request(self) -> Optional[str]:
        """從請求中獲取用戶ID"""
        # 優先從Cookie獲取
        access_token = request.cookies.get('access_token')
        if access_token:
            payload = self.verify_token(access_token, 'access')
            if payload:
                return payload.get('sub')
        
        # 嘗試刷新token
        refresh_token = request.cookies.get('refresh_token')
        if refresh_token:
            new_access_token = self.refresh_access_token(refresh_token)
            if new_access_token:
                # 這裡可以設置新的cookie，但需要response對象
                # 暫時返回用戶ID
                payload = self.verify_token(new_access_token, 'access')
                if payload:
                    return payload.get('sub')
        
        return None
    
    def require_auth(self, f):
        """認證裝飾器"""
        from functools import wraps
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id = self.get_user_from_request()
            if not user_id:
                return {'error': '未認證'}, 401
            
            # 將用戶ID添加到請求上下文
            request.current_user_id = user_id
            return f(*args, **kwargs)
        
        return decorated_function

# 安全標頭設置
def set_security_headers(response: Response) -> Response:
    """設置安全標頭"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; connect-src 'self' https://ciqlfqfgzqqgdrogedxg.supabase.co;"
    
    return response

# 測試函數
def test_session_manager():
    """測試Session管理器"""
    print("🧪 測試安全Session管理器")
    
    manager = SecureSessionManager()
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    # 測試創建token
    print("1. 測試創建token...")
    access_token = manager.create_access_token(test_user_id)
    refresh_token = manager.create_refresh_token(test_user_id)
    
    print(f"✅ Access token: {access_token[:50]}...")
    print(f"✅ Refresh token: {refresh_token[:50]}...")
    
    # 測試驗證token
    print("2. 測試驗證token...")
    payload = manager.verify_token(access_token, 'access')
    if payload and payload.get('sub') == test_user_id:
        print("✅ Token驗證成功")
    else:
        print("❌ Token驗證失敗")
        return
    
    # 測試刷新token
    print("3. 測試刷新token...")
    new_access_token = manager.refresh_access_token(refresh_token)
    if new_access_token:
        print("✅ Token刷新成功")
    else:
        print("❌ Token刷新失敗")
        return
    
    # 測試過期token
    print("4. 測試過期token...")
    import time
    time.sleep(1)  # 等待1秒
    
    # 創建一個已過期的token（1秒過期）
    old_manager = SecureSessionManager()
    old_manager.access_token_expire_minutes = 1/60  # 1秒
    expired_token = old_manager.create_access_token(test_user_id)
    
    time.sleep(2)  # 等待2秒
    expired_payload = manager.verify_token(expired_token, 'access')
    if expired_payload is None:
        print("✅ 過期token正確被拒絕")
    else:
        print("❌ 過期token應該被拒絕")
    
    print("\n🎉 安全Session管理器測試完成！")

if __name__ == '__main__':
    test_session_manager()
