'use server';

import { revalidatePath } from 'next/cache';
import { tokenLogin } from '@/api/route';
import { fetchCsrfToken } from '@/api/route';
import { setSessionId } from './session';

export async function loginUser(prevState, formData) {
  const credentials = {
    email: formData.get('email'),
    password: formData.get('password')
  };

  try {
    // const csrftoken = await fetchCsrfToken();

    const response = await tokenLogin(credentials);

    console.log('response');

    if (response && response.status === 200) {
      console.log('Login successful');
      const { sessionId, access, refresh } = response.data;
      console.log('response data', response.data);
      await setSessionId(sessionId, { access_token : access, refresh_token : refresh });
      revalidatePath('/sphere');  

      return {
        success: true,
        errors: null
      }
    } else {
      console.log('Login failed');
      return {
        errors: 'Login failed. Please try again.'
      }
    }
    
  } catch (error) {
    // error for the server
    console.error("Unexpected server error: ", error);
    // error for the client
    return { errors: 'Invalid login credentials. Please try again.' };
  };
};

// Djangosun@123