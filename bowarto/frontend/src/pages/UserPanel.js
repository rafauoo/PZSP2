// UserPanel.js
import React, {useState, useEffect} from 'react';
import refreshAccessToken from '../requests/refresh';
import UserPanelHeader from '../components/UserPanelHeader';
import UserApplicationsTable from '../components/UserApplicationsTable';
import {
  fetchData,
  fetchResourceData,
  fetchParticipantsData,
  handleDeleteResource,
  handleAddParticipant
} from '../requests/api';

function UserPanel() {
  const [applicationsData, setApplicationsData] = useState([]);
  const [competitionNames, setCompetitionNames] = useState({});
  const [participantsData, setParticipantsData] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDataAndPopulateState = async () => {
      try {
        await refreshAccessToken();
        const token = sessionStorage.getItem('access');
        const userApplicationsUrl = 'http://20.108.53.69/api/applications/';
        const userApplicationsOptions = {method: 'GET', headers: {'Authorization': `Bearer ${token}`}};
        const userData = await fetchData(userApplicationsUrl, userApplicationsOptions);

        const competitionIds = userData.map(application => application.competition);
        const competitionData = await fetchResourceData(competitionIds, token, 'competitions', 'title');
        const participantsData = await fetchParticipantsData(userData, token);

        setApplicationsData(userData);
        setCompetitionNames(competitionData);
        setParticipantsData(participantsData);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setLoading(false);
      }
    };

    fetchDataAndPopulateState();
  }, []);

  const handleDeleteParticipant = async (participantId) => {
    try {
      const confirmation = window.confirm(`Czy na pewno chcesz usunąć tego uczestnika?`);

      if (confirmation) {
        // Wywołaj zapytanie do API w celu usunięcia uczestnika
        const token = sessionStorage.getItem('access');
        const deleteParticipantUrl = `http://20.108.53.69/api/participants/${participantId}/`;
        const deleteParticipantOptions = {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        };

        await fetch(deleteParticipantUrl, deleteParticipantOptions);

        // Uaktualnij participantsData lokalnie po usunięciu uczestnika
        setParticipantsData(prevParticipantsData => {
          const updatedParticipantsData = {...prevParticipantsData};

          for (const applicationId in updatedParticipantsData) {
            if (Object.prototype.hasOwnProperty.call(updatedParticipantsData, applicationId)) {
              updatedParticipantsData[applicationId] = updatedParticipantsData[applicationId].filter(participant => participant.id !== participantId);
            }
          }

          return updatedParticipantsData;
        });
      }
    } catch (error) {
      console.error('Error deleting participant:', error);
    }
  };

  const handleDeleteApplication = async (applicationId) => {
    const confirmation = window.confirm(`Czy na pewno chcesz usunąć to zgłoszenie?`);

    if (confirmation) {
      await handleDeleteResource(applicationId, 'applications', setApplicationsData);
    }
  };

  const handleAddParticipantWrapper = async (applicationId, newParticipant) => {
    await handleAddParticipant(applicationId, newParticipant, participantsData, setParticipantsData);
  };

  return (
    <div className="user-panel">
      <UserPanelHeader/>
      <UserApplicationsTable
        userApplications={applicationsData}
        competitionNames={competitionNames}
        participantsData={participantsData}
        loading={loading}
        onDeleteParticipant={handleDeleteParticipant}
        onDeleteApplication={handleDeleteApplication}
        onAddParticipant={handleAddParticipantWrapper}
      />
    </div>
  );
}

export default UserPanel;
