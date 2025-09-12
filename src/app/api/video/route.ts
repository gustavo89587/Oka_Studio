import { NextRequest } from "next/server";

export async function POST(req: NextRequest) {
  const formIn = await req.formData();
  const fd = new FormData();
  formIn.forEach((v, k) => fd.set(k, v));

  const r = await fetch(`${process.env.WORKER_URL}/video`, {
    method: "POST",
    headers: { "x-worker-token": process.env.WORKER_TOKEN! },
    body: fd,
    cache: "no-store",
  });

  const body = await r.text();
  return new Response(body, {
    status: r.status,
    headers: { "content-type": r.headers.get("content-type") || "application/json" },
  });
}
