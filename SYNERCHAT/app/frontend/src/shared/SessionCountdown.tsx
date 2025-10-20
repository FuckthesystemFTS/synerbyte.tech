import React, { useEffect, useState } from 'react'

type Props = {
  expiresAt: number
  onExpire: () => void
  onRenew: () => void
}

export default function SessionCountdown({ expiresAt, onExpire, onRenew }: Props) {
  const [remaining, setRemaining] = useState<number>(() => Math.max(0, expiresAt - Math.floor(Date.now() / 1000)))

  useEffect(() => {
    const id = setInterval(() => {
      const r = Math.max(0, expiresAt - Math.floor(Date.now() / 1000))
      setRemaining(r)
      if (r === 0) {
        clearInterval(id)
        onExpire()
      }
    }, 1000)
    return () => clearInterval(id)
  }, [expiresAt, onExpire])

  const mm = String(Math.floor(remaining / 60)).padStart(2, '0')
  const ss = String(remaining % 60).padStart(2, '0')

  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
      <span>Scadenza sessione:</span>
      <strong>{mm}:{ss}</strong>
      <button onClick={onRenew}>Rinnova sessione</button>
    </div>
  )
}