'use client'

import { useFormStatus } from "react-dom";

export function LoginButton () {
  const { pending } = useFormStatus()

  return (
    <button disabled={pending} type="submit">
      {pending ? 'Logging in...' : 'Login'}
    </button>
  );
}