import Credentials from 'next-auth/providers/credentials';
import { tokenLogin } from './api';
import { setSessionId } from './utils/session';
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
            const { sessionId, access, refresh } = response.data;

            return { sessionId, access, refresh };
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

export default authOptions;
