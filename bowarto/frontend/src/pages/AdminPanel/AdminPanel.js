import React, {useEffect, useState} from "react";
import MessageModal from "../../components/MessageModal";
import {getApplicationList} from "../../api/requests/application";
import CompetitionsTable from "./components/CompetitionsTable";
import {getUserByID} from "../../api/requests/user";
import refreshAccessToken from "../../requests/refresh";

const LOADING_MESSAGE = "Trwa ładowanie...";

const AdminPanel = () => {
  const [showMessageModal, setShowMessageModal] = useState(false);
  const [messageText, setMessageText] = useState('');

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([])

  useEffect(() => {
    fetchData()
  }, []);


  const fetchData = async () => {
    try {
      await refreshAccessToken();
      const applications = await getApplicationList();
      console.log(applications);
      const uniqueCompetitionIds = new Set();

      const uniqueCompetitions = applications.reduce((acc, application) => {
        const competition = application.competition;
        const competitionId = competition.id;

        if (!uniqueCompetitionIds.has(competitionId)) {
          uniqueCompetitionIds.add(competitionId);
          acc.push({...competition, applications: []});
        }

        return acc;
      }, []);

      // Dodaj aplikacje do odpowiednich konkursów
      for (const application of applications) {
        const competitionId = application.competition.id;
        const competitionIndex = uniqueCompetitions.findIndex(
          (comp) => comp.id === competitionId
        );

        if (competitionIndex !== -1) {
          // Pobierz dane użytkownika za pomocą funkcji getUserById
          const user = await getUserByID(application.user);

          // Sprawdź, czy applications jest zdefiniowane, jeśli nie, zainicjuj jako pustą tablicę
          if (!uniqueCompetitions[competitionIndex].applications) {
            uniqueCompetitions[competitionIndex].applications = [];
          }

          uniqueCompetitions[competitionIndex].applications.push({
            id: application.id,
            user: user,
            participants: application.participants,
            competition: application.competition
          });
        }
      }

      // console.log(uniqueCompetitions);
      setData(uniqueCompetitions);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setLoading(false);
    }
  };


  return (
    <div>
      {loading ? (
        <p>{LOADING_MESSAGE}</p>
      ) : (
        <>
          {data.length !== 0 ? (
            <CompetitionsTable competitions={data}/>
          ) : (
            <>
              <p>Nie posiadasz obecnie żadnych zgłoszeń.</p>
            </>
          )}
        </>
      )}

      <MessageModal
        show={showMessageModal}
        onClose={() => {
          setShowMessageModal(false);
          setMessageText('');
        }}
        message={messageText}
      />
    </div>
  );
}

export default AdminPanel;