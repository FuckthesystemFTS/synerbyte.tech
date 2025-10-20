import React, { useEffect, useRef, useState } from 'react'
import { trackSocket } from '../shared/useKillSwitch'

type Props = {
  token: string
  conversationId: string
}

export default function Chat({ token, conversationId }: Props) {
  const [input, setInput] = useState('')
  const [log, setLog] = useState<string[]>([])
  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${encodeURIComponent(conversationId)}?token=${encodeURIComponent(token)}`)
    ws.binaryType = 'arraybuffer'
    ws.onmessage = (ev) => {
      const data = new Uint8Array(ev.data as ArrayBuffer)
      // Placeholder: show hex of received ciphertext packet
      const hex = Array.from(data).map(b => b.toString(16).padStart(2, '0')).join('')
      setLog((l) => [...l, `RX ${hex.slice(0, 32)}... (${data.length}b)`])
    }
    ws.onerror = () => setLog((l) => [...l, 'WS error'])
    ws.onclose = () => setLog((l) => [...l, 'WS closed'])
    wsRef.current = ws
    trackSocket(ws)
    return () => ws.close()
  }, [conversationId, token])

  const send = () => {
    const ws = wsRef.current
    if (!ws || ws.readyState !== ws.OPEN) return
    // Placeholder: send UTF-8 bytes as a stand-in for ciphertext
    const enc = new TextEncoder().encode(input)
    ws.send(enc)
    setLog((l) => [...l, `TX ${input}`])
    setInput('')
  }

  return (
    <div style={{ border: '1px solid #ccc', padding: 12, width: 420 }}>
      <h3>Chat (relay cifrato)</h3>
      <div style={{ height: 200, overflow: 'auto', background: '#fafafa', padding: 8, fontFamily: 'monospace' }}>
        {log.map((line, i) => (<div key={i}>{line}</div>))}
      </div>
      <div style={{ marginTop: 8, display: 'flex', gap: 8 }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Messaggio (placeholder)" style={{ flex: 1 }} />
        <button onClick={send}>Invia</button>
      </div>
    </div>
  )
}