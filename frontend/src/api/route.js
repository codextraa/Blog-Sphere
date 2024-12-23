import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true,
});

api.interceptors.request.use(request => {
  console.log('Request Headers:', request.headers);
  return request;
});

// export const retrieveTokenId = async () => {
//   try {
//     const response = await fetch(`${API_BASE_URL}/retrieve-token/`, {
//       method: 'GET',
//       headers: {
//         'Content-Type': 'application/json',
//         'Accept': 'application/json',
//       },
//       credentials: 'include',
//     });

//     if (response.status === 200) {
//       const data = await response.json();
//       return data.sessionId;
//     } else {
//       console.error('Error retrieving session ID:', response.status);
//       return null;
//     }
//   } catch (error) {
//     console.error('Error retrieving:', error);
//     return null;
//   }
// };

export const retrieveTokenId = async () => {
  try {
    const response = await api.get('retrieve-token/');
    return response.data.sessionId;
  } catch (error) {
    console.error('Error retrieving session ID:', error);
    return null;
  }
}

//API Endpoints
export const tokenLogin = async (credentials) => {
  return api.post('token/', credentials);
};

export const tokenRefresh = async () => {
  // csrfToken = await fetchCsrfToken();
  return api.post('token/refresh/');
};

export const tokenVerify = async (token) => {
  // setCsrfToken(csrfToken);
  // return api.post('token/verify/', { token: access_token }); // Verify token
  const response = await fetch(`${API_BASE_URL}/token/verify/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json', // Ensure correct content type
    },
    body: JSON.stringify({ token }), // Send token in the body with the correct key
  });

  return response;
};

export const fetchUsers = async() => {
  return api.get('users/');
};

export const fetchUsersById = async (id) => {
  return api.get(`users/${id}/`);
};

export const createUser = async (userData) => {
  return api.post('users/', userData);
};

export const updateUser = async (id, userData) => {
  return api.patch(`users/${id}/`, userData);
};

export const deleteUser = async (id) => {
  return api.delete(`users/${id}/`);
};

export const fetchCategories = async() => {
  return api.get('categories/');
};

export const fetchCategoriesById = async (id) => {
  return api.get(`categories/${id}/`);
};

export const createCategory = async (categoryData) => {
  return api.post('categories/', categoryData);
};

export const updateCategory = async (id, categoryData) => {
  return api.patch(`categories/${id}/`, categoryData);
};

export const deleteCategory = async (id) => {
  return api.delete(`categories/${id}/`);
};

export const fetchBlogs = async() => {
  return api.get('blogs/');
};

export const fetchBlogsById = async (id) => {
  return api.get(`blogs/${id}/`);
};

export const createBlog = async (blogData) => {
  return api.post('blogs/', blogData);
};

export const updateBlog = async (id, blogData) => {
  return api.patch(`blogs/${id}/`, blogData);
};

export const deleteBlog = async (id) => {
  return api.delete(`blogs/${id}/`);
};


// api.interceptors.response.use(
//   (response) => response,
//   async (error) => {
//     const originalRequest = error.config;
//     if (
//       error.response.status === 401 && // Unauthorized error
//       !originalRequest._retry // Avoid infinite loop
//     ) {
//       originalRequest._retry = true;
//       try {
//         // Refresh the token
//         const csrfToken = await fetchCsrfToken();
//         if (csrfToken) {
//           setCsrfToken(csrfToken);
//         }
//         await refreshAccessToken();
//         return api(originalRequest); // Retry original request
//       } catch (refreshError) {
//         console.error('Token refresh failed:', refreshError);
//         return Promise.reject(refreshError);
//       }
//     }
//     return Promise.reject(error);
//   }
// );

// let csrfToken = null;

// api.interceptors.request.use(
//   (config) => {
//     if (config.headers['X-CSRFToken'] === undefined) {
//       console.log('setting csrf token');
//       config.headers['X-CSRFToken'] = csrfToken; // Set CSRF token in headers
//     };
//     console.log(config);
//     console.log(config.headers);
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );


// const setCsrfToken = (token) => {
//   api.defaults.headers['X-CSRFToken'] = token;
// };

// export const fetchCsrfToken = async () => {
//   try {
//     const response = await api.get('get-csrf-token/');
//     return response.data.csrfToken;
//   } catch (error) {
//     console.error('Error fetching CSRF token:', error);
//     return null;
//   }
// };