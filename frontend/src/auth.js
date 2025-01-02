import NextAuth from "next-auth";
import authOptions, { refresh_token } from "./auth.config";

export const { handlers, signIn, signOut, auth } = NextAuth({
  pages: {
    signIn: "/auth/login",
  },
  callbacks: {
    async jwt({ token, user }) {
      const now = Math.floor(Date.now() / 1000); // Current time in seconds
      // On login, set initial token values
      if (user) {
        console.log("Setting initial token values");
        token.accessToken = user.accessToken;
        token.refreshToken = user.refreshToken;
        token = {
          ...token,
          accessTokenExpires: Math.floor(Date.now() / 1000) + 20,
          refreshTokenExpires: Math.floor(Date.now() / 1000) + 24 * 60 * 60,
        };
        return token;
      };

      // Validate refresh token expiry
      if (token.refreshTokenExpires && token.refreshTokenExpires < now) {
        console.warn("Refresh token expired. Logging out...");
        return null; // Returning null invalidates the session
      };

      // Validate access token expiry
      if (token.accessTokenExpires && token.accessTokenExpires < now) {

        const refreshedToken = await refresh_token(token); // Get the refreshed token
        if (refreshedToken) {
          return refreshedToken; // Return the updated token
        } else {
          return null; // Token refresh failed, invalidate session
        };
      };

      return token; // Return updated token
    },

    async session({ session, token }) {
      if (!token) {
        // If the token is null (e.g., refresh token expired), invalidate the session
        console.warn("Session invalidated due to expired or missing tokens.");
        return null;
      }

      session.accessToken = token.accessToken;
      session.refreshToken = token.refreshToken;
      session.accessTokenExpires = token.accessTokenExpires;
      session.refreshTokenExpires = token.refreshTokenExpires;

      return session;
    },
  },
  ...authOptions,
  session: {
    strategy: "jwt",
  },
  trustHost: true,
  secret: process.env.AUTH_SECRET,
});