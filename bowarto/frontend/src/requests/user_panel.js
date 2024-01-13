import refreshAccessToken from "./refresh";
import {editParticipant} from "../api/requests/participant";

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
    console.log(existingApplications)
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
      console.log(createdApplicationData)
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


export async function updateParticipant(participantId, formData) {
  try {
    // Pobierz token dostępu
    await refreshAccessToken();
    const token = sessionStorage.getItem('access');

    // Utwórz adres URL do aktualizacji uczestnika
    const apiUrl = `http://20.108.53.69/api/participants/${participantId}/`;

    // Wyślij żądanie PATCH do aktualizacji uczestnika
    const response = await fetch(apiUrl, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    });

    // Pobierz dane odpowiedzi
    const result = await response.json();

    // Wyświetl wynik w konsoli (możesz dostosować to do swoich potrzeb)
    console.log('Update result:', result);

    return result;
  } catch (error) {
    console.error('Error updating participant:', error);
  }
}

export async function uploadAttachment(participantId, newAttachment) {
  try {

    const formData = new FormData();
    formData.append('attachment', JSON.stringify({'path': newAttachment}));
    console.log(formData)

    // Utwórz adres URL do wysłania załącznika

    // Wyślij żądanie POST do wysłania załącznika
    const response = await editParticipant(participantId, newAttachment)

    // Sprawdź, czy status odpowiedzi jest w zakresie 200-299
    if (!response.ok) {
      throw new Error(`Upload failed with status ${response.status}`);
    }

    // Pobierz dane odpowiedzi
    const result = await response.json();

    // Wyświetl wynik w konsoli (możesz dostosować to do swoich potrzeb)
    console.log('Upload result:', result);

    return result;
  } catch (error) {
    console.error('Error uploading attachment:', error);
    throw error;
  }
}


export const downloadFile = async (attachmentId) => {
  try {
    await refreshAccessToken();
    const token = sessionStorage.getItem('access');

    // Pobierz plik z serwera
    const response = await fetch(`http://20.108.53.69/api/files/${attachmentId}/`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
      },
      responseType: 'arraybuffer', // Set responseType here
    });

    const contentDisposition = response.headers.get('content-disposition');
    const filename = parseFilenameFromContentDisposition(contentDisposition);

    // Access response data using arrayBuffer() method
    const responseData = await response.arrayBuffer();

    // Save file with correct data
    saveFile(responseData, filename);
  } catch (error) {
    console.error('Error downloading file:', error);
    throw error;
  }
}

const parseFilenameFromContentDisposition = (contentDisposition) => {
  const match = /filename\*=utf-8''(.+)/.exec(contentDisposition);
  return match ? decodeURIComponent(match[1]) : 'downloaded_file';
};

const saveFile = (data, filename) => {
  const blob = new Blob([data], {type: 'application/octet-stream'});
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

export const deleteFile = async (attachmentId) => {
  try {
    await refreshAccessToken();
    const token = sessionStorage.getItem('access');

    // Usuń plik z serwera
    const response = await fetch(`http://20.108.53.69/api/files/${attachmentId}/`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error('Error deleting file');
    }

    console.log('File deleted successfully');
    // Implementuj dodatkową logikę po poprawnym usunięciu pliku
  } catch (error) {
    console.error('Error deleting file:', error);
    throw error;
  }
};

