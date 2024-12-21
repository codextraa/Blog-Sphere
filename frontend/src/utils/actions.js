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
    };

  } catch (error) {
    // error for the server
    console.error("Unexpected server error message: ", error.response?.data || error.message);
    console.error("Unexpected server error: ", error);
    // error for the client
    return { errors: 'Invalid login credentials. Please try again.' };
  };

  revalidatePath('/');
  redirect('/');
};

// Djangosun@123