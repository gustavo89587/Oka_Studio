// app/api/copy/route.ts
import { NextResponse } from "next/server";
import { generateCopy, type Platform } from "@/lib/finch";

const ALLOWED_ORIGINS = new Set([
  "http://localhost:3000",
  "http://localhost",              // Capacitor Android em debug às vezes usa
  "capacitor://localhost",         // WebView do APK
  process.env.NEXT_PUBLIC_BASE_URL || "", // seu domínio Vercel, ex: https://oka-studio.vercel.app
]);

function cors(res: NextResponse) {
  // Ajuste fino: em produção, valide o Origin do request
  res.headers.set("Access-Control-Allow-Origin", "*"); // pode restringir depois
  res.headers.set("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.headers.set("Access-Control-Allow-Headers", "Content-Type, Authorization");
  return res;
}

export async function OPTIONS() {
  return cors(new NextResponse(null, { status: 204 }));
}

export async function POST(req: Request) {
  try {
    const { topic, platform } = await req.json();
    if (!topic || !platform) {
      return cors(
        NextResponse.json({ error: "topic e platform são obrigatórios" }, { status: 400 })
      );
    }

    const valid = new Set<Platform>(["LinkedIn","Instagram","YouTube shorts","TikTok"]);
    if (!valid.has(platform)) {
      return cors(
        NextResponse.json({ error: "platform inválido" }, { status: 400 })
      );
    }

    const text = generateCopy(topic, platform as Platform);
    return cors(NextResponse.json({ ok: true, text }));
  } catch (e: any) {
    return cors(NextResponse.json({ ok: false, error: e?.message || "erro" }, { status: 500 }));
  }
}
