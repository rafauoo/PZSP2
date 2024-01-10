import refreshAccessToken from "./refresh";

export const fetchDataFromApi = async (url) => {
  try {
    await refreshAccessToken();
    const token = sessionStorage.getItem('access');
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      }
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    return await response.json();
  } catch (error) {
    throw new Error(`Error fetching data from ${url}: ${error}`);
  }
};

export async function submitForm(competitionId, formData) {
  try {
    console.log(competitionId, formData)
    // Step 1: Try to fetch existing applications for the given competitionId
    console.log(competitionId)
    await refreshAccessToken();
    const token = sessionStorage.getItem('access');
    const apiUrl = `http://20.108.53.69/api/applications/?competition=${competitionId}`;
    const response = await fetch(apiUrl, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      }
    });
    const existingApplications = await response.json();
    // Step 2: Check if the list is empty
    if (existingApplications.length === 0) {
      // If the list is empty, create a new application object
      const newApplication = {competition: competitionId};
      // Send a POST request to create a new application
      const createApplicationResponse = await fetch('http://20.108.53.69/api/applications/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(newApplication),
      });

      const createdApplicationData = await createApplicationResponse.json();
      const createdApplicationId = createdApplicationData.id;
      // Add the applicationId to the formData
      formData.application = createdApplicationId;
    } else {
      // If the list is not empty, use the first applicationId from the list\
      const existingApplicationId = existingApplications[0].id;
      console.log(existingApplicationId)
      // Add the existing applicationId to the formData
      console.log(formData)
      formData.application = existingApplicationId;
      console.log(formData)
    }

    // Step 3: Now you can send the extended formData to another endpoint or perform any other actions
    console.log('Extended formData:', formData);

    // Example: Send the extended formData to another API endpoint
    const submitResponse = await fetch('http://20.108.53.69/api/participants/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    });

    const submitResult = await submitResponse.json();
    console.log('Submit result:', submitResult);
    return submitResult;
  } catch (error) {
    console.error('Error submitting form:', error);
  }
}

export async function deleteParticipantAndCheckApplication(participant_id) {
  try {
    // Step 1: Try to fetch existing applications for the given participant_id
    await refreshAccessToken();
    const token = sessionStorage.getItem('access');

    // Fetch the participant data to get the associated application
    const participantResponse = await fetch(`http://20.108.53.69/api/participants/${participant_id}/`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      }
    });

    const participantData = await participantResponse.json();

    // Get the associated application ID from the participant data
    const applicationId = participantData.application;

    // Step 2: Check if there are any participants left for the associated application
    const participantsResponse = await fetch(`http://20.108.53.69/api/participants/?application=${applicationId}`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      }
    });

    const remainingParticipants = await participantsResponse.json();
    console.log(remainingParticipants)
    if (remainingParticipants.length === 1) {
      // If there is only one participant left (the one being deleted), delete the application
      await fetch(`http://20.108.53.69/api/applications/${applicationId}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
    } else {

      // Step 3: Delete the participant
      await fetch(`http://20.108.53.69/api/participants/${participant_id}/`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
      });
    }
  } catch (error) {
    console.error('Error deleting participant:', error);
  }
}

export const deleteApplication = async (applicationId) => {
  try {
    await refreshAccessToken();
    const token = sessionStorage.getItem('access');
    await fetch(`http://20.108.53.69/api/applications/${applicationId}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    })
  } catch (error) {
    console.error('Error deleting application:', error)
  }
}