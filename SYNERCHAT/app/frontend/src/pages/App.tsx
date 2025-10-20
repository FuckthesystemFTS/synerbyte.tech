import React, { useEffect, useMemo, useState } from 'react'
import { ethers } from 'ethers'
import SessionCountdown from '../shared/SessionCountdown'
import { useKillSwitch } from '../shared/useKillSwitch'
import Chat from './Chat'
import Payments from './Payments'

function getProvider() {
  const anyWindow = window as any
  if (!anyWindow.ethereum) throw new Error('Wallet non trovato')
  return new ethers.BrowserProvider(anyWindow.ethereum)
}

export default function App() {
  const [address, setAddress] = useState<string>('')
  const [deviceId] = useState<string>(() => '0x' + crypto.getRandomValues(new Uint8Array(32)).reduce((a, b) => a + b.toString(16).padStart(2, '0'), ''))
  const [token, setToken] = useState<string>('')
  const [expiresAt, setExpiresAt] = useState<number>(0)
  const { secureWipe } = useKillSwitch()

  useEffect(() => {
    if (expiresAt && Date.now() / 1000 > expiresAt) secureWipe()
  }, [expiresAt, secureWipe])

  const login = async () => {
    const provider = getProvider()
    const signer = await provider.getSigner()
    const addr = await signer.getAddress()
    setAddress(addr)
    const start = await fetch(`/auth/siwe-start?address=${addr}&deviceId=${deviceId}&chainId=137`).then(r => r.json())
    const sig = await signer.signMessage(start.message)
    const verify = await fetch('/auth/siwe-verify', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ address: addr, deviceId, nonce: start.nonce, signature: sig, issuedAt: start.issuedAt, expiresAt: start.expiresAt, chainId: 137 }) }).then(r => r.json())
    setToken(verify.token)
    setExpiresAt(verify.expiresAt)
  }

  const renew = async () => {
    setToken('')
    setExpiresAt(0)
    await login()
  }

  return (
    <div style={{ padding: 16 }}>
      <img src="/logosy.jpg" alt="Synerchat" style={{ width: 160 }} />
      <h2>Synerchat — Messaggistica sicura a tempo</h2>
      {!token ? (
        <button onClick={login}>Accedi con Wallet (Polygon)</button>
      ) : (
        <div>
          <div>Connesso: {address}</div>
          <SessionCountdown expiresAt={expiresAt} onExpire={secureWipe} onRenew={renew} />
          <div style={{ marginTop: 16, display: 'flex', gap: 16 }}>
            <Chat token={token} conversationId={address.toLowerCase()} />
            <Payments address={address} />
          </div>
        </div>
      )}
    </div>
  )
}