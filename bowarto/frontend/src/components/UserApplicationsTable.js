// UserApplicationsTable.js
import React, {useState} from 'react';
import Table from 'react-bootstrap/Table';
import ApplicationRow from './ApplicationRow';

function UserApplicationsTable({
                                 userApplications,
                                 competitionNames,
                                 participantsData,
                                 loading,
                                 onDeleteParticipant,
                                 onDeleteApplication,
                                 onAddParticipant,
                               }) {
  const [expandedApplication, setExpandedApplication] = useState(null);

  const handleToggleExpand = (applicationId) => {
    setExpandedApplication((prevExpanded) => (prevExpanded === applicationId ? null : applicationId));
  };

  const handleDeleteParticipantInTable = (participantId) => {
    onDeleteParticipant(participantId);
  };

  const handleDeleteApplicationInTable = async (applicationId) => {
    onDeleteApplication(applicationId);
  };

  const handleAddParticipantInTable = (applicationId, newParticipant) => {
    onAddParticipant(applicationId, newParticipant);
  };

  return (
    <div className="user-applications-table">
      {loading ? (
        <p>Loading...</p>
      ) : (
        <Table striped bordered hover>
          <thead>
          <tr>
            <th>Konkurs</th>
            <th>Utworzenie aplikacji</th>
            <th></th>
          </tr>
          </thead>
          <tbody>
          {userApplications.map((application) => (
            <ApplicationRow
              key={application.id}
              application={application}
              competitionName={competitionNames[application.competition]}
              expanded={expandedApplication === application.id}
              participantsData={participantsData}
              onToggleExpand={handleToggleExpand}
              onDeleteApplication={handleDeleteApplicationInTable}
              onDeleteParticipantInTable={handleDeleteParticipantInTable}
              onAddParticipant={handleAddParticipantInTable}
            />
          ))}
          </tbody>
        </Table>
      )}
    </div>
  );
}

export default UserApplicationsTable;
