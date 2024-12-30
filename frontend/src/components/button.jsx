'use client'

import { useFormStatus } from "react-dom";
import classes from "./button.module.css"

export function LoginButton () {
  const { pending } = useFormStatus()

  return (
    <button disabled={pending} type="submit" className={classes.login_button} >
      {pending ? 'Logging in...' : 'Login'}
    </button>
  );
}