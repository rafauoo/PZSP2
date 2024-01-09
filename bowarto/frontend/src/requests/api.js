import refreshAccessToken from "./refresh";

export const fetchData = async (url, options) => {
  const response = await fetch(url, options);

  if (!response.ok) {
    throw new Error(`HTTP error! Status: ${response.status}`);
  }

  try {
    // Sprawdź, czy odpowiedź zawiera ciało (nie jest typu No Content)
    if (response.status !== 204) {
      return await response.json();
    } else {
      // Jeśli odpowiedź jest typu No Content, zwróć pusty obiekt
      return {};
    }
  } catch (error) {
    console.error('Error parsing JSON:', error);
    throw new Error('Error parsing JSON');
  }
};

export const fetchResourceData = async (resourceIds, token, resourceType, mapKey) => {
  const url = `http://20.108.53.69/api/${resourceType}/`;
  const options = {method: 'GET', headers: {'Authorization': `Bearer ${token}`}};
  const resourceData = await fetchData(url, options);

  return resourceIds.reduce((acc, resourceId) => {
    const resource = resourceData.find(item => item.id === resourceId);
    acc[resourceId] = resource ? resource[mapKey] : null;
    return acc;
  }, {});
};

export const fetchParticipantsData = async (applications, token) => {
  const url = 'http://20.108.53.69/api/participants/';
  const options = {method: 'GET', headers: {'Authorization': `Bearer ${token}`}};
  const participantsData = await fetchData(url, options);

  return applications.reduce((acc, application) => {
    const participantsForApplication = participantsData.filter(participant => participant.application === application.id);
    acc[application.id] = participantsForApplication;
    return acc;
  }, {});
};

export const handleDeleteResource = async (resourceId, resourceType, setResourceData) => {
  try {
    await refreshAccessToken();
    const token = sessionStorage.getItem('access');
    const url = `http://20.108.53.69/api/${resourceType}/${resourceId}/`;
    const options = {method: 'DELETE', headers: {'Authorization': `Bearer ${token}`}};
    const response = await fetchData(url, options);

    console.log(response);

    // if (!response.ok) {
    //   throw new Error(`HTTP error! Status: ${response.status}`);
    // }

    // Uaktualnij stan usuwając zasób z danych lokalnych
    setResourceData((prevData) => {
      console.log(prevData);
      const updatedData = {...prevData};

      // Usuń zasób z lokalnych danych
      updatedData[resourceType] = updatedData[resourceType].filter(item => item.id !== resourceId);

      console.log(`Deleted ${resourceType} with id ${resourceId}`);
      console.log('Updated Data:', updatedData);

      return updatedData;
    });
  } catch (error) {
    console.error(`Error deleting ${resourceType}:`, error);
  }
};


export const handleAddParticipant = async (applicationId, newParticipant, participantsData, setParticipantsData) => {
  try {
    await refreshAccessToken();
    const token = sessionStorage.getItem('access');

    const response = await fetch(`http://20.108.53.69/api/participants/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        application: applicationId,
        ...newParticipant
      })
    });

    if (!response.ok) {
      console.log(applicationId);
      console.log(JSON.stringify({
        application: applicationId,
        ...newParticipant
      }));
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    // Poczekaj, aż dane JSON zostaną pobrane
    const newParticipantData = await response.json();

    // Użyj callbacka do aktualizacji stanu
    setParticipantsData((prevParticipantsData) => {
      const updatedParticipantsData = {...prevParticipantsData};
      updatedParticipantsData[applicationId] = [...(updatedParticipantsData[applicationId] || []), newParticipantData];
      return updatedParticipantsData;
    });
  } catch (error) {
    console.error('Error adding participant:', error);
  }
};

