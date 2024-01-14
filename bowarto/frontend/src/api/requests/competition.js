import {apiRequest} from "./base";
import {competitionsUrl} from "../urls";

export const getCompetitionList = async () => {
  try {
    return await apiRequest(competitionsUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Error fetching competitions:', error.message);
    throw error;
  }
};

export const getCompetitionByID = async (competitionID) => {
  try {
    return await apiRequest(`${competitionsUrl}${competitionID}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Error fetching competition by ID:', error.message);
    throw error;
  }
};


export const createCompetition = async (competitionData) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(competitionsUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(competitionData),
    });
  } catch (error) {
    console.error('Error creating competition:', error.message);
    throw error;
  }
};

export const editCompetition = async (competitionID, competitionData) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${competitionsUrl}${competitionID}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(competitionData),
    });
  } catch (error) {
    console.error('Error editing competition:', error.message);
    throw error;
  }
};

export const deleteCompetitionByID = async (competitionID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${competitionsUrl}${competitionID}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error deleting competition:', error.message);
    throw error;
  }
};
