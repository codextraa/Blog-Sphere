import authConfig from "./auth.config";
import NextAuth from "next-auth";
import {
  DEFAULT_LOGIN_REDIRECT,
  apiAuthPrefix,
  authRoutes,
} from "./route";

const { auth } = NextAuth(authConfig);

export default auth(async (req) => {
    console.log('Middleware running');
    const { nextUrl } = req; // The request URL
    const isLoggedIn = !!req.auth; // Check if the user is logged in

    const isApiAuthRoute = nextUrl.pathname.startsWith(apiAuthPrefix); // Check API auth route
    const isAuthRoute = authRoutes.includes(nextUrl.pathname); // Check login/signup route

    // console.log('req.auth:', req.auth);
    // console.log('isLoggedIn:', isLoggedIn);
    // console.log('nextUrl.pathname:', nextUrl.pathname);
    // console.log(`isApiAuthRoute: ${isApiAuthRoute}`, `isAuthRoute: ${isAuthRoute}`);

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
};