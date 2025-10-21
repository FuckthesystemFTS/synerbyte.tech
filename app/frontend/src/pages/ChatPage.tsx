import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useChat } from '../contexts/ChatContext';
import { useNavigate } from 'react-router-dom';
import { crypto } from '../lib/crypto/encryption';
import { api, User } from '../lib/api';

export const ChatPage: React.FC = () => {
  const { user, logout } = useAuth();
  const { chats, activeChat, messages, requests, setActiveChat, sendMessage, sendChatRequest, acceptRequest, verifyChat, refreshChats } = useChat();
  const navigate = useNavigate();
  
  const [messageInput, setMessageInput] = useState('');
  const [showNewChat, setShowNewChat] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<User[]>([]);
  const [newChatCode, setNewChatCode] = useState('');
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [showRequests, setShowRequests] = useState(false);
  const [acceptCode, setAcceptCode] = useState('');
  const [acceptingRequestId, setAcceptingRequestId] = useState<number | null>(null);
  const [showVerification, setShowVerification] = useState(false);
  const [verificationCode, setVerificationCode] = useState('');
  const [verifyingChatId, setVerifyingChatId] = useState<number | null>(null);
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
  const [showSidebar, setShowSidebar] = useState(true);
  const [showScrollTop, setShowScrollTop] = useState(false);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!user) {
      navigate('/login');
    }
  }, [user, navigate]);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    // Handle sidebar visibility on mobile
    if (activeChat) {
      // Hide sidebar on mobile when chat is selected
      if (isMobile) {
        setShowSidebar(false);
      }
    } else {
      // Show sidebar when no chat selected
      if (isMobile) {
        setShowSidebar(true);
      }
    }
  }, [activeChat, isMobile]);

  useEffect(() => {
    // Check for verification needed
    if (activeChat?.verification_pending) {
      setShowVerification(true);
      setVerifyingChatId(activeChat.id);
    }
  }, [activeChat]);

  const handleSearch = async () => {
    if (searchQuery.length < 2) return;
    try {
      const response = await api.searchUsers(searchQuery);
      setSearchResults(response.users);
    } catch (error) {
      console.error('Search failed:', error);
    }
  };

  const handleSendRequest = async () => {
    if (!selectedUser || newChatCode.length !== 4) {
      alert('Please enter a 4-character code');
      return;
    }
    try {
      await sendChatRequest(selectedUser.id, newChatCode);
      alert('Chat request sent!');
      setShowNewChat(false);
      setNewChatCode('');
      setSelectedUser(null);
      setSearchQuery('');
      setSearchResults([]);
    } catch (error: any) {
      alert(error.message);
    }
  };

  const handleAcceptRequest = async (requestId: number) => {
    if (acceptCode.length !== 4) {
      alert('Please enter a 4-character code');
      return;
    }
    try {
      await acceptRequest(requestId, acceptCode);
      setAcceptCode('');
      setAcceptingRequestId(null);
      setShowRequests(false);
      alert('Chat request accepted!');
    } catch (error: any) {
      alert(error.message);
    }
  };

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!messageInput.trim() || !activeChat) return;

    const messageText = messageInput.trim();
    setMessageInput(''); // Clear input immediately for better UX

    try {
      // Encrypt message using chat ID as shared secret
      const sharedSecret = `chat_${activeChat.id}_secret`;
      const encrypted = await crypto.encryptSimple(messageText, sharedSecret);
      await sendMessage(encrypted);
    } catch (error: any) {
      console.error('Failed to send message:', error);
      // Message will show as failed with retry mechanism
    }
  };

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || !e.target.files[0] || !activeChat) return;
    
    const file = e.target.files[0];
    
    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      alert('Image size must be less than 5MB');
      return;
    }
    
    // Check file type
    if (!file.type.startsWith('image/')) {
      alert('Please select an image file');
      return;
    }
    
    try {
      // Convert image to base64
      const reader = new FileReader();
      reader.onload = async (event) => {
        const base64Image = event.target?.result as string;
        
        // Encrypt image data
        const sharedSecret = `chat_${activeChat.id}_secret`;
        const encrypted = await crypto.encryptSimple(base64Image, sharedSecret);
        
        // Send as image message
        sendMessage(encrypted, 'image');
      };
      reader.readAsDataURL(file);
    } catch (error: any) {
      alert('Failed to upload image: ' + error.message);
    }
  };

  const handleVerifyChat = async () => {
    if (!verifyingChatId || verificationCode.length !== 4) {
      alert('Please enter the 4-character code');
      return;
    }
    try {
      await verifyChat(verifyingChatId, verificationCode);
      setShowVerification(false);
      setVerificationCode('');
      setVerifyingChatId(null);
      alert('Chat verified! Active for another 30 minutes.');
    } catch (error: any) {
      alert(error.message);
    }
  };

  const handleClearChat = async () => {
    if (!activeChat) return;
    if (!confirm('Are you sure you want to clear all messages in this chat?')) return;
    
    try {
      await api.clearChatMessages(activeChat.id);
      alert('Chat messages cleared');
    } catch (error: any) {
      alert('Failed to clear chat: ' + error.message);
    }
  };

  const handleDeleteChat = async () => {
    if (!activeChat) return;
    if (!confirm('Do you want to delete this chat? Both users must agree for the chat to be deleted.')) return;
    
    try {
      const response = await api.requestDeleteChat(activeChat.id);
      alert(response.message);
    } catch (error: any) {
      alert('Failed to request deletion: ' + error.message);
    }
  };

  if (!user) return null;

  const handleBackToList = () => {
    setActiveChat(null);
    if (isMobile) {
      setShowSidebar(true);
    }
  };

  const handleScroll = (e: React.UIEvent<HTMLDivElement>) => {
    const target = e.target as HTMLDivElement;
    // Show scroll-to-top button if scrolled down more than 200px
    setShowScrollTop(target.scrollTop > 200);
  };

  const scrollToTop = () => {
    if (messagesContainerRef.current) {
      messagesContainerRef.current.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Arial, sans-serif', overflow: 'hidden' }}>
      {/* Sidebar */}
      <div style={{ 
        width: isMobile ? '100%' : '300px', 
        background: '#2c3e50', 
        color: 'white', 
        display: (isMobile && !showSidebar) ? 'none' : 'flex', 
        flexDirection: 'column',
        position: isMobile ? 'absolute' : 'relative',
        height: '100%',
        zIndex: isMobile ? 10 : 1
      }}>
        {/* Header */}
        <div style={{ padding: '20px', borderBottom: '1px solid #34495e' }}>
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '15px' }}>
            <img src="/logosy.jpg" alt="Logo" style={{ width: '40px', height: '40px', borderRadius: '50%', marginRight: '10px' }} />
            <div style={{ flex: 1 }}>
              <div style={{ fontWeight: 'bold', fontSize: '16px' }}>{user.username || user.email}</div>
              <div style={{ fontSize: '12px', color: '#95a5a6' }}>Online</div>
            </div>
            <button
              onClick={logout}
              style={{ background: '#e74c3c', border: 'none', color: 'white', padding: '5px 10px', borderRadius: '4px', cursor: 'pointer', fontSize: '12px' }}
            >
              Logout
            </button>
          </div>
          
          <button
            onClick={() => setShowNewChat(true)}
            style={{ width: '100%', padding: '10px', background: '#3498db', border: 'none', color: 'white', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', marginBottom: '8px' }}
          >
            + New Chat
          </button>
          
          <button
            onClick={() => setShowRequests(!showRequests)}
            style={{ width: '100%', padding: '10px', background: '#9b59b6', border: 'none', color: 'white', borderRadius: '6px', cursor: 'pointer', fontWeight: '600', position: 'relative' }}
          >
            Requests {requests.length > 0 && <span style={{ position: 'absolute', right: '10px', background: '#e74c3c', borderRadius: '50%', width: '20px', height: '20px', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: '12px' }}>{requests.length}</span>}
          </button>
        </div>

        {/* Chat List */}
        <div style={{ flex: 1, overflowY: 'auto' }}>
          {chats.map(chat => (
            <div
              key={chat.id}
              onClick={() => setActiveChat(chat)}
              style={{
                padding: '15px',
                borderBottom: '1px solid #34495e',
                cursor: 'pointer',
                background: activeChat?.id === chat.id ? '#34495e' : 'transparent',
                transition: 'background 0.2s'
              }}
            >
              <div style={{ fontWeight: '600', marginBottom: '5px' }}>
                {chat.other_user.username || chat.other_user.email}
              </div>
              <div style={{ fontSize: '12px', color: '#95a5a6' }}>
                {chat.verification_pending && '⚠️ Verification needed'}
              </div>
            </div>
          ))}
          {chats.length === 0 && (
            <div style={{ padding: '20px', textAlign: 'center', color: '#95a5a6', fontSize: '14px' }}>
              No active chats
            </div>
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div style={{ 
        flex: 1, 
        display: (isMobile && showSidebar) ? 'none' : 'flex', 
        flexDirection: 'column', 
        background: '#ecf0f1',
        width: isMobile ? '100%' : 'auto',
        position: 'relative'
      }}>
        {activeChat ? (
          <>
            {/* Chat Header - FIXED AT TOP */}
            <div style={{ 
              padding: isMobile ? '12px' : '20px', 
              background: 'white', 
              borderBottom: '2px solid #bdc3c7',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              position: 'fixed',
              top: 0,
              left: isMobile ? 0 : '300px',
              right: 0,
              zIndex: 1000,
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
              WebkitTransform: 'translateZ(0)',
              transform: 'translateZ(0)'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flex: 1 }}>
                {isMobile && (
                  <button
                    onClick={handleBackToList}
                    style={{
                      background: '#3498db',
                      color: 'white',
                      border: 'none',
                      borderRadius: '50%',
                      width: '36px',
                      height: '36px',
                      cursor: 'pointer',
                      fontSize: '18px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center'
                    }}
                  >
                    ←
                  </button>
                )}
                <div>
                  <div style={{ fontWeight: 'bold', fontSize: isMobile ? '16px' : '18px', color: '#2c3e50' }}>
                  {activeChat.other_user.username || activeChat.other_user.email}
                </div>
                <div style={{ fontSize: '12px', color: '#7f8c8d' }}>
                    {activeChat.verification_pending ? '⚠️ Verification required' : '🔒 End-to-end encrypted'}
                  </div>
                </div>
              </div>
              <div style={{ display: 'flex', gap: isMobile ? '5px' : '10px', flexWrap: 'wrap' }}>
                <button
                  onClick={handleClearChat}
                  style={{
                    padding: isMobile ? '6px 12px' : '8px 16px',
                    background: '#f39c12',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer',
                    fontSize: isMobile ? '12px' : '14px',
                    fontWeight: '500'
                  }}
                >
                  {isMobile ? '🗑️' : '🗑️ Clear Chat'}
                </button>
                <button
                  onClick={handleDeleteChat}
                  style={{
                    padding: isMobile ? '6px 12px' : '8px 16px',
                    background: '#e74c3c',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer',
                    fontSize: isMobile ? '12px' : '14px',
                    fontWeight: '500'
                  }}
                >
                  {isMobile ? '❌' : '❌ Delete Chat'}
                </button>
                {!isMobile && (
                  <button
                    onClick={refreshChats}
                    style={{ padding: '8px 15px', background: '#3498db', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}
                  >
                    Refresh
                  </button>
                )}
              </div>
            </div>

            {/* Messages */}
            <div 
              ref={messagesContainerRef}
              onScroll={handleScroll}
              style={{ 
                flex: 1, 
                overflowY: 'auto', 
                overflowX: 'hidden',
                padding: '15px', 
                paddingTop: isMobile ? '80px' : '100px',
                paddingBottom: isMobile ? '80px' : '100px',
                WebkitOverflowScrolling: 'touch',
                display: 'flex',
                flexDirection: 'column',
                position: 'relative'
              }}>
              {messages.map((msg, idx) => {
                const isOwn = msg.sender_id === user.id;
                const status = (msg as any).status;
                const isTempMessage = typeof msg.id === 'string' && msg.id.startsWith('temp_');
                
                return (
                  <div key={msg.id || idx} style={{ 
                    marginBottom: '12px', 
                    display: 'flex', 
                    justifyContent: isOwn ? 'flex-end' : 'flex-start',
                    width: '100%'
                  }}>
                    <div style={{
                      maxWidth: isMobile ? '75%' : '60%',
                      minWidth: '80px',
                      padding: '10px 14px',
                      borderRadius: isOwn ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
                      background: isOwn ? (status === 'failed' ? '#e74c3c' : '#3498db') : 'white',
                      color: isOwn ? 'white' : '#2c3e50',
                      boxShadow: '0 1px 2px rgba(0,0,0,0.15)',
                      wordWrap: 'break-word',
                      wordBreak: 'break-word',
                      opacity: status === 'sending' ? 0.7 : 1,
                      position: 'relative'
                    }}>
                      {!isOwn && <div style={{ fontSize: '11px', fontWeight: '600', marginBottom: '4px', opacity: 0.9 }}>{msg.username || msg.email}</div>}
                      <MessageContent content={msg.encrypted_content} chatId={activeChat.id} messageType={msg.message_type || 'text'} />
                      <div style={{ fontSize: '9px', marginTop: '4px', opacity: 0.7, textAlign: 'right', display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '4px' }}>
                        <span>{new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                        {isOwn && (
                          <span style={{ fontSize: '11px' }}>
                            {status === 'sending' && '⏳'}
                            {status === 'sent' && '✓'}
                            {status === 'failed' && '✗'}
                            {!status && !isTempMessage && '✓✓'}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
              <div ref={messagesEndRef} />
              
              {/* Floating Scroll to Top Button */}
              {showScrollTop && (
                <button
                  onClick={scrollToTop}
                  style={{
                    position: 'fixed',
                    bottom: isMobile ? '80px' : '100px',
                    right: isMobile ? '20px' : '40px',
                    width: '50px',
                    height: '50px',
                    borderRadius: '50%',
                    background: '#3498db',
                    color: 'white',
                    border: 'none',
                    fontSize: '24px',
                    cursor: 'pointer',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
                    zIndex: 1000,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    transition: 'all 0.3s ease'
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
                  onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
                >
                  ↑
                </button>
              )}
            </div>

            {/* Message Input - FIXED AT BOTTOM */}
            <form onSubmit={handleSendMessage} style={{ 
              padding: isMobile ? '10px' : '20px', 
              background: 'white', 
              borderTop: '2px solid #bdc3c7',
              position: 'sticky',
              bottom: 0,
              zIndex: 100,
              boxShadow: '0 -2px 4px rgba(0,0,0,0.1)'
            }}>
              <div style={{ display: 'flex', gap: '10px' }}>
                <input
                  type="text"
                  value={messageInput}
                  onChange={(e) => setMessageInput(e.target.value)}
                  placeholder="Type a message..."
                  style={{ flex: 1, padding: isMobile ? '10px' : '12px', border: '2px solid #bdc3c7', borderRadius: '8px', fontSize: '14px' }}
                />
                <label style={{ padding: isMobile ? '10px 15px' : '12px 20px', background: '#95a5a6', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600', display: 'flex', alignItems: 'center' }}>
                  {isMobile ? '📎' : '📎 Image'}
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageUpload}
                    style={{ display: 'none' }}
                  />
                </label>
                <button
                  type="submit"
                  style={{ padding: isMobile ? '10px 20px' : '12px 30px', background: '#3498db', color: 'white', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: '600' }}
                >
                  {isMobile ? '➤' : 'Send'}
                </button>
              </div>
            </form>
          </>
        ) : (
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#7f8c8d' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '48px', marginBottom: '20px' }}>💬</div>
              <div style={{ fontSize: '20px', fontWeight: '600' }}>Select a chat to start messaging</div>
            </div>
          </div>
        )}
      </div>

      {/* New Chat Modal */}
      {showNewChat && (
        <Modal onClose={() => { setShowNewChat(false); setSelectedUser(null); setSearchResults([]); setSearchQuery(''); }}>
          <h2 style={{ marginTop: 0 }}>Start New Chat</h2>
          <div style={{ marginBottom: '20px' }}>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search by email or username"
              style={{ width: '100%', padding: '10px', border: '2px solid #bdc3c7', borderRadius: '6px', marginBottom: '10px', boxSizing: 'border-box' }}
            />
            <button onClick={handleSearch} style={{ width: '100%', padding: '10px', background: '#3498db', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
              Search
            </button>
          </div>
          
          {searchResults.length > 0 && (
            <div style={{ marginBottom: '20px', maxHeight: '200px', overflowY: 'auto', border: '1px solid #bdc3c7', borderRadius: '6px' }}>
              {searchResults.map(u => (
                <div
                  key={u.id}
                  onClick={() => setSelectedUser(u)}
                  style={{
                    padding: '10px',
                    cursor: 'pointer',
                    background: selectedUser?.id === u.id ? '#ecf0f1' : 'white',
                    borderBottom: '1px solid #ecf0f1'
                  }}
                >
                  {u.username || u.email}
                </div>
              ))}
            </div>
          )}
          
          {selectedUser && (
            <>
              <div style={{ marginBottom: '10px', padding: '10px', background: '#ecf0f1', borderRadius: '6px' }}>
                Selected: <strong>{selectedUser.username || selectedUser.email}</strong>
              </div>
              <input
                type="text"
                value={newChatCode}
                onChange={(e) => setNewChatCode(e.target.value.slice(0, 4))}
                placeholder="Enter 4-character code"
                maxLength={4}
                style={{ width: '100%', padding: '10px', border: '2px solid #bdc3c7', borderRadius: '6px', marginBottom: '10px', boxSizing: 'border-box', textAlign: 'center', fontSize: '18px', letterSpacing: '5px' }}
              />
              <button onClick={handleSendRequest} style={{ width: '100%', padding: '12px', background: '#27ae60', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600' }}>
                Send Request
              </button>
            </>
          )}
        </Modal>
      )}

      {/* Requests Modal */}
      {showRequests && (
        <Modal onClose={() => { setShowRequests(false); setAcceptingRequestId(null); setAcceptCode(''); }}>
          <h2 style={{ marginTop: 0 }}>Chat Requests</h2>
          {requests.length === 0 ? (
            <p>No pending requests</p>
          ) : (
            requests.map(req => (
              <div key={req.id} style={{ padding: '15px', background: '#ecf0f1', borderRadius: '8px', marginBottom: '10px' }}>
                <div style={{ fontWeight: '600', marginBottom: '5px' }}>{req.username || req.email}</div>
                <div style={{ fontSize: '14px', color: '#7f8c8d', marginBottom: '10px' }}>
                  Code: <strong style={{ fontSize: '18px', letterSpacing: '3px' }}>{req.verification_code}</strong>
                </div>
                {acceptingRequestId === req.id ? (
                  <>
                    <input
                      type="text"
                      value={acceptCode}
                      onChange={(e) => setAcceptCode(e.target.value.slice(0, 4))}
                      placeholder="Your 4-character code"
                      maxLength={4}
                      style={{ width: '100%', padding: '8px', border: '2px solid #bdc3c7', borderRadius: '6px', marginBottom: '8px', boxSizing: 'border-box', textAlign: 'center', fontSize: '16px', letterSpacing: '5px' }}
                    />
                    <button onClick={() => handleAcceptRequest(req.id)} style={{ width: '100%', padding: '10px', background: '#27ae60', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
                      Confirm Accept
                    </button>
                  </>
                ) : (
                  <button onClick={() => setAcceptingRequestId(req.id)} style={{ width: '100%', padding: '10px', background: '#3498db', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer' }}>
                    Accept
                  </button>
                )}
              </div>
            ))
          )}
        </Modal>
      )}

      {/* Verification Modal */}
      {showVerification && (
        <Modal onClose={() => { setShowVerification(false); setVerificationCode(''); }}>
          <h2 style={{ marginTop: 0, color: '#e74c3c' }}>⚠️ Verification Required</h2>
          <p>Enter the other user's code to keep this chat active:</p>
          <input
            type="text"
            value={verificationCode}
            onChange={(e) => setVerificationCode(e.target.value.slice(0, 4))}
            placeholder="4-character code"
            maxLength={4}
            style={{ width: '100%', padding: '12px', border: '2px solid #e74c3c', borderRadius: '6px', marginBottom: '15px', boxSizing: 'border-box', textAlign: 'center', fontSize: '20px', letterSpacing: '8px' }}
          />
          <button onClick={handleVerifyChat} style={{ width: '100%', padding: '12px', background: '#27ae60', color: 'white', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: '600' }}>
            Verify Chat
          </button>
          <p style={{ fontSize: '12px', color: '#7f8c8d', marginTop: '10px', textAlign: 'center' }}>
            You have 5 minutes to verify or the chat will be destroyed
          </p>
        </Modal>
      )}
    </div>
  );
};

const Modal: React.FC<{ children: React.ReactNode; onClose: () => void }> = ({ children, onClose }) => (
  <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
    <div style={{ background: 'white', padding: '30px', borderRadius: '12px', maxWidth: '500px', width: '90%', maxHeight: '80vh', overflowY: 'auto', position: 'relative' }}>
      <button
        onClick={onClose}
        style={{ position: 'absolute', top: '15px', right: '15px', background: '#e74c3c', color: 'white', border: 'none', borderRadius: '50%', width: '30px', height: '30px', cursor: 'pointer', fontSize: '18px' }}
      >
        ×
      </button>
      {children}
    </div>
  </div>
);

const MessageContent: React.FC<{ content: string; chatId: number; messageType: string }> = ({ content, chatId, messageType }) => {
  const [decrypted, setDecrypted] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const decrypt = async () => {
      try {
        const sharedSecret = `chat_${chatId}_secret`;
        const msg = await crypto.decryptSimple(content, sharedSecret);
        setDecrypted(msg);
      } catch (error) {
        console.error('Decryption error:', error);
        setDecrypted('[Failed to decrypt]');
      }
      setLoading(false);
    };
    decrypt();
  }, [content, chatId]);

  if (loading) return <span>Decrypting...</span>;
  
  if (messageType === 'image') {
    return <img src={decrypted} alt="Shared image" style={{ maxWidth: '100%', borderRadius: '8px', marginTop: '5px' }} />;
  }
  
  return <span>{decrypted}</span>;
};
