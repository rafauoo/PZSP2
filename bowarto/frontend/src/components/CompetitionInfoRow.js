import { Table } from "react-bootstrap";
import { getApplicationListByCompetitionID } from "../api/requests/application";
import refreshAccessToken from "../requests/refresh";
import { useEffect, useState } from "react";

export default function CompetitionInfoRow({ competition }) {

  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      await refreshAccessToken();
      const applicationsData = await getApplicationListByCompetitionID(competition.id);
      console.log(applicationsData)
      setApplications(applicationsData)
      setLoading(false);
    } catch (error) {
      console.error(error)
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      {loading ? (<p> LOADING</p>) : (
        <Table striped bordered={false} hover>
          <thead>
            <tr>
              <th>
                <h3>Participants</h3>
              </th>
            </tr>
          </thead>
          <tbody>
            {applications.map((application) =>
              application.participants.map((participant) => (
                <tr key={participant.id}>
                  <td>
                    {participant.name}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </Table>
      )
      }
    </>
  );
}
