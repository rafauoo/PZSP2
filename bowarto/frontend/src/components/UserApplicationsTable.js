// UserApplicationsTable.js
import React, {useState} from 'react';
import Table from 'react-bootstrap/Table';
import ApplicationRow from './ApplicationRow';

function UserApplicationsTable({
                                 applications,
                                 onAddParticipant,
                                 onDeleteParticipant,
                                 onEditParticipant,
                                 onDeleteApplication,
                               }) {
  const [expandedApplication, setExpandedApplication] = useState(null);

  const handleToggleExpand = (applicationId) => {
    setExpandedApplication((prevExpanded) => (prevExpanded === applicationId ? null : applicationId));
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
            onDeleteApplication={onDeleteApplication}
            onDeleteParticipant={onDeleteParticipant}
            onAddParticipant={onAddParticipant}
            onEditParticipant={onEditParticipant}
          />
        ))}
        </tbody>
      </Table>
    </div>
  );
}

export default UserApplicationsTable;
