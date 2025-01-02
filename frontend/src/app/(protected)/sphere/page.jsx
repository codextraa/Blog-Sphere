import { auth, signOut } from '@/auth';

export default async function Home() {
  const session = await auth();
  console.log("Session: ", session);

  return (
    <div>
      <h1>Home</h1>
    </div>
  );
}