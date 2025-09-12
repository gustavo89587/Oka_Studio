import { NextRequest } from 'next/server';


export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 120;


export async function POST(req: NextRequest) {
const WORKER_URL = process.env.WORKER_URL;
const WORKER_TOKEN = process.env.WORKER_TOKEN;
if (!WORKER_URL || !WORKER_TOKEN) {
return new Response(JSON.stringify({ error: 'WORKER_URL/WORKER_TOKEN not set' }), { status: 500 });
}


const { prompt, size } = await req.json();


const res = await fetch(`${WORKER_URL}/generate-image`, {
method: 'POST',
headers: {
'Content-Type': 'application/json',
Authorization: `Bearer ${WORKER_TOKEN}`,
},
body: JSON.stringify({ prompt, size }),
});


if (!res.ok) {
const msg = await res.text();
return new Response(JSON.stringify({ error: `WORKER ${res.status}: ${msg}` }), { status: 502 });
}


const buf = Buffer.from(await res.arrayBuffer());
return new Response(buf, {
headers: {
'Content-Type': 'image/png',
'Content-Disposition': 'attachment; filename="image.png"',
'Cache-Control': 'no-store',
},
}