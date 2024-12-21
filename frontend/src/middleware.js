import { NextResponse } from "next/server";
import { tokenVerify } from "@/api/route";
import { fetchCsrfToken } from "@/api/route";


export default async function tokenMiddleware(req) {
  const { cookies } = req;
  const access_token = cookies.get('access_token');

  if (!access_token) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  try {
    const csrfToken = await fetchCsrfToken();

    const response = await tokenVerify(access_token.value, csrfToken);

    if (response.status === 200) {
      return NextResponse.next();
    } else {
      console.log(`Token verification failed: ${response.status}`);
      return NextResponse.redirect(new URL('/login', req.url));
    };

  } catch (error) {
    console.error('Error verifying token:', error);
    return NextResponse.redirect(new URL('/login', req.url));
  }
}

export const config = {
  matcher: ['/sphere/:path*'],
}