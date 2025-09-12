"use client";
import { useMemo, useRef, useState } from 'react';


type SizePreset = '1080x1920' | '1920x1080' | '1080x1080' | '1350x1080';


const SIZE_MAP: Record<string, SizePreset> = {
'Shorts/TikTok/Reels (9:16)': '1080x1920',
'YouTube 16:9': '1920x1080',
'Feed 1:1': '1080x1080',
'Feed 4:5': '1350x1080',
};


export default function Page() {
const inputRef = useRef<HTMLInputElement | null>(null);
const [format, setFormat] = useState<string>('Shorts/TikTok/Reels (9:16)');
const [text, setText] = useState('Fala, Gustavo! Este é um teste do Oka Studio.');
const [subStyle, setSubStyle] = useState<'finch' | 'impacto' | 'basic'>('finch');
const [duration, setDuration] = useState<number>(30);
const [fps, setFps] = useState<number>(30);
const [bgVideo, setBgVideo] = useState<File | null>(null);
const [bgImage, setBgImage] = useState<File | null>(null);
const [status, setStatus] = useState<string>('Pronto.');


const charCount = useMemo(() => text.length, [text]);


async function handleTTS() {
setStatus('Gerando áudio...');
const res = await fetch('/api/tts', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ text }),
});
if (!res.ok) { setStatus('Erro no TTS'); return; }
const blob = await res.blob();
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
}