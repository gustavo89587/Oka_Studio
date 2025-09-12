import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { text } = await req.json();
  if (!text) return NextResponse.json({ error: "text required" }, { status: 400 });

  const r = await fetch(`${process.env.WORKER_URL}/tts`, {
    method: "POST",
    headers: {
      "x-worker-token": process.env.WORKER_TOKEN!,
      "content-type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ text }),
    cache: "no-store",
  });

  const data = await r.json().catch(async () => ({ raw: await r.text() }));
  return NextResponse.json(data, { status: r.status });
}
