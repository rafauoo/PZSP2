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

  const handleDeleteParticipant = (participantId) => {
    const confirmation = window.confirm(`Czy na pewno chcesz usunąć tego uczestnika?`);

    if (confirmation) {
      handleDeleteResource(participantId, 'participants', sessionStorage.getItem('access'), setParticipantsData);
    }
  };

  const handleDeleteApplication = (applicationId) => {
    const confirmation = window.confirm(`Czy na pewno chcesz usunąć to zgłoszenie?`);

    if (confirmation) {
      handleDeleteResource(applicationId, 'applications', sessionStorage.getItem('access'), setApplicationsData);
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
