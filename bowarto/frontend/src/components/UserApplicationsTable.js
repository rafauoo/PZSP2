// UserApplicationsTable.js
import React, {useState} from 'react';
import Table from 'react-bootstrap/Table';
import ApplicationRow from './ApplicationRow';
import {deleteParticipantAndCheckApplication} from "../requests/user_panel";

function UserApplicationsTable({
                                 applications,
                                 onDeleteParticipant,
                                 onAddParticipant
                               }) {
  const [expandedApplication, setExpandedApplication] = useState(null);

  const handleToggleExpand = (applicationId) => {
    setExpandedApplication((prevExpanded) => (prevExpanded === applicationId ? null : applicationId));
  };


  // Remove the participant with the specified participantId from applicationData
  // const updatedApplications = applicationsData.participants.filter(participant => participant.id !== participantId);

  // Update applicationData with the new participants array
  //   setApplicationsData({...updatedApplications});
  //   // Call the function to delete the participant and check the application
  //   await deleteParticipantAndCheckApplication(participantId);
  // } catch
  //   (error) {
  //   console.error("Error removing participant:", error);


  const handleDeleteApplicationInTable = async (applicationId) => {

  };


  return (
    <div className="user-applications-table">

      <Table striped bordered hover>
        <thead>
        <tr>
          <th>Konkurs</th>
          <th>Utworzenie aplikacji</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        {applications.map((application) => (
          <ApplicationRow
            application={application}
            expanded={expandedApplication === application.id}
            onToggleExpand={handleToggleExpand}
            onDeleteApplication={handleDeleteApplicationInTable}
            onDeleteParticipant={onDeleteParticipant}
            onAddParticipant={onAddParticipant}
          />
        ))}
        </tbody>
      </Table>
    </div>
  );
}

export default UserApplicationsTable;
