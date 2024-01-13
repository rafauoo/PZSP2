import {apiRequest} from "./base";
import {filesUrl} from "../urls"; // Make sure to import the correct URL for files

export const getFileList = async () => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(filesUrl, {
      method: 'GET', headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching files:', error.message);
    throw error;
  }
};

export const getFileByID = async (fileID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${filesUrl}${fileID}/`, {
      method: 'GET', headers: {
        'Authorization': `Bearer ${accessToken}`,
      }, responseType: 'arraybuffer'
    });
  } catch (error) {
    console.error('Error fetching file by ID:', error.message);
    throw error;
  }
};

export const deleteFile = async (fileID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${filesUrl}${fileID}/`, {
      method: 'DELETE', headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error deleting file:', error.message);
    throw error;
  }
};
