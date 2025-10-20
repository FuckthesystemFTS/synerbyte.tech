import sodium from 'libsodium-wrappers'
import { trackBuffer } from '../../shared/useKillSwitch'

export type RatchetState = {
  rootKey: Uint8Array
  sendKey: Uint8Array
  recvKey: Uint8Array
}

export async function initCrypto(): Promise<void> {
  await sodium.ready
}

export function deriveKeysFromX25519(sharedSecret: Uint8Array): RatchetState {
  const hkdf = sodium.crypto_kdf_derive_from_key
  const master = sodium.crypto_kdf_keygen()
  // Mix in shared secret
  for (let i = 0; i < master.length && i < sharedSecret.length; i++) master[i] ^= sharedSecret[i]
  const rootKey = hkdf(32, 1, 'root-key', master)
  const sendKey = hkdf(32, 2, 'send-key', master)
  const recvKey = hkdf(32, 3, 'recv-key', master)
  trackBuffer(rootKey); trackBuffer(sendKey); trackBuffer(recvKey)
  return { rootKey, sendKey, recvKey }
}

export function aeadEncrypt(key: Uint8Array, plaintext: Uint8Array, aad?: Uint8Array) {
  const nonce = sodium.randombytes_buf(sodium.crypto_aead_xchacha20poly1305_ietf_NPUBBYTES)
  const ciphertext = sodium.crypto_aead_xchacha20poly1305_ietf_encrypt(plaintext, aad, null, nonce, key)
  trackBuffer(ciphertext); trackBuffer(nonce)
  return { ciphertext, nonce }
}

export function aeadDecrypt(key: Uint8Array, nonce: Uint8Array, ciphertext: Uint8Array, aad?: Uint8Array) {
  return sodium.crypto_aead_xchacha20poly1305_ietf_decrypt(null, ciphertext, aad, nonce, key)
}