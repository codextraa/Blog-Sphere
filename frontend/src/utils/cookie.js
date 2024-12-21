'use client';

export function setTokencookie(access, refresh) {
  document.cookie = `access_token=${access}; path=/sphere; SameSite=strict; Secure;`;
  document.cookie = `refresh_token=${refresh}; path=/sphere; SameSite=strict; Secure;`;
}