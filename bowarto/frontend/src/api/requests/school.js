import {apiRequest} from "./base";
import {schoolsUrl} from "../urls";

export const getSchoolList = async () => {
  try {
    // TODO     const accessToken = sessionStorage.getItem('access');

    return await apiRequest(schoolsUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        //TODO         'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching schools:', error.message);
    throw error;
  }
};

export const createSchool = async (schoolData) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(schoolsUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(schoolData),
    });
  } catch (error) {
    console.error('Error creating school:', error.message);
    throw error;
  }
};

export const getSchoolByID = async (schoolID) => {
  try {
    // TODO     const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${schoolsUrl}${schoolID}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        // TODO         'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching school by ID:', error.message);
    throw error;
  }
};

export const editSchool = async (schoolID, schoolData) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${schoolsUrl}${schoolID}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(schoolData),
    });
  } catch (error) {
    console.error('Error editing school:', error.message);
    throw error;
  }
};

export const deleteSchool = async (schoolID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${schoolsUrl}${schoolID}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error deleting school:', error.message);
    throw error;
  }
};
