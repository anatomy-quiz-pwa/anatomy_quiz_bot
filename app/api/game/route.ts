import { NextRequest, NextResponse } from "next/server";
import { readFile } from "fs/promises";
import { join } from "path";

export async function GET(req: NextRequest) {
  try {
    // 讀取 public/index.html 文件
    const filePath = join(process.cwd(), "public", "index.html");
    const htmlContent = await readFile(filePath, "utf-8");
    
    return new NextResponse(htmlContent, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-cache",
      },
    });
  } catch (error) {
    console.error("Error serving game page:", error);
    return new NextResponse("Game page not found", { status: 404 });
  }
}
