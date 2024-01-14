import React from "react";
import ParticipantsTable from "./ParticipantsTable";
import Table from "react-bootstrap/Table";
import ParticipantsList from "../../../components/ParticipantsList";
import ApplicationRow from "../../../components/ApplicationRow";

const ApplicationsTable = ({applications}) => {
  return (
    <Table striped bordered hover>
      <tbody>
      {applications.map((application) => (
        <ApplicationRow application={application}/>
      ))};
      </tbody>
    </Table>
  )
}

export default ApplicationsTable;