import React, { useEffect, useMemo, useState } from 'react'
import { ethers } from 'ethers'

const FTS_ADDRESS = '0xCc12Ea927F6E8d3919010498Ef8736d4612FD83e'

const ERC20_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function decimals() view returns (uint8)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'function approve(address spender, uint256 amount) returns (bool)',
  'function transfer(address to, uint256 amount) returns (bool)'
]

type Props = {
  address: string
}

export default function Payments({ address }: Props) {
  const [balance, setBalance] = useState<string>('0')
  const [decimals, setDecimals] = useState<number>(18)
  const [to, setTo] = useState('')
  const [amount, setAmount] = useState('')
  const [status, setStatus] = useState('')

  const provider = useMemo(() => new ethers.BrowserProvider((window as any).ethereum), [])

  useEffect(() => {
    (async () => {
      const signer = await provider.getSigner()
      const erc20 = new ethers.Contract(FTS_ADDRESS, ERC20_ABI, signer)
      const bal = await erc20.balanceOf(address)
      const dec = await erc20.decimals()
      setBalance(bal.toString()); setDecimals(dec)
    })()
  }, [address, provider])

  const send = async () => {
    try {
      setStatus('Invio in corso...')
      const signer = await provider.getSigner()
      const erc20 = new ethers.Contract(FTS_ADDRESS, ERC20_ABI, signer)
      const value = ethers.parseUnits(amount, decimals)
      const tx = await erc20.transfer(to, value)
      await tx.wait()
      setStatus('Fatto!')
    } catch (e: any) {
      setStatus(e.message || 'Errore')
    }
  }

  return (
    <div style={{ border: '1px solid #ccc', padding: 12, width: 360 }}>
      <h3>Pagamenti FTS</h3>
      <div>Saldo: {ethers.formatUnits(balance, decimals)} FTS</div>
      <div style={{ marginTop: 8, display: 'flex', gap: 8, flexDirection: 'column' }}>
        <input value={to} onChange={(e) => setTo(e.target.value)} placeholder="Destinatario" />
        <input value={amount} onChange={(e) => setAmount(e.target.value)} placeholder="Importo" />
        <button onClick={send}>Invia FTS</button>
      </div>
      <div style={{ marginTop: 8, color: '#555' }}>{status}</div>
    </div>
  )
}