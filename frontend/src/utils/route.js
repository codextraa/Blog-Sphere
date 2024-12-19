import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
};

api.interceptors.response.use((config) => {
  const csrfToken = getCookie('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

//API Endpoints
export const login = async (credentials) => {
  return api.post('token/', credentials);
};

export const refreshAccessToken = async () => {
  return api.post('token/refresh/');
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