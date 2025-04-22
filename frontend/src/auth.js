import NextAuth from "next-auth";
import GoogleProvider from "next-auth/providers/google";
import FacebookProvider from "next-auth/providers/facebook";
import GitHubProvider from "next-auth/providers/github";
import { socialLoginAction } from "./actions/authActions";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    }),
    FacebookProvider({
      clientId: process.env.FACEBOOK_CLIENT_ID,
      clientSecret: process.env.FACEBOOK_CLIENT_SECRET,
      authorization: {
        params: {
          scope: "email,public_profile", // request email and public profile
        },
      },
    }),
    GitHubProvider({
      clientId: process.env.GITHUB_CLIENT_ID,
      clientSecret: process.env.GITHUB_CLIENT_SECRET,
    }),
  ],
  trustHost: process.env.NEXTAUTH_TRUSTED_HOST,
  baseUrl: process.env.NEXTAUTH_URL,
  callbacks: {
    /* eslint-disable-next-line no-unused-vars */
    async signIn({ user, account, profile, email, credentials }) {
      let result;
      if (account.provider === "google") {
        result = await socialLoginAction("google-oauth2", account.access_token);
      }

      if (account.provider === "facebook") {
        result = await socialLoginAction("facebook", account.access_token);
      }

      if (account.provider === "github") {
        result = await socialLoginAction("github", account.access_token);
      }

      if (result?.error) {
        return `/auth/login?error=${result.error}`;
      }

      return true;
    },
    async jwt({ token, account }) {
      if (account) {
        token.accessToken = account.access_token;
      }
      return token;
    },
  },
});
