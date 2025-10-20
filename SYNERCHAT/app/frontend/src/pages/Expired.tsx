import React from 'react'

export default function Expired() {
  return (
    <div style={{ padding: 24 }}>
      <h2>Sessione scaduta</h2>
      <p>Per proteggere la tua privacy, i dati locali sono stati eliminati.</p>
      <button onClick={() => location.replace('/')}>Torna alla Home</button>
    </div>
  )
}