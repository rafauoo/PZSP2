import { centeredHeader } from "../../../styles/styles";
import { centeredCellStyle } from "../../../styles/styles";
import { Table } from "reactstrap";
import CompetitionRow from "./CompetitionRow";
import ApplicationsTable from "./ApplicationsTable";
import MessageModal from "../../../components/MessageModal";
import { useState, useEffect } from "react";
import React from 'react';
import refreshAccessToken from '../../../requests/refresh';
import {getApplicationList} from "../../../api/requests/application";
import {
  handleAddAttachmentLogic,
  handleAddParticipantLogic,
  handleDeleteApplicationLogic,
  handleDeleteParticipantLogic,
  handleDownloadFileLogic,
  handleEditParticipantLogic,
  handleRemoveFileLogic
} from "../../UserPanel/UserPanelHelpers";

const LOADING_MESSAGE = "Trwa ładowanie...";
const DELETE_PARTICIPANT_CONFIRMATION = 'Czy na pewno chcesz usunąć tego uczestnika?';
const DELETE_APPLICATION_CONFIRMATION = 'Czy na pewno chcesz usunąć to zgłoszenie?';
const DELETE_FILE_CONFIRMATION = 'Czy na pewno chcesz usunąć ten załącznik?';

const SingleCompetitionTable = ({ competitions, header }) => {
  const [selectedCompetitionId, setSelectedCompetitionId] = useState(null);

  const handleToggleUserApplicationsTable = (competitionId) => {
    setSelectedCompetitionId((prevId) => (prevId === competitionId ? null : competitionId));
  };
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

  const handleRemoveFile = async (fileId) => {
    const isConfirmed = window.confirm(DELETE_FILE_CONFIRMATION);
    if (!isConfirmed) {
      return;
    }
    const {
      updatedApplications, showMessageModal, messageText
    } = await handleRemoveFileLogic(fileId, applicationsData);

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

  return (
    <>
      <h1 style={centeredHeader}>{header}</h1>
      <Table striped bordered={false} hover>
        <thead>
          <tr>
            <th style={centeredCellStyle}>Nazwa</th>
            <th style={centeredCellStyle}>Data rozpoczęcia konkursu</th>
            <th style={centeredCellStyle}>Data zakończenia konkursu</th>
            <th style={centeredCellStyle}></th>
          </tr>
        </thead>
        <tbody>
          {competitions.map((competition) => (
            <React.Fragment key={competition.id}>
              <CompetitionRow competition={competition} showUserApplicationsTable={() => handleToggleUserApplicationsTable(competition.id)} />
              {selectedCompetitionId === competition.id && (
                <tr>
                  <td colSpan="4">
                  {loading ? (
                    <p>{LOADING_MESSAGE}</p>) : (<>
                    {applicationsData !== 0 ? (<>
                      <ApplicationsTable
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
                      <p>Brak zgłoszeń</p>
                    </>)}
                  </>)}
                  </td>
                </tr>
              )}
            </React.Fragment>
          ))}
        </tbody>
      </Table>
      <hr />
      <MessageModal
      show={showMessageModal}
      onClose={() => {
        setShowMessageModal(false);
        setMessageText('');
      }}
      message={messageText}
      />
    </>
  );
};


export default SingleCompetitionTable;