#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render 部署入口點
將 app_supabase 的應用程序重新導出為 app
"""

import os

# 導入 app_supabase 中的應用程序
from app_supabase import app

# 確保 app 變數可以被 uvicorn 找到
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
