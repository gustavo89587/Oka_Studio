import OpenAI from 'openai';
import { NextRequest } from 'next/server';


export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';
export const maxDuration = 60;


export async function POST(req: NextRequest) {
const key = process.env.OPENAI_API_KEY;
if (!key) return new Response(JSON.stringify({ error: 'Missing OPENAI_API_KEY' }), { status: 500 });
const { topic, format } = await req.json();


const openai = new OpenAI({ apiKey: key });
const system = `Você é um copywriter de cibersegurança e tecnologia. Entregue copy em JSON com: title, hook, script, cta, hashtags.`;


const completion = await openai.chat.completions.create({
model: 'gpt-4o-mini',
messages: [
{ role: 'system', content: system },
{ role: 'user', content: `Crie uma copy para ${format}. Tema: ${topic}. Responda em JSON.` },
],
response_format: { type: 'json_object' },
temperature: 0.7,
});


const content = completion.choices[0].message.content ?? '{}';
return new Response(content, { headers: { 'Content-Type': 'application/json' } });
}