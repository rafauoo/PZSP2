import React from "react";
import ApplicationsTable from "./ApplicationsTable";
import Table from "react-bootstrap/Table";
import ApplicationRow from "../../../components/ApplicationRow";
import UserApplicationsTable from "../../../components/UserApplicationsTable";

const competitionsTable = ({competitions}) => {
  return (
    <>
      <h1>Zgłoszenia</h1>
      {competitions.map((competition) => (
        <UserApplicationsTable applications={competition.applications}/>
      ))}
    </>
  )
}

export default competitionsTable;