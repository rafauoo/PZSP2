// UserPanel.js
import React, {useState, useEffect} from 'react';
import refreshAccessToken from '../requests/refresh';
import UserPanelHeader from '../components/UserPanelHeader';
import UserApplicationsTable from '../components/UserApplicationsTable';
import {Link} from "react-router-dom";
import {
  deleteApplication,
  deleteParticipantAndCheckApplication,
  fetchDataFromApi,
  submitForm, updateParticipant, uploadAttachment
} from "../requests/user_panel";

const buttonStyle = {
  backgroundColor: 'rgb(131, 203, 83)',
  borderRadius: '5px',
  color: 'black',
  padding: '5px 10px',
  border: 'none',
  cursor: 'pointer',
};


function UserPanel() {
  const [applicationsData, setApplicationsData] = useState([]);
  const [showAddParticipantModal, setShowAddParticipantModal] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const applications = await fetchDataFromApi('http://20.108.53.69/api/applications/');
        const participants = await fetchDataFromApi('http://20.108.53.69/api/participants/');
        const competitions = await fetchDataFromApi('http://20.108.53.69/api/competitions/');
        const files = await fetchDataFromApi('http://20.108.53.69/api/files/');

        // Przyporządkuj uczestników do odpowiednich aplikacji
        const applicationsWithParticipants = applications.map(application => {
          const applicationParticipants = participants.filter(participant => participant.application === application.id);
          return {...application, participants: applicationParticipants};
        });

        // Przyporządkuj pliki do odpowiednich uczestników
        const applicationsWithParticipantsAndFiles = applicationsWithParticipants.map(application => {
          const applicationParticipantsWithFiles = application.participants.map(participant => {
            const participantFiles = files.filter(file => file.participant === participant.id);
            // Jeśli uczestnik ma przypisany plik, zwróć jego id, w przeciwnym razie null
            const participantFile = participantFiles.length > 0 ? participantFiles[0].id : null;
            return {...participant, file: participantFile};
          });

          return {...application, participants: applicationParticipantsWithFiles};
        });

        // Przyporządkuj konkursy do odpowiednich aplikacji
        const applicationsWithCompetitions = applicationsWithParticipantsAndFiles.map(application => {
          const competition = competitions.find(comp => comp.id === application.competition);
          return {...application, competition};
        });

        setApplicationsData(applicationsWithCompetitions);

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    fetchData();
  }, []);


  const handleDeleteParticipant = async (participantId) => {
    const isConfirmed = window.confirm('Czy na pewno chcesz usunąć tego uczestnika?');
    if (isConfirmed) {
      try {
        await deleteParticipantAndCheckApplication(participantId);

        setApplicationsData(prevApplications => {
          const updatedApplications = prevApplications.map(application => {
            const updatedParticipants = application.participants.filter(participant => participant.id !== participantId);

            // Log information to understand the process
            console.log('Application ID:', application.id);
            console.log('Updated Participants:', updatedParticipants);

            return updatedParticipants.length !== 0 ? {...application, participants: updatedParticipants} : null;
          });

          // Log the updated applications
          console.log('Updated Applications:', updatedApplications);

          const filteredApplications = updatedApplications.filter(Boolean);

          // Log the filtered applications
          console.log('Filtered Applications:', filteredApplications);

          return filteredApplications;
        });
      } catch (error) {
        console.error("Error deleting participant:", error);
      }
    }
  };


  const handleDeleteApplication = async (applicationId) => {
    const isConfirmed = window.confirm('Czy na pewno chcesz usunąć to zgłoszenie?');

    if (isConfirmed) {
      console.log('Deleting application with ID:', applicationId);

      // Wywołanie funkcji do usunięcia aplikacji (jeśli to konieczne)
      await deleteApplication(applicationId);

      // Aktualizacja stanu, usuwając aplikację o zadanym ID
      setApplicationsData(prevApplicationsData =>
        prevApplicationsData.filter(application => application.id !== applicationId)
      );
    }
  };


  const handleCloseAddParticipantModal = () => {
    setShowAddParticipantModal(false);
  };

  const handleAddParticipant = async (competitionId, newParticipant) => {
    // Call the submitForm function with formData and competitionId
    const createdParticipant = await submitForm(competitionId, newParticipant);
    setApplicationsData(prevApplications => {
      // Find the application to which the participant is added
      const updatedApplications = prevApplications.map(application => {
        if (application.competition.id === competitionId) {
          // Add the created participant to the application
          return {
            ...application,
            participants: [...application.participants, createdParticipant]
          };
        }
        return application;
      });

      // Log the updated applications
      console.log('Updated Applications:', updatedApplications);

      return updatedApplications;
    });
    // Close the modal after adding the participant
    handleCloseAddParticipantModal();
  };

  const handleEditParticipant = async (participantId, editedData) => {
    try {
      // Wywołaj funkcję do aktualizacji uczestnika
      const updatedParticipant = await updateParticipant(participantId, editedData);

      // Zaktualizuj stan applications
      setApplicationsData(prevApplications => {
        // Mapuj po poprzednim stanie i zaktualizuj uczestnika w odpowiedniej aplikacji
        const updatedApplications = prevApplications.map(application => {
          const updatedParticipants = application.participants.map(participant => {
            // Znajdź uczestnika o tym samym ID co zaktualizowany uczestnik
            if (participant.id === participantId) {
              // Zaktualizuj uczestnika
              return updatedParticipant;
            }
            return participant;
          });

          // Zwróć zaktualizowaną aplikację z zaktualizowanymi uczestnikami
          return {...application, participants: updatedParticipants};
        });

        // Log the updated applications
        console.log('Updated Applications:', updatedApplications);

        return updatedApplications;
      });

      console.log('Updated participant:', updatedParticipant);
    } catch (error) {
      console.error('Error updating participant:', error);
    }
  };
  const handleAddAttachment = async (participantId, newAttachment) => {
    console.log(participantId, newAttachment);

    try {
      // Wywołaj funkcję do przesłania załącznika
      const uploadedFile = await uploadAttachment(participantId, newAttachment);

      // Zaktualizuj applicationData, dodając nowy plik do odpowiedniego uczestnika
      setApplicationsData(prevApplications => {
        // Mapuj po poprzednim stanie i zaktualizuj uczestnika w odpowiedniej aplikacji
        const updatedApplications = prevApplications.map(application => {
          const updatedParticipants = application.participants.map(participant => {
            // Znajdź uczestnika o tym samym ID co przekazane participantId
            if (participant.id === participantId) {
              // Dodaj nowy plik do uczestnika (jeśli nie ma jeszcze przypisanego pliku)
              const updatedFile = participant.file ? participant.file : uploadedFile.id;
              return {...participant, file: updatedFile};
            }
            return participant;
          });

          // Zwróć zaktualizowaną aplikację z zaktualizowanymi uczestnikami
          return {...application, participants: updatedParticipants};
        });

        // Log the updated applications
        console.log('Updated Applications:', updatedApplications);

        return updatedApplications;
      });

      console.log('Uploaded file:', uploadedFile);
    } catch (error) {
      console.error('Error uploading attachment:', error);
    }
  };

  return (
    <div className="user-panel">
      <Link to="/konkursy">
        <button style={buttonStyle}>Przejdź do konkursów</button>
      </Link>
      {applicationsData.length !== 0 ? (
          <>
            <UserPanelHeader/>
            <UserApplicationsTable
              applications={applicationsData}
              onDeleteParticipant={handleDeleteParticipant}
              onDeleteApplication={handleDeleteApplication}
              onAddParticipant={handleAddParticipant}
              onEditParticipant={handleEditParticipant}
              onAddAttachment={handleAddAttachment}
            />
          </>
        ) :
        (
          <>
            <p>Nie posiadasz obecnie żadnych zgłoszeń.</p>
          </>
        )}
    </div>
  );
}

export default UserPanel;
