'use server';

// import { revalidatePath } from 'next/cache';
// import { tokenLogin } from '../../api';
// import { fetchCsrfToken } from '../../api';
// import { setSessionId } from '../utils/session';
import { AuthError } from 'next-auth';
import { signIn } from '@/auth';
import { DEFAULT_LOGIN_REDIRECT } from '@/route';

export async function loginUser(prevState, formData) {
  console.log("Triggered loginUser");
  let email = formData.get('email');
  let password = formData.get('password');

  if (email === '' || password === '') {
    return {
      errors: 'Email and password are required.'
    };
  };  

  try {
    await signIn("credentials", {
      email,
      password,
      redirectTo: DEFAULT_LOGIN_REDIRECT
    });
  } catch (error) {
    // error for server
    console.error(error);
    if (error instanceof AuthError) {
        switch (error.type) {
            case "CredentialsSignin":
                return { error: "Invalid credentials" };
            default:
                return { error: "Something went wrong" };
        };
    };

    throw error;
  };
};

// Djangosun@123

