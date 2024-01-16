import { useEffect, useState } from "react";
import { centeredCellStyle, headerShowStyle, buttonStyledShow } from "../../../styles/styles";
import formatDate from "../../../utils/format";
import { buttonStyleEdit } from "../../../styles/styles";
import EditCompetitionModal from "./EditCompetitionModal";

const CompetitionRow = ({ competition, showUserApplicationsTable }) => {
  const [expanded, setExpanded] = useState(false)
  const [showEditCompetitionModal, setShowCompetitionModal] = useState(false);
  const handleModal = () => {
    showEditCompetitionModal ? setShowCompetitionModal(false) : setShowCompetitionModal(true);
  };


  return (
    <>
      <tr key={competition.id} onClick={showUserApplicationsTable} style={{ cursor: 'pointer' }}>
        <td>
          <h4>{competition.title}</h4>
          <p>{competition.description}</p>
        </td>
        <td style={centeredCellStyle}>
          {formatDate(competition.start_at)}
        </td>
        <td style={centeredCellStyle}>
          {formatDate(competition.end_at)}
        </td>
        <th colSpan="3" style={headerShowStyle}>
          <button style={buttonStyledShow}
                  onClick={() => setExpanded(!expanded)}>{expanded ? "Ukryj" : "Pokaż"}</button>
        </th>
      </tr>
      <EditCompetitionModal show={showEditCompetitionModal} handleClose={handleModal} competition={competition} />
    </>
  )
}

export default CompetitionRow;
