import {apiRequest} from "./base";
import {participantsUrl} from "../urls";

export const getParticipantList = async () => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(participantsUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching participants:', error.message);
    throw error;
  }
};

export const getParticipantListByApplicationID = async (applicationID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${participantsUrl}?application=${applicationID}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching participants for an application:', error.message);
    throw error;
  }
};

export const createParticipant = async (participantData) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(participantsUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(participantData),
    });
  } catch (error) {
    console.error('Error creating participant:', error.message);
    throw error;
  }
};

export const getParticipantByID = async (participantID) => {
  try {
    const accessToken = sessionStorage.getItem('access');

    return await apiRequest(`${participantsUrl}${participantID}/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching participant by ID:', error.message);
    throw error;
  }
};

export const editParticipant = async (participantID, participantData) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${participantsUrl}${participantID}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
      body: JSON.stringify(participantData),
    });
  } catch (error) {
    console.error('Error editing participant:', error.message);
    throw error;
  }
};

export const deleteParticipant = async (participantID) => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(`${participantsUrl}${participantID}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error deleting participant:', error.message);
    throw error;
  }
};
