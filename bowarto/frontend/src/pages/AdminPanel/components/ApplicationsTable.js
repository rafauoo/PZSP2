import React from "react";
import ParticipantsTable from "./ParticipantsTable";
import Table from "react-bootstrap/Table";
import ParticipantsList from "../../../components/ParticipantsList";
import ApplicationRow from "../../../components/ApplicationRow";
import { innerTable } from "../../../styles/styles";

const ApplicationsTable = ({ applications }) => {
  return (
    <table style={innerTable}>
      <tbody>
        {applications.map((application) => (
          <ApplicationRow application={application} />
        ))}
      </tbody>
    </table>
  )
}

export default ApplicationsTable;
