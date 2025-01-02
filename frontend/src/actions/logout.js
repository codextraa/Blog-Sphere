'use server';

import { auth, signOut } from '@/auth';


export async function automaticlogout() {
  const session = await auth();
  if (!session) {
    await signOut(auth);
  }
}