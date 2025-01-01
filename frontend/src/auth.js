import NextAuth from "next-auth";
import authOptions from "./auth.config";

export const { handlers, signIn, signOut, auth } = NextAuth({
  pages: {
    signIn: "/auth/login",
  },
  callbacks: {
    async session({ session, token }) {
      // Add the access and refresh tokens to the session object
      if (token.access) {
        session.accessToken = token.access;
      }
      if (token.refresh) {
        session.refreshToken = token.refresh;
      }
      return session;
    },
    async jwt({ token, user }) {
      if (user) {
        // Store access and refresh tokens in JWT token
        token.access = user.access;
        token.refresh = user.refresh;
      }
      return token;
    },
  },
  ...authOptions,
  trustHost: true,
  secret: process.env.AUTH_SECRET,
  // useSecureCookies: process.env.NODE_ENV === "production",
})