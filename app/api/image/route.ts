export const dynamic = 'force-dynamic';

export async function POST(req: Request) {
  const body = await req.json();

  const fast_preview = body.fast_preview ?? (process.env.NEXT_PUBLIC_FAST_PREVIEW === 'true');
  const quality = body.quality ?? (process.env.NEXT_PUBLIC_QUALITY !== 'false');

  const r = await fetch(`${process.env.WORKER_URL}/image`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.WORKER_TOKEN}`,
    },
    body: JSON.stringify({ ...body, fast_preview, quality })
  });

  return new Response(await r.text(), { status: r.status });
}
