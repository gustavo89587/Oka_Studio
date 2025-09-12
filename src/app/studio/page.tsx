// src/app/studio/page.tsx
"use client";

import { useState, useRef, useMemo } from "react";

export default function Page() {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const [text, setText] = useState("");
  const charCount = useMemo(() => text.length, [text]);

  return (
    <div style={{ padding: 24, fontSize: 18 }}>
      <h1 style={{ fontWeight: 700, fontSize: 24, marginBottom: 12 }}>Oka Studio</h1>
      <p style={{ opacity: 0.8, marginBottom: 12 }}>Studio OK ✅ — client component carregado.</p>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          ref={inputRef}
          value={text}
          placeholder="Digite um texto de teste…"
          onChange={(e) => setText(e.target.value)}
          style={{
            flex: 1,
            padding: 10,
            border: "1px solid #ddd",
            borderRadius: 8,
          }}
        />
        <button
          onClick={() => inputRef.current?.focus()}
          style={{
            padding: "10px 14px",
            borderRadius: 8,
            border: "1px solid #ddd",
            background: "#f8f8f8",
            cursor: "pointer",
          }}
        >
          Focar
        </button>
      </div>

      <div style={{ marginTop: 10, opacity: 0.7 }}>Caracteres: {charCount}</div>
    </div>
  );
}
