// lib/supabase.ts
import { createClient } from '@supabase/supabase-js';

export const sbAdmin = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!,   // service_role 只用在伺服器
  { auth: { persistSession: false } }
);
