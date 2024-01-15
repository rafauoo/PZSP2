import { centeredHeader } from "../../../styles/styles"
import { centeredCellStyle } from "../../../styles/styles";
import { Table } from "reactstrap";
import CompetitionRow from "./CompetitionRow";
import UserApplicationsTable from "../../../components/UserApplicationsTable"
import { useState } from "react";

const SingleCompetitionTable = ({ competitions, header }) => {
  // const handleShowUserApplicationsTable = () => { };
  const [selectedCompetitionId, setSelectedCompetitionId] = useState(null);

  const handleToggleUserApplicationsTable = (competitionId) => {
    setSelectedCompetitionId((prevId) => (prevId === competitionId ? null : competitionId));
  };
  return (
    <>
      <h1 style={centeredHeader}>{header}</h1>
      <Table striped bordered={false} hover>
        <thead>
          <tr>
            <th style={centeredCellStyle}>Data rozpoczęcia konkursu</th>
            <th style={centeredCellStyle}>Data zakończenia konkursu</th>
            <th style={centeredCellStyle}></th>
          </tr>
        </thead>
        <tbody>
          {competitions.map((competition) => (
            <>
              <CompetitionRow competition={competition} showUserApplicationsTable={() => handleToggleUserApplicationsTable(competition.id)} />
              {selectedCompetitionId === competition.id && (
                <UserApplicationsTable applications={competition.applications} />
              )}
            </>
          ))}
        </tbody>
      </Table>
      <hr></hr>

    </>
  )
}
export default SingleCompetitionTable;
