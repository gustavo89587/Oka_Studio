"use client";
import { useState } from "react";

export default function Home() {
  const [topic, setTopic] = useState("Cibersegurança com IA");
  const [platform, setPlatform] = useState("Instagram");
  const [out, setOut] = useState("");

  async function handleGen(e: React.FormEvent) {
    e.preventDefault();
    setOut("Gerando...");
    const r = await fetch("/api/copy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ topic, platform }),
    });
    const data = await r.json();
    setOut(data.text || data.error || "Erro");
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="mb-6 text-3xl font-bold text-yellow-600">✨ Oka Studio</h1>
      <form onSubmit={handleGen} className="space-y-3">
        <input
          className="w-full rounded border p-2"
          placeholder="Tema do vídeo"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <select
          className="w-full rounded border p-2"
          value={platform}
          onChange={(e) => setPlatform(e.target.value)}
        >
          <option>LinkedIn</option>
          <option>Instagram</option>
          <option>YouTube shorts</option>
          <option>TikTok</option>
        </select>
        <button className="rounded bg-yellow-500 px-4 py-2 font-semibold text-white hover:opacity-90">
          Gerar copy Finch
        </button>
      </form>

      <pre className="mt-6 whitespace-pre-wrap rounded bg-neutral-100 p-4 text-sm">
        {out}
      </pre>
    </main>
  );
}
