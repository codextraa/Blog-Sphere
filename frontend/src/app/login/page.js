'use client';

import { useActionState } from 'react';
import classes from './page.module.css';
import { LoginButton } from '@/components/button';
import { loginUser } from "@/utils/actions";
import Image from 'next/image';
import logoImg from '@/icons/circle_design.svg';

export default function loginPage () {
  const [state, formAction] = useActionState(loginUser, { errors: null });

  if (state.success) {
    // Redirect the user to /sphere
    window.location.href = '/sphere';
  }

  return (
    <div className={classes.login_container}>
        <div className={classes.logo}>
            <Image src={logoImg} className={classes.logo_icon} alt="Blog-Sphere-logo" priority />
            <span>SPHERE</span>


          </div>
          <div className={classes.login_form_container}>
            <h1>Login</h1>
            <form action={formAction} className={classes.login_form}>
              {state.errors && <p>{state.errors}</p>}
              {/* {state.errors && (
                <ErrorAlert message={state.errors} onClose={() => {}} />
              )} */}
              <div className= {classes.input_group}>
                <input type="text" placeholder="EMAIL" name="email" required/>
                <i className= {classes.user_icon}></i>
              </div>

              <div className = {classes.input_group}>
                <input type="password" placeholder="PASSWORD" name='password' required/>
                <i className= {classes.password_icon}></i>
              </div>
              <LoginButton />
            </form>
        </div>
      </div>
  );
};
