import { NextResponse } from "next/server";
import { generateCopy, type Platform } from "@/lib/finch";

function cors(res: NextResponse) {
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
    const valid = new Set<Platform>(["LinkedIn","Instagram","YouTube shorts","TikTok"]);
    if (!topic || !platform || !valid.has(platform)) {
      return cors(NextResponse.json({ error: "topic ou platform inválidos" }, { status: 400 }));
    }
    const text = generateCopy(topic, platform as Platform);
    return cors(NextResponse.json({ ok: true, text }));
  } catch (e: any) {
    return cors(NextResponse.json({ ok: false, error: e?.message || "erro" }, { status: 500 }));
  }
}
