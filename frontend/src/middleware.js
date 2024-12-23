import { NextResponse } from "next/server";
import { tokenVerify, tokenRefresh, retrieveTokenId } from "@/api/route";
import { getSessionId, setSessionId, deleteSessionId } from "./utils/session";
import { fetchCsrfToken } from "@/api/route";


export default async function tokenMiddleware(req) {
  const session = await getSessionId();
  console.log('session:', session);

  if (!session) {
    return NextResponse.redirect(new URL('/login', req.url));
  };

  let { sessionId, tokens } = session;

  if (!tokens) {
    try {
      console.log('Retrieving token ID....');
      tokens = await retrieveTokenId();
    } catch (error) {
      console.error('Error retrieving token ID:', error);
      return NextResponse.redirect(new URL('/login', req.url));
    };
  };

  console.log('tokens:', tokens);
  const { access_token, refresh_token } = tokens;
  console.log('Token access and refresh got');

  try {
    const response = await tokenVerify(access_token.value);

    if (response.status === 200) {
      console.log('Token verification successful');
      return NextResponse.next();
    } else {
      console.log(`Token verification failed: ${response.status}`);
      return NextResponse.redirect(new URL('/login', req.url));
    };

  } catch (error) {
    if (error.response.status === 401 && refresh_token) {
      try {
        const refreshResponse = await tokenRefresh(refresh_token.value);
        const newTokens = refreshResponse.data;
        await deleteSessionId();
        await setSessionId(sessionId, newTokens);
        console.log('Token refreshed');
        return NextResponse.next();
      } catch (error) {
        console.error('Error refreshing token:', error);
        return NextResponse.redirect(new URL('/login', req.url));
      };
    } else {
      console.error('Error verifying token:', error);
      return NextResponse.redirect(new URL('/login', req.url));
    };
  };
};

export const config = {
  matcher: ['/sphere/:path*'],
}