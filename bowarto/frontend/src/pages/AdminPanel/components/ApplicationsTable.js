// UserApplicationsTable.js
import React, {useState, useEffect} from 'react';
import Table from 'react-bootstrap/Table';
import formatDate from "../../../utils/format";
import AddParticipantModal from "../../../components/AddParticipantModal";
import ParticipantsList from './ParticipantsList';
import refreshAccessToken from '../../../requests/refresh';
import {
  deleteParticipantAndCheckApplication,
  submitForm
} from "../../../requests/user_panel";
import { getUserByID } from '../../../api/requests/user';
import { buttonContainerStyle, buttonContainerStyleParticipants, buttonStyleBasic, buttonStyleDelete, buttonStyleEdit, buttonStyledShow, buttonStyledShow1, iconButtonStyle } from "../../../styles/styles";


function ApplicationRow({
  application,
  expanded,
  onToggleExpand,
  onDeleteApplication,
  onDeleteParticipant,
  onAddParticipant,
  onEditParticipant,
  onAddAttachment,
  onDownloadFile,
  onRemoveFile
}) {
  const [showAddParticipantModal, setShowAddParticipantModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [userData, setUserData] = useState(null)

  const handleShowAddParticipantModal = () => {
    setShowAddParticipantModal(true);

  };

  const handleCloseAddParticipantModal = () => {
    setShowAddParticipantModal(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      await refreshAccessToken()
      const user = await getUserByID(application.user);
      setUserData(user);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };
  return (
    <>
      <tr>
        <td>
          <h2>{userData ? userData.email : null}</h2>
        </td>
        <td style={buttonContainerStyleParticipants}>
          <button style={buttonStyledShow1}
            onClick={() => onToggleExpand(application.id)}>
            <img src={require('../../../images/view-white.png')} alt="Widok" style={iconButtonStyle} />
            {expanded ? 'Ukryj' : 'Wyświetl'}
          </button>
          <button style={buttonStyleDelete}
            onClick={() => onDeleteApplication(application.id)}>
            <img src={require('../../../images/delete.png')} alt="Usuń" style={iconButtonStyle} />
            Usuń aplikację
          </button>
        </td>
      </tr>
      {expanded && (
        <tr>
          <td colSpan="3">
          <ParticipantsList
              participants={application.participants || []}
              onDeleteParticipant={onDeleteParticipant}
              onEditParticipant={onEditParticipant}
              onAddAttachment={onAddAttachment}
              onDownloadFile={onDownloadFile}
              onRemoveFile={onRemoveFile}
            />
          </td>
        </tr>
      )}
      <AddParticipantModal
        competitionId={application.competition.id}
        show={showAddParticipantModal}
        handleClose={handleCloseAddParticipantModal}
        onAddParticipant={onAddParticipant}
      />
    </>
  );
}


function ApplicationsTable({
                                 applications,
                                 onAddParticipant,
                                 onDeleteParticipant,
                                 onEditParticipant,
                                 onDeleteApplication,
                                 onAddAttachment,
                                 onDownloadFile,
                                 onRemoveFile
                               }) {
  const [expandedApplication, setExpandedApplication] = useState(null);

  const handleToggleExpand = (applicationId) => {
    setExpandedApplication((prevExpanded) => (prevExpanded === applicationId ? null : applicationId));
  };


  return (
    <div className="user-applications-table">

      <Table striped bordered hover>
        {/*<thead>*/}
        {/*<tr>*/}
        {/*  <th>Konkurs</th>*/}
        {/*  <th></th>*/}
        {/*  <th></th>*/}
        {/*</tr>*/}
        {/*</thead>*/}
        <tbody>
        {applications.map((application) => (
          <ApplicationRow
            application={application}
            expanded={expandedApplication === application.id}
            onToggleExpand={handleToggleExpand}
            onDeleteApplication={onDeleteApplication}
            onDeleteParticipant={onDeleteParticipant}
            onAddParticipant={onAddParticipant}
            onEditParticipant={onEditParticipant}
            onAddAttachment={onAddAttachment}
            onDownloadFile={onDownloadFile}
            onRemoveFile={onRemoveFile}
          />
        ))}
        </tbody>
      </Table>
    </div>
  );
}

export default ApplicationsTable;
