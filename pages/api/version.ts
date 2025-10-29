import type { NextApiRequest, NextApiResponse } from 'next';
export default function handler(_: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({
    sha: process.env.VERCEL_GIT_COMMIT_SHA || 'unknown',
    builtAt: process.env.VERCEL_BUILD_OUTPUT_TIMESTAMP || null,
  });
}
