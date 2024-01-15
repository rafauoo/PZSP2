import { useEffect, useState } from "react";
import { centeredCellStyle } from "../../../styles/styles";
import formatDate from "../../../utils/format";
import { buttonStyleEdit } from "../../../styles/styles";
import EditCompetitionModal from "./EditCompetitionModal";

const CompetitionRow = ({ competition, showUserApplicationsTable }) => {

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
        <td style={centeredCellStyle}>
          <button
            style={buttonStyleEdit}
            onClick={handleModal}
          >
            Edytuj
          </button>
        </td>
      </tr>
      <EditCompetitionModal show={showEditCompetitionModal} handleClose={handleModal} competition={competition} />
    </>
  )
}

export default CompetitionRow;
