import React, {useEffect, useState} from 'react';
import refreshAccessToken from '../../requests/refresh';
import {getApplicationList} from "../../api/requests/application";
import MessageModal from "../../components/MessageModal";
import UserPanelHeader from '../../components/UserPanelHeader';
import UserApplicationsTable from '../../components/UserApplicationsTable';
import {
  handleAddAttachmentLogic,
  handleAddParticipantLogic,
  handleDeleteApplicationLogic,
  handleDeleteParticipantLogic,
  handleDownloadFileLogic,
  handleEditParticipantLogic,
  handleRemoveFileLogic
} from "./UserPanelHelpers";

const LOADING_MESSAGE = "Trwa ładowanie...";
const DELETE_PARTICIPANT_CONFIRMATION = 'Czy na pewno chcesz usunąć tego uczestnika?';
const DELETE_APPLICATION_CONFIRMATION = 'Czy na pewno chcesz usunąć to zgłoszenie?';
const DELETE_FILE_CONFIRMATION = 'Czy na pewno chcesz usunąć ten załącznik?';

function UserPanel() {
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [messageText, setMessageText] = useState('');

  const [applicationsData, setApplicationsData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      await refreshAccessToken()
      const applications = await getApplicationList();
      setApplicationsData(applications);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };
  const confirmAction = (message) => window.confirm(message);

  const handleDeleteParticipant = async (participantId) => {
    const isConfirmed = confirmAction(DELETE_PARTICIPANT_CONFIRMATION);
    if (!isConfirmed) {
      return;
    }

    const {
      updatedApplications, showMessageModal, messageText
    } = await handleDeleteParticipantLogic(participantId, applicationsData);

    setApplicationsData(updatedApplications);
    setShowMessageModal(showMessageModal);
    setMessageText(messageText);
  };

  const handleDeleteApplication = async (applicationId) => {
    const isConfirmed = window.confirm(DELETE_APPLICATION_CONFIRMATION);
    if (!isConfirmed) {
      return;
    }

    const {
      updatedApplications, showMessageModal, messageText
    } = await handleDeleteApplicationLogic(applicationId, applicationsData);

    setApplicationsData(updatedApplications);
    setShowMessageModal(showMessageModal);
    setMessageText(messageText);
  };

  const handleAddParticipant = async (competitionId, newParticipant) => {
    const {
      updatedApplications, showMessageModal, messageText
    } = await handleAddParticipantLogic(competitionId, newParticipant, applicationsData);

    setApplicationsData(updatedApplications);
    setShowMessageModal(showMessageModal);
    setMessageText(messageText);
  };

  const handleEditParticipant = async (participantId, editedData) => {
    const {
      updatedApplications, showMessageModal, messageText
    } = await handleEditParticipantLogic(participantId, editedData, applicationsData);

    setApplicationsData(updatedApplications);
    setShowMessageModal(showMessageModal);
    setMessageText(messageText);
  };

  const handleAddAttachment = async (participantId, newAttachment) => {
    const {
      updatedApplications, showMessageModal, messageText
    } = await handleAddAttachmentLogic(participantId, newAttachment, applicationsData);

    setApplicationsData(updatedApplications);
    setShowMessageModal(showMessageModal);
    setMessageText(messageText);
  };

  const handleRemoveFile = async (attachmentId) => {
    const isConfirmed = window.confirm(DELETE_FILE_CONFIRMATION);
    if (!isConfirmed) {
      return;
    }
    const {
      updatedApplications, showMessageModal, messageText
    } = await handleRemoveFileLogic(attachmentId, applicationsData);

    setApplicationsData(updatedApplications);
    setShowMessageModal(showMessageModal);
    setMessageText(messageText);
  };

  const handleDownloadFile = async (attachmentId) => {
    const {
      showMessageModal, messageText
    } = await handleDownloadFileLogic(attachmentId);

    setShowMessageModal(showMessageModal);
    setMessageText(messageText);
  };

  return (<div className="user-panel">
    {loading ? (
      <p>{LOADING_MESSAGE}</p>) : (<>
      {applicationsData.length !== 0 ? (<>
        <UserPanelHeader/>
        <UserApplicationsTable
          applications={applicationsData}
          onDeleteParticipant={handleDeleteParticipant}
          onDeleteApplication={handleDeleteApplication}
          onAddParticipant={handleAddParticipant}
          onEditParticipant={handleEditParticipant}
          onAddAttachment={handleAddAttachment}
          onDownloadFile={handleDownloadFile}
          onRemoveFile={handleRemoveFile}
        />
      </>) : (<>
        <p>Nie posiadasz obecnie żadnych zgłoszeń.</p>
      </>)}
    </>)}

    <MessageModal
      show={showMessageModal}
      onClose={() => {
        setShowMessageModal(false);
        setMessageText('');
      }}
      message={messageText}
    />
  </div>);
}

export default UserPanel;
