import { useCallback } from 'react'

type SensitiveBuffer = ArrayBuffer | Uint8Array

let trackedBuffers: Set<SensitiveBuffer> = new Set()
let trackedBlobUrls: Set<string> = new Set()
let trackedSockets: Set<WebSocket> = new Set()

export function trackBuffer(buf: SensitiveBuffer) {
  trackedBuffers.add(buf)
}

export function trackBlobUrl(url: string) {
  trackedBlobUrls.add(url)
}

export function trackSocket(ws: WebSocket) {
  trackedSockets.add(ws)
}

export function useKillSwitch() {
  const secureWipe = useCallback(async () => {
    try {
      await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt', 'decrypt'])
    } catch {}

    // Overwrite buffers
    trackedBuffers.forEach((buf) => {
      try {
        if (buf instanceof Uint8Array) {
          crypto.getRandomValues(buf)
          buf.fill(0)
        } else {
          const view = new Uint8Array(buf)
          crypto.getRandomValues(view)
          view.fill(0)
        }
      } catch {}
    })
    trackedBuffers.clear()

    // Storage wipe
    try { localStorage.clear() } catch {}
    try { sessionStorage.clear() } catch {}
    try {
      if ('caches' in window) {
        const names = await caches.keys()
        await Promise.all(names.map((n) => caches.delete(n)))
      }
    } catch {}
    try {
      const dbs = await indexedDB.databases()
      await Promise.all(dbs.map(d => d.name ? new Promise<void>((resolve) => { const req = indexedDB.deleteDatabase(d.name!); req.onsuccess = () => resolve(); req.onerror = () => resolve(); req.onblocked = () => resolve(); }) : Promise.resolve()))
    } catch {}

    // Revoke blobs
    trackedBlobUrls.forEach((u) => { try { URL.revokeObjectURL(u) } catch {} })
    trackedBlobUrls.clear()

    // Close websockets
    trackedSockets.forEach((ws) => { try { ws.close(4000, 'wipe') } catch {} })
    trackedSockets.clear()

    // Reload to expired page
    try { location.replace('/expired') } catch { location.reload() }
  }, [])

  return { secureWipe }
}