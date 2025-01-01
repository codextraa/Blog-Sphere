// import { NextResponse } from "next/server";
// import { tokenVerify, tokenRefresh, retrieveTokenId } from "./api";
// import { getSessionId, setSessionId, deleteSessionId } from "./utils/session";
// import { fetchCsrfToken } from "./api";


// export default async function tokenMiddleware(req) {
//   const session = await getSessionId();
//   console.log('session:', session);

//   if (!session) {
//     return NextResponse.redirect(new URL('/login', req.url));
//   };

//   let { sessionId, tokens } = session;

//   if (!tokens) {
//     try {
//       console.log('Retrieving token ID....');
//       tokens = await retrieveTokenId();
//     } catch (error) {
//       console.error('Error retrieving token ID:', error);
//       return NextResponse.redirect(new URL('/login', req.url));
//     };
//   };

//   console.log('tokens:', tokens);
//   const { access_token, refresh_token } = tokens;
//   console.log('Token access and refresh got');

//   try {
//     const response = await tokenVerify(access_token.value);

//     if (response.status === 200) {
//       console.log('Token verification successful');
//       return NextResponse.next();
//     } else {
//       console.log(`Token verification failed: ${response.status}`);
//       return NextResponse.redirect(new URL('/login', req.url));
//     };

//   } catch (error) {
//     if (error.response.status === 401 && refresh_token) {
//       try {
//         const refreshResponse = await tokenRefresh(refresh_token.value);
//         const newTokens = refreshResponse.data;
//         await deleteSessionId();
//         await setSessionId(sessionId, newTokens);
//         console.log('Token refreshed');
//         return NextResponse.next();
//       } catch (error) {
//         console.error('Error refreshing token:', error);
//         return NextResponse.redirect(new URL('/login', req.url));
//       };
//     } else {
//       console.error('Error verifying token:', error);
//       return NextResponse.redirect(new URL('/login', req.url));
//     };
//   };
// };

import authConfig from "./auth.config";
import NextAuth from "next-auth";
import {
  DEFAULT_LOGIN_REDIRECT,
  apiAuthPrefix,
  authRoutes,
} from "./route";

const { auth } = NextAuth(authConfig);

export default auth((req) => {
    console.log('Middleware running');
    console.log('Request Headers:', req.headers);
    const { nextUrl } = req; // The request URL
    const isLoggedIn = !!req.auth; // Check if the user is logged in

    const isApiAuthRoute = nextUrl.pathname.startsWith(apiAuthPrefix); // Check API auth route
    const isAuthRoute = authRoutes.includes(nextUrl.pathname); // Check login/signup route

    console.log('req.auth:', req.auth);
    console.log('isLoggedIn:', isLoggedIn);
    console.log('nextUrl.pathname:', nextUrl.pathname);
    console.log(`isApiAuthRoute: ${isApiAuthRoute}`, `isAuthRoute: ${isAuthRoute}`);

    // Skip API auth routes
    if (isApiAuthRoute) {
        console.log('Skipping API auth route');
        return undefined;
    }

    // Handle auth routes (login, register)
    if (isAuthRoute) {
        console.log('Handling auth route');
        if (isLoggedIn) {
            console.log('User is logged in, redirecting to /');
            // Avoid loop by skipping middleware for DEFAULT_LOGIN_REDIRECT
            if (nextUrl.pathname === DEFAULT_LOGIN_REDIRECT) {
                console.log('Skipping middleware for DEFAULT_LOGIN_REDIRECT');
                return undefined;
            }
            return Response.redirect(new URL(DEFAULT_LOGIN_REDIRECT, nextUrl));
        }
        return undefined;
    }

    // Redirect unauthenticated users to login
    if (!isLoggedIn) {
        console.log('User is not logged in, redirecting to /auth/login');
        if (nextUrl.pathname === '/auth/login') {
            // Prevent redirect loop for login page
            console.log('Skipping middleware for /auth/login');
            return undefined;
        }
        return Response.redirect(new URL('/auth/login', nextUrl));
    }

    return undefined;
});

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
    '/',
  ],
}