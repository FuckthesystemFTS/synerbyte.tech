import sodium from 'libsodium-wrappers';

export class CryptoManager {
  private initialized = false;
  private keyPair: { publicKey: Uint8Array; privateKey: Uint8Array } | null = null;

  async init() {
    if (!this.initialized) {
      await sodium.ready;
      this.initialized = true;
    }
  }

  async generateKeyPair() {
    await this.init();
    this.keyPair = sodium.crypto_box_keypair();
    return {
      publicKey: sodium.to_base64(this.keyPair.publicKey),
      privateKey: sodium.to_base64(this.keyPair.privateKey),
    };
  }

  async loadKeyPair(publicKey: string, privateKey: string) {
    await this.init();
    this.keyPair = {
      publicKey: sodium.from_base64(publicKey),
      privateKey: sodium.from_base64(privateKey),
    };
  }

  getPublicKey(): string {
    if (!this.keyPair) {
      throw new Error('Key pair not initialized');
    }
    return sodium.to_base64(this.keyPair.publicKey);
  }

  // Simplified encryption using secretbox with shared key
  async encryptSimple(message: string, sharedSecret: string): Promise<string> {
    await this.init();
    
    // Derive key from shared secret
    const key = sodium.crypto_generichash(32, sodium.from_string(sharedSecret));
    const messageBytes = sodium.from_string(message);
    const nonce = sodium.randombytes_buf(sodium.crypto_secretbox_NONCEBYTES);

    const encrypted = sodium.crypto_secretbox_easy(messageBytes, nonce, key);

    // Combine nonce and encrypted message
    const combined = new Uint8Array(nonce.length + encrypted.length);
    combined.set(nonce);
    combined.set(encrypted, nonce.length);

    return sodium.to_base64(combined);
  }

  async decryptSimple(encryptedMessage: string, sharedSecret: string): Promise<string> {
    await this.init();
    
    // Derive key from shared secret
    const key = sodium.crypto_generichash(32, sodium.from_string(sharedSecret));
    const combined = sodium.from_base64(encryptedMessage);
    const nonce = combined.slice(0, sodium.crypto_secretbox_NONCEBYTES);
    const encrypted = combined.slice(sodium.crypto_secretbox_NONCEBYTES);

    const decrypted = sodium.crypto_secretbox_open_easy(encrypted, nonce, key);

    return sodium.to_string(decrypted);
  }

  async encrypt(message: string, recipientPublicKey: string): Promise<string> {
    await this.init();
    if (!this.keyPair) {
      throw new Error('Key pair not initialized');
    }

    const messageBytes = sodium.from_string(message);
    const recipientPubKey = sodium.from_base64(recipientPublicKey);
    const nonce = sodium.randombytes_buf(sodium.crypto_box_NONCEBYTES);

    const encrypted = sodium.crypto_box_easy(
      messageBytes,
      nonce,
      recipientPubKey,
      this.keyPair.privateKey
    );

    // Combine nonce and encrypted message
    const combined = new Uint8Array(nonce.length + encrypted.length);
    combined.set(nonce);
    combined.set(encrypted, nonce.length);

    return sodium.to_base64(combined);
  }

  async decrypt(encryptedMessage: string, senderPublicKey: string): Promise<string> {
    await this.init();
    if (!this.keyPair) {
      throw new Error('Key pair not initialized');
    }

    const combined = sodium.from_base64(encryptedMessage);
    const nonce = combined.slice(0, sodium.crypto_box_NONCEBYTES);
    const encrypted = combined.slice(sodium.crypto_box_NONCEBYTES);
    const senderPubKey = sodium.from_base64(senderPublicKey);

    const decrypted = sodium.crypto_box_open_easy(
      encrypted,
      nonce,
      senderPubKey,
      this.keyPair.privateKey
    );

    return sodium.to_string(decrypted);
  }

  // Store keys in localStorage
  saveKeys() {
    if (!this.keyPair) {
      throw new Error('Key pair not initialized');
    }
    localStorage.setItem('publicKey', sodium.to_base64(this.keyPair.publicKey));
    localStorage.setItem('privateKey', sodium.to_base64(this.keyPair.privateKey));
  }

  loadKeys(): boolean {
    const publicKey = localStorage.getItem('publicKey');
    const privateKey = localStorage.getItem('privateKey');
    
    if (publicKey && privateKey) {
      this.keyPair = {
        publicKey: sodium.from_base64(publicKey),
        privateKey: sodium.from_base64(privateKey),
      };
      return true;
    }
    return false;
  }

  clearKeys() {
    this.keyPair = null;
    localStorage.removeItem('publicKey');
    localStorage.removeItem('privateKey');
  }
}

export const crypto = new CryptoManager();
