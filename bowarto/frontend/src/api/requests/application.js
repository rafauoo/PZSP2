import {apiRequest} from "./base";
import {applicationsUrl} from "../urls";

export const getApplicationList = async () => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(applicationsUrl, {
      method: 'GET', headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching applications:', error.message);
    throw error;
  }
};

export const getApplicationListByCompetitionID = async (competitionID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${applicationsUrl}?competition=${competitionID}`, {
      method: 'GET', headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching applications for a competition:', error.message);
    throw error;
  }
};

export const createApplication = async (applicationData) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(applicationsUrl, {
      method: 'POST', headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      }, body: JSON.stringify(applicationData),
    });
  } catch (error) {
    console.error('Error creating application:', error.message);
    throw error;
  }
};

export const getApplicationByID = async (applicationID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${applicationsUrl}${applicationID}/`, {
      method: 'GET', headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching application by ID:', error.message);
    throw error;
  }
};

export const deleteApplication = async (applicationID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${applicationsUrl}${applicationID}/`, {
      method: 'DELETE', headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error deleting application:', error.message);
    throw error;
  }
};
