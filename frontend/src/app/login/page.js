'use client';

import { useActionState } from 'react';
// import { classes } from './page.module.css';
import { LoginButton } from '@/components/button';
import { loginUser } from "@/utils/actions";

export default function loginPage () {
  const [state, formAction] = useActionState(loginUser, { errors: null });

  return (
    <div>
      <header>
        <h1>Login</h1>
      </header>
      <main>
        <form action={formAction}>
          {state.errors && <p>{state.errors}</p>}
          {/* {state.errors && (
            <ErrorAlert message={state.errors} onClose={() => {}} />
          )} */}
          <p>
            <label htmlFor="email">Email:</label>
            <input type="text" id="email" name="email" required />
          </p>
          <p>
            <label htmlFor="password">Password:</label>
            <input type="password" id="password" name="password" required />
          </p>
          <LoginButton />
        </form>
      </main>
    </div>
  );
};