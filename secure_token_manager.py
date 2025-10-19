#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全的Token管理系統
- 使用高熵隨機token
- 只存儲雜湊值
- 原子性操作
- 極短TTL
"""

import os
import secrets
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

class SecureTokenManager:
    """安全的Token管理器"""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.token_length = 32  # 256-bit token
        self.ttl_minutes = 5    # 5分鐘TTL
    
    def _generate_token(self) -> str:
        """生成高熵隨機token"""
        return secrets.token_urlsafe(self.token_length)
    
    def _hash_token(self, token: str) -> str:
        """生成token的SHA256雜湊"""
        return hashlib.sha256(token.encode('utf-8')).hexdigest()
    
    def _verify_token(self, token: str, token_hash: str) -> bool:
        """驗證token是否匹配雜湊"""
        return hmac.compare_digest(self._hash_token(token), token_hash)
    
    def create_link_token(self, line_user_id: str) -> Optional[str]:
        """創建連結token（返回明文token，數據庫存雜湊）"""
        try:
            # 生成高熵token
            token = self._generate_token()
            token_hash = self._hash_token(token)
            
            # 設定過期時間
            expires_at = (datetime.utcnow() + timedelta(minutes=self.ttl_minutes)).isoformat() + 'Z'
            
            # 先清理該用戶的舊token（原子操作）
            self.supabase.table('link_tokens').delete().eq('line_user_id', line_user_id).execute()
            
            # 插入新token（只存雜湊）
            response = self.supabase.table('link_tokens').insert({
                'token_hash': token_hash,
                'line_user_id': line_user_id,
                'expires_at': expires_at,
                'used': False,
                'created_at': datetime.utcnow().isoformat() + 'Z'
            }).execute()
            
            if response.data:
                logger.info(f"✅ 為用戶 {line_user_id} 創建安全token")
                return token
            else:
                logger.error(f"❌ 創建token失敗")
                return None
                
        except Exception as e:
            logger.error(f"❌ 創建token異常: {e}")
            return None
    
    def consume_token(self, token: str) -> Optional[Dict[str, Any]]:
        """原子性消耗token並返回用戶信息"""
        try:
            token_hash = self._hash_token(token)
            
            # 開始事務性查詢
            response = self.supabase.table('link_tokens').select('*').eq('token_hash', token_hash).eq('used', False).execute()
            
            if not response.data:
                logger.warning(f"❌ Token不存在或已使用: {token_hash[:8]}...")
                return None
            
            token_data = response.data[0]
            line_user_id = token_data['line_user_id']
            expires_at = datetime.fromisoformat(token_data['expires_at'].replace('Z', '+00:00'))
            
            # 檢查過期
            if datetime.now(expires_at.tzinfo) > expires_at:
                logger.warning(f"❌ Token已過期: {token_hash[:8]}...")
                return None
            
            # 原子性標記為已使用
            update_response = self.supabase.table('link_tokens').update({
                'used': True,
                'used_at': datetime.utcnow().isoformat() + 'Z'
            }).eq('token_hash', token_hash).eq('used', False).execute()
            
            if not update_response.data:
                logger.warning(f"❌ Token已被其他請求消耗: {token_hash[:8]}...")
                return None
            
            logger.info(f"✅ Token消耗成功: {token_hash[:8]}... -> {line_user_id}")
            
            return {
                'line_user_id': line_user_id,
                'token_id': token_data['id']
            }
            
        except Exception as e:
            logger.error(f"❌ 消耗token異常: {e}")
            return None
    
    def cleanup_expired_tokens(self) -> int:
        """清理過期token"""
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            
            # 刪除過期或已使用的token
            response = self.supabase.table('link_tokens').delete().or_(
                f'expires_at.lt.{now},used.eq.true'
            ).execute()
            
            deleted_count = len(response.data) if response.data else 0
            logger.info(f"🧹 清理了 {deleted_count} 個過期token")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"❌ 清理token異常: {e}")
            return 0

# 測試函數
def test_secure_token_manager():
    """測試安全token管理器"""
    print("🧪 測試安全Token管理器")
    
    # 初始化
    supabase = create_client(
        os.getenv('SUPABASE_URL', 'https://ciqlfqfgzqqgdrogedxg.supabase.co'),
        os.getenv('SUPABASE_ANON_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpcWxmcWZnenFxZ2Ryb2dlZHhnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEyMDcwODUsImV4cCI6MjA2Njc4MzA4NX0.LP-9iTyckifGXvS45GBWBImnBGKADAw0jk1BpGNZWWA')
    )
    
    manager = SecureTokenManager(supabase)
    test_user_id = "U977c24d1fec3a2bf07035504e1444911"
    
    # 測試創建token
    print("1. 測試創建token...")
    token = manager.create_link_token(test_user_id)
    if token:
        print(f"✅ Token創建成功: {token[:16]}...")
    else:
        print("❌ Token創建失敗")
        return
    
    # 測試消耗token
    print("2. 測試消耗token...")
    result = manager.consume_token(token)
    if result:
        print(f"✅ Token消耗成功: {result}")
    else:
        print("❌ Token消耗失敗")
        return
    
    # 測試重複消耗（應該失敗）
    print("3. 測試重複消耗...")
    result2 = manager.consume_token(token)
    if result2:
        print("❌ 重複消耗應該失敗")
    else:
        print("✅ 重複消耗正確失敗")
    
    # 測試清理
    print("4. 測試清理過期token...")
    cleaned = manager.cleanup_expired_tokens()
    print(f"✅ 清理了 {cleaned} 個token")
    
    print("\n🎉 安全Token管理器測試完成！")

if __name__ == '__main__':
    test_secure_token_manager()
