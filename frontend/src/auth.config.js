import Credentials from 'next-auth/providers/credentials';
import { tokenLogin, tokenRefresh } from './api';
import Github from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Facebook from 'next-auth/providers/facebook';


const authOptions = {
  providers: [
    // Github({
    //   clientId: process.env.GITHUB_ID,
    //   clientSecret: process.env.GITHUB_SECRET,
    // }),
    // Google({
    //   clientId: process.env.GOOGLE_ID,
    //   clientSecret: process.env.GOOGLE_SECRET,
    // }),
    // Facebook({
    //   clientId: process.env.FACEBOOK_ID,
    //   clientSecret: process.env.FACEBOOK_SECRET,
    // }),
    Credentials({
      async authorize(credentials) {
        console.log("Triggering Credentials");
        const { email, password } = credentials;

        try {
          const response = await tokenLogin({ email, password });

          if (response.data) {
            const { access, refresh } = response.data;

            return {
              accessToken: access,
              refreshToken: refresh
            };
          };
          
          throw new Error('Invalid credentials');
        } catch (error) {
          console.error("Authorization Error:", error);
          throw new Error(error.message);
        };
      },
    }),
  ],
};

export const refresh_token = async (token) => {
  try {
    const response = await tokenRefresh(token.refreshToken);

    return {
      ...token,
      accessToken: response.access,
      refreshToken: response.refresh,
      accessTokenExpires: Math.floor(Date.now() / 1000) + 10,
      refreshTokenExpires: Math.floor(Date.now() / 1000) + 24 * 60 * 60,
    };
  } catch (error) {
    console.error("Failed to refresh token:", error);
    return null; // Returning null invalidates the session
  }
}

export default authOptions;
