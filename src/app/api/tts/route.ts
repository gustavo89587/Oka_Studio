import { NextRequest } from 'next/server';


export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;


export async function POST(req: NextRequest) {
const { text, voiceId } = await req.json();
const key = process.env.ELEVENLABS_API_KEY;
if (!key) return new Response(JSON.stringify({ error: 'Missing ELEVENLABS_API_KEY' }), { status: 500 });
const id = voiceId || process.env.NEXT_PUBLIC_TTS_DEFAULT_VOICE_ID;
if (!id) return new Response(JSON.stringify({ error: 'Missing voiceId' }), { status: 400 });


const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${id}`, {
method: 'POST',
headers: {
'xi-api-key': key,
'Content-Type': 'application/json',
'Accept': 'audio/mpeg',
},
body: JSON.stringify({
text,
model_id: 'eleven_multilingual_v2',
voice_settings: { stability: 0.5, similarity_boost: 0.8, style: 0.3, use_speaker_boost: true },
}),
});


if (!r.ok) {
const msg = await r.text();
return new Response(JSON.stringify({ error: `TTS ${r.status}: ${msg}` }), { status: 500 });
}


const buf = Buffer.from(await r.arrayBuffer());
return new Response(buf, {
status: 200,
headers: {
'Content-Type': 'audio/mpeg',
'Content-Disposition': 'attachment; filename="narracao.mp3"',
'Cache-Control': 'no-store',
},
});
}