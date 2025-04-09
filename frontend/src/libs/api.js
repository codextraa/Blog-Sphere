import { ApiClient } from "./apiClient";
import { getRefreshTokenFromSession } from "./cookie";

const HTTPS = process.env.HTTPS === "true";
const API_URL = HTTPS
  ? process.env.API_BASE_HTTPS_URL
  : process.env.API_BASE_URL;
const apiClient = new ApiClient(API_URL);

// API functions
export const getCSRFToken = async () => {
  return apiClient.get("/auth-api/get-csrf-token/");
};

export const recaptchaVerify = async (data) => {
  return apiClient.post("/auth-api/recaptcha-verify/", data);
};

export const login = async (data) => {
  return apiClient.post("/auth-api/login/", data);
};

export const getToken = async (data) => {
  return apiClient.post("/auth-api/token/", data);
};

export const resendOtp = async (data) => {
  return apiClient.post("/auth-api/resend-otp/", data);
};

export const refreshToken = async (refreshToken) => {
  return await apiClient.post("/auth-api/token/refresh/", {
    refresh: refreshToken,
  });
};

export const verifyEmail = async (token, expiry) => {
  const queryParams = new URLSearchParams({ token, expiry }).toString();
  return apiClient.get(`/auth-api/verify-email/?${queryParams}`);
};

export const requestEmailVerification = async (data) => {
  return apiClient.post("/auth-api/verify-email/", data);
};

export const requestPhoneVerification = async (data) => {
  return apiClient.post("/auth-api/verify-phone/", data);
};

export const verifyPhone = async (data) => {
  return apiClient.patch("/auth-api/verify-phone/", data);
};

export const verifyPassResetLink = async (token, expiry) => {
  const queryParams = new URLSearchParams({ token, expiry }).toString();
  return apiClient.get(`/auth-api/reset-password/?${queryParams}`);
};

export const requestPasswordReset = async (data) => {
  return apiClient.post("/auth-api/reset-password/", data);
};

export const resetPassword = async (token, expiry, data) => {
  const queryParams = new URLSearchParams({ token, expiry }).toString();
  return apiClient.patch(`/auth-api/reset-password/?${queryParams}`, data);
};

export const logout = async () => {
  const refreshToken = await getRefreshTokenFromSession();

  if (refreshToken) {
    await apiClient.post("/auth-api/logout/", { refresh: refreshToken });
  }
};

export const socialOauth = async (data) => {
  return apiClient.post("/auth-api/social-auth/", data);
};

export const getUsers = async (queryParams = {}) => {
  const params = new URLSearchParams(queryParams);
  return apiClient.get(`/auth-api/users/?${params.toString()}`);
};

export const getUser = async (id) => {
  return apiClient.get(`/auth-api/users/${id}/`);
};

export const createUser = async (data) => {
  return apiClient.post("/auth-api/users/", data);
};

export const updateUser = async (id, data) => {
  return apiClient.patch(`/auth-api/users/${id}/`, data);
};

export const deleteUser = async (id) => {
  return apiClient.delete(`/auth-api/users/${id}/`);
};

export const activateUser = async (id) => {
  return apiClient.patch(`/auth-api/users/${id}/activate-user/`);
};

export const deactivateUser = async (id) => {
  return apiClient.patch(`/auth-api/users/${id}/deactivate-user/`);
};

export const uploadProfileImage = async (id, data) => {
  return apiClient.patch(`/auth-api/users/${id}/upload-image/`, data, {}, true);
};
