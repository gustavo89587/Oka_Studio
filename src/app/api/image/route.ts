import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const { prompt, preset = "VERTICAL_9_16" } = await req.json();
  if (!prompt) return NextResponse.json({ error: "prompt required" }, { status: 400 });

  const r = await fetch(`${process.env.WORKER_URL}/image`, {
    method: "POST",
    headers: {
      "x-worker-token": process.env.WORKER_TOKEN!,
      "content-type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({ prompt, preset }),
    cache: "no-store",
  });

  const data = await r.json().catch(async () => ({ raw: await r.text() }));
  return NextResponse.json(data, { status: r.status });
}
