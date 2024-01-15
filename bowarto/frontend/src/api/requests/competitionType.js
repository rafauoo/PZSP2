import { competitionTypesUrl } from "../urls";
import { apiRequest } from "./base";

export const getCompetitionTypes = async () => {
  try {
    return await apiRequest(competitionTypesUrl, {
      method: 'GET', headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.error('Error fetching competition types:', error.message);
    throw error;
  }
};
