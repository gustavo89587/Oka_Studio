"use client";
import { useEffect, useMemo, useRef, useState } from "react";

type Preset = "VERTICAL_9_16" | "SQUARE_1_1" | "PORTRAIT_4_5" | "LANDSCAPE_16_9";
const PRESETS: { key: Preset; label: string; hint: string; w: number; h: number }[] = [
  { key: "VERTICAL_9_16", label: "Shorts/TikTok/Reels", hint: "1080×1920", w:1080, h:1920 },
  { key: "SQUARE_1_1",    label: "Feed 1:1",            hint: "1080×1080", w:1080, h:1080 },
  { key: "PORTRAIT_4_5",  label: "Feed 4:5",            hint: "1080×1350", w:1080, h:1350 },
  { key: "LANDSCAPE_16_9",label: "YouTube/Landscape",   hint: "1920×1080", w:1920, h:1080 },
];

type JobState = "idle" | "running" | "done" | "error";

export default function Studio() {
  const [preset, setPreset] = useState<Preset>("VERTICAL_9_16");
  const [text, setText] = useState("Título forte + CTA. Escreva seu roteiro aqui.");
  const [prompt, setPrompt] = useState("samurai cyberpunk neon, ultra detailed, cinematic lighting");
  const [bg, setBg] = useState<File | null>(null);

  const [status, setStatus] = useState<JobState>("idle");
  const [message, setMessage] = useState<string>("");
  const [json, setJson] = useState<any>(null);
  const [imgUrl, setImgUrl] = useState<string | null>(null);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);

  const presetInfo = useMemo(() => PRESETS.find(p => p.key === preset)!, [preset]);
  const abortRef = useRef<AbortController | null>(null);

  function reset() {
    setStatus("idle"); setMessage(""); setJson(null);
    setImgUrl(null); setAudioUrl(null); setVideoUrl(null);
  }
  async function safeFetch<T>(input: RequestInfo | URL, init?: RequestInit): Promise<T> {
    abortRef.current?.abort();
    const ac = new AbortController(); abortRef.current = ac;
    const r = await fetch(input, { ...init, signal: ac.signal });
    const ct = r.headers.get("content-type") || "";
    const data = ct.includes("application/json") ? await r.json() : await r.text();
    if (!r.ok) throw new Error(typeof data === "string" ? data : JSON.stringify(data));
    return data as T;
  }
  const pick = (o:any, keys:string[]) => (keys.find(k => o?.[k]) ? String(o[keys.find(k => o?.[k]) as string]) : null);

  async function genTTS() {
    reset(); setStatus("running"); setMessage("Gerando TTS...");
    try {
      const data = await safeFetch<any>("/api/tts", { method:"POST", body: JSON.stringify({ text }) });
      setJson(data); setAudioUrl(pick(data, ["audio_url","url","file_url","public_url","audio_path"]));
      setStatus("done"); setMessage("TTS pronto!");
    } catch(e:any){ setStatus("error"); setMessage(e.message||"Erro no TTS"); }
  }
  async function genImage() {
    reset(); setStatus("running"); setMessage(`Gerando imagem ${presetInfo.hint}...`);
    try {
      const data = await safeFetch<any>("/api/image", { method:"POST", body: JSON.stringify({ prompt, preset })});
      setJson(data); setImgUrl(pick(data, ["image_url","url","file_url","public_url","image_path"]));
      setStatus("done"); setMessage("Imagem pronta!");
    } catch(e:any){ setStatus("error"); setMessage(e.message||"Erro na imagem"); }
  }
  async function genVideo() {
    reset(); setStatus("running"); setMessage(`Gerando vídeo ${presetInfo.hint}...`);
    try {
      const fd = new FormData(); fd.set("text", text); fd.set("preset", preset); if (bg) fd.set("bg_image", bg, bg.name);
      const r = await fetch("/api/video", { method:"POST", body: fd });
      const data = await r.json().catch(async()=>({ raw: await r.text() }));
      setJson(data); setVideoUrl(pick(data, ["video_url","url","file_url","public_url","video_path"]));
      setStatus("done"); setMessage("Vídeo pronto!");
    } catch(e:any){ setStatus("error"); setMessage(e.message||"Erro no vídeo"); }
  }

  const [copy, setCopy] = useState("");
  function gerarCopy() {
    setCopy([
      `Atenção: poste no formato ${presetInfo.label} (${presetInfo.hint}).`,
      `Interesse: gere roteiro, voz e vídeo em minutos com o Oka Studio.`,
      `Desejo: estética premium e consistência diária.`,
      `Ação: gere agora e publique hoje.`
    ].join(" "));
  }

  return (
    <div className="mx-auto max-w-5xl p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Oka Studio — Gerar Conteúdo</h1>
        <span className="text-xs px-2 py-1 rounded-full bg-yellow-100 text-yellow-900">
          {presetInfo.label} • {presetInfo.hint}
        </span>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Form */}
        <div className="border rounded-xl p-4 bg-white shadow-sm space-y-3">
          <label className="block text-sm font-semibold">Formato</label>
          <div className="grid grid-cols-2 gap-2">
            {PRESETS.map(p=>(
              <button key={p.key} onClick={()=>setPreset(p.key)}
                className={`border rounded px-3 py-2 text-left hover:bg-yellow-50 ${preset===p.key?"border-yellow-500 bg-yellow-50":""}`}>
                <div className="font-medium">{p.label}</div>
                <div className="text-xs opacity-70">{p.hint}</div>
              </button>
            ))}
          </div>

          <label className="block text-sm font-semibold mt-3">Roteiro / Texto</label>
          <textarea className="w-full border rounded p-2 h-28" value={text} onChange={e=>setText(e.target.value)} />

          <label className="block text-sm font-semibold mt-3">Prompt da Imagem</label>
          <input className="w-full border rounded p-2" value={prompt} onChange={e=>setPrompt(e.target.value)} />

          <label className="block text-sm font-semibold mt-3">BG opcional (imagem)</label>
          <input type="file" accept="image/*" onChange={e=>setBg(e.target.files?.[0]||null)} />

          <div className="flex gap-2 pt-2">
            <button onClick={genTTS}   className="px-4 py-2 rounded bg-black text-white">Gerar TTS</button>
            <button onClick={genImage} className="px-4 py-2 rounded bg-black text-white">Gerar Imagem</button>
            <button onClick={genVideo} className="px-4 py-2 rounded bg-black text-white">Gerar Vídeo</button>
          </div>

          <div className="pt-3">
            <label className="block text-sm font-semibold">Copy (AIDA simples)</label>
            <div className="flex gap-2 mb-2">
              <button onClick={gerarCopy} className="px-3 py-2 rounded border">Gerar Copy</button>
              <button onClick={()=>navigator.clipboard.writeText(copy)} className="px-3 py-2 rounded border">Copiar</button>
            </div>
            <textarea className="w-full border rounded p-2 h-28" value={copy} onChange={e=>setCopy(e.target.value)} />
          </div>
        </div>

        {/* Preview */}
        <div className="border rounded-xl p-4 bg-white shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <div className="text-sm font-semibold">Status</div>
            <div className={`text-xs px-2 py-1 rounded-full ${
              status==="running"?"bg-blue-100 text-blue-700":status==="done"?"bg-green-100 text-green-700":
              status==="error"?"bg-red-100 text-red-700":"bg-gray-100 text-gray-700"}`}>
              {status.toUpperCase()}
            </div>
          </div>
          <div className="text-sm opacity-80">{message || "Aguardando..."}</div>

          <div className="h-[220px] border rounded-lg flex items-center justify-center overflow-hidden bg-gray-50">
            {videoUrl ? (
              <video key={videoUrl} controls className="max-h-full"><source src={videoUrl} /></video>
            ) : imgUrl ? (
              <img src={imgUrl} alt="preview" className="max-h-full" />
            ) : audioUrl ? (
              <audio controls src={audioUrl} />
            ) : (
              <div className="text-sm text-gray-500">Prévia aparecerá aqui</div>
            )}
          </div>

          {(audioUrl || imgUrl || videoUrl) && (
            <div className="flex gap-2">
              {audioUrl && <a className="px-3 py-2 rounded border" href={audioUrl} target="_blank">Baixar Áudio</a>}
              {imgUrl &&   <a className="px-3 py-2 rounded border" href={imgUrl} target="_blank">Baixar Imagem</a>}
              {videoUrl && <a className="px-3 py-2 rounded border" href={videoUrl} target="_blank">Baixar Vídeo</a>}
            </div>
          )}

          <details className="mt-2">
            <summary className="cursor-pointer text-sm font-semibold">Detalhes (JSON)</summary>
            <pre className="bg-gray-50 p-3 text-xs overflow-auto max-h-64 rounded">{JSON.stringify(json, null, 2)}</pre>
          </details>
        </div>
      </div>
    </div>
  );
}
