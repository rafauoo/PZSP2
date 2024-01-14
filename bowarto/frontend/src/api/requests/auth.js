import {apiRequest} from "./base";
import {loginUrl, meUrl, refreshUrl, registerUrl} from "../urls";

export const refreshAccessToken = async (refreshToken) => {
  try {
    const data = await apiRequest(refreshUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        refresh: refreshToken,
      }),
    });

    return data.access;
  } catch (error) {
    console.error('Error refreshing access token:', error.message);
    throw error;
  }
};

export const loginUser = async (credentials) => {
  try {
    return await apiRequest(loginUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
  } catch (error) {
    console.error('Error during login:', error.message);
    throw error;
  }
};

export const logoutUser = async (refreshToken) => {
  try {
    await apiRequest(loginUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        refresh: refreshToken,
      }),
    });
  } catch (error) {
    console.error('Error during logout:', error.message);
    throw error;
  }
};

export const registerUser = async (userData) => {
  try {
    return await apiRequest(registerUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
  } catch (error) {
    console.error('Error during registration:', error.message);
    throw error;
  }
};

export const getMe = async () => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(meUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error getting user details:', error.message);
    throw error;
  }
};