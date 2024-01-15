import {apiRequest} from "./base";
import {statsUrl} from "../urls";

export const getStats = async () => {
  try {
    const accessToken = sessionStorage.getItem('access');
    return await apiRequest(statsUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });
  } catch (error) {
    console.error('Error fetching stats:', error.message);
    throw error;
  }
};
