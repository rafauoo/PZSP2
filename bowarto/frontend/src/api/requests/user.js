import {apiRequest} from "./base";
import {usersUrl, meUrl} from "../urls";

export const getUserList = async () => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(usersUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,

      },
    });
  } catch (error) {
    console.error('Error fetching users:', error.message);
    throw error;
  }
};

export const getUserByID = async (userID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${usersUrl}${userID}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,

      },
    });
  } catch (error) {
    console.error('Error fetching user by ID:', error.message);
    throw error;
  }
};

export const editUser = async (userID, userData) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${usersUrl}${userID}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(userData),
    });
  } catch (error) {
    console.error('Error editing user:', error.message);
    throw error;
  }
};

export const deleteUserByID = async (userID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${usersUrl}${userID}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error deleting user:', error.message);
    throw error;
  }
};
