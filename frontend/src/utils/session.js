import { cookies } from 'next/headers';


const tokenStore = new Map(); // lost while reloaded

const getTokens = (sessionId) => {
  console.log(tokenStore);
  console.log(sessionId);
  console.log('get token', tokenStore.get(sessionId));
  return tokenStore.get(sessionId);
};

const saveTokens = (sessionId, tokens) => {
  tokenStore.set(sessionId, tokens);
};


const deleteTokens = (sessionId) => {
  tokenStore.delete(sessionId);
};

export const getSessionId = async () => {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get('sessionId');
  console.log('get cookie', sessionId);
  if (sessionId) {
    const tokens = getTokens(sessionId.value);
    return {
      sessionId: sessionId.value,
      tokens
    }
  }
  return null;
};

export const setSessionId = async (sessionId, tokens) => {
  const cookieStore = await cookies();
  saveTokens(sessionId, tokens);
  console.log('set token', tokenStore);
  cookieStore.set('sessionId', sessionId, {
    httpOnly: true, // Prevent client-side access
    secure: true, // HTTPS in production
    sameSite: 'Lax', // Required for cross-site requests
    maxAge: 1 * 24 * 60 * 60 // 1 day
  });
  console.log('set cookie', cookieStore);
};

export const deleteSessionId = async () => {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get('sessionId');
  if (sessionId) {
    deleteTokens(sessionId.value);
  }
  cookieStore.delete('sessionId');
};
