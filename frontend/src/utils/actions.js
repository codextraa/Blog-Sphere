'use server';

import { redirect } from 'next/navigation';
import { revalidatePath } from 'next/cache';
import { login } from '@/api/route';
import { fetchCsrfToken } from '@/api/route';

export async function loginUser(prevState, formData) {
  const credentials = {
    email: formData.get('email'),
    password: formData.get('password')
  };

  try {
    const csrfToken = await fetchCsrfToken();

    const response = await login(credentials, csrfToken);

    if (response && response.status === 200) {
      console.log('Login successful');
      console.log(response.data);
      
      // Revalidate the page
      revalidatePath('/sphere');

      return {
        accessToken: response.data.access,
        refreshToken: response.data.refresh,
        errors: null
      }
    };
    
  } catch (error) {
    // error for the server
    console.error("Unexpected server error: ", error);
    // error for the client
    return { errors: 'Invalid login credentials. Please try again.' };
  };
};

// Djangosun@123