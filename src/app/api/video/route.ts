import { NextRequest } from 'next/server';


export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 300; // 5 min para render


export async function POST(req: NextRequest) {
const WORKER_URL = process.env.WORKER_URL;
const WORKER_TOKEN = process.env.WORKER_TOKEN;
if (!WORKER_URL || !WORKER_TOKEN) {
return new Response(JSON.stringify({ error: 'WORKER_URL/WORKER_TOKEN not set' }), { status: 500 });
}


const form = await req.formData();
const forward = new FormData();
for (const [k, v] of form.entries()) {
if (typeof v === 'string') forward.append(k, v);
else forward.append(k, v, (v as File).name);
}


const res = await fetch(`${WORKER_URL}/render-video`, {
method: 'POST',
headers: { Authorization: `Bearer ${WORKER_TOKEN}` },
body: forward,
});


if (!res.ok) {
const msg = await res.text();
return new Response(JSON.stringify({ error: `WORKER ${res.status}: ${msg}` }), { status: 502 });
}


const buf = Buffer.from(await res.arrayBuffer());
return new Response(buf, {
headers: {
'Content-Type': 'video/mp4',
'Content-Disposition': 'attachment; filename="shorts_final.mp4"',
}