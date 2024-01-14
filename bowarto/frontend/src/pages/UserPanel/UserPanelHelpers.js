import {
  deleteApplication,
  deleteParticipantAndCheckApplication, downloadFile,
  submitForm,
  updateParticipant,
  uploadAttachment,
  deleteFile
} from "../../requests/user_panel";

export const handleDeleteParticipantLogic = async (participantId, prevApplications) => {
  try {
    await deleteParticipantAndCheckApplication(participantId);

    const updatedApplications = prevApplications.map((application) => {
      const updatedParticipants = application.participants.filter((participant) => participant.id !== participantId);

      return updatedParticipants.length !== 0 ? {
        ...application,
        participants: updatedParticipants
      } : null;
    });

    return {
      updatedApplications,
      showMessageModal: true,
      messageText: 'Pomyślnie usunięto uczestnika.'
    };
  } catch (error) {
    console.error('Error deleting participant:', error);
    return {
      showMessageModal: true,
      messageText: 'Uczestnik nie został usunięty.'
    };
  }
};
export const handleDeleteApplicationLogic = async (applicationId, prevApplicationsData) => {
  try {
    console.log('Deleting application with ID:', applicationId);

    // Wywołanie funkcji do usunięcia aplikacji (jeśli to konieczne)
    await deleteApplication(applicationId);

    // Aktualizacja stanu, usuwając aplikację o zadanym ID
    const updatedApplications = prevApplicationsData.filter(application => application.id !== applicationId);

    return {
      updatedApplications,
      showMessageModal: true,
      messageText: 'Pomyślnie usunięto zgłoszenie.'
    };
  } catch (error) {
    console.error('Error deleting application:', error);
    return {
      showMessageModal: true,
      messageText: 'Błąd podczas usuwania zgłoszenia.'
    };
  }
};

export const handleAddParticipantLogic = async (competitionId, newParticipant, prevApplications) => {
  try {
    // Call the submitForm function with formData and competitionId
    const createdParticipant = await submitForm(competitionId, newParticipant);

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

    return {
      updatedApplications,
      showMessageModal: true,
      messageText: 'Pomyślnie dodano uczestnika.'
    };
  } catch (error) {
    console.error('Error adding participant:', error);
    return {
      showMessageModal: true,
      messageText: 'Błąd podczas dodawania uczestnika.'
    };
  }
};

export const handleEditParticipantLogic = async (participantId, editedData, prevApplications) => {
  try {
    // Wywołaj funkcję do aktualizacji uczestnika
    const updatedParticipant = await updateParticipant(participantId, editedData);

    // Zaktualizuj stan applications
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

    return {
      updatedApplications,
      showMessageModal: true,
      messageText: 'Pomyślnie edytowano uczestnika.'
    };
  } catch (error) {
    console.error('Error updating participant:', error);
    return {
      showMessageModal: true,
      messageText: 'Błąd podczas aktualizacji uczestnika.'
    };
  }
};

export const handleAddAttachmentLogic = async (participantId, newAttachment, prevApplications) => {
  try {
    // Wywołaj funkcję do przesłania załącznika
    const uploadedFile = await uploadAttachment(participantId, newAttachment);

    // Zaktualizuj applicationData, dodając nowy plik do odpowiedniego uczestnika
    const updatedApplications = prevApplications.map(application => {
      const updatedParticipants = application.participants.map(participant => {
        // Znajdź uczestnika o tym samym ID co przekazane participantId
        if (participant.id === participantId) {
          // Dodaj nowy plik do uczestnika (jeśli nie ma jeszcze przypisanego pliku)
          const updatedFile = participant.attachment ? participant.attachment : uploadedFile.id;
          return {...participant, attachment: updatedFile};
        }
        return participant;
      });

      // Zwróć zaktualizowaną aplikację z zaktualizowanymi uczestnikami
      return {...application, participants: updatedParticipants};
    });

    return {
      updatedApplications,
      showMessageModal: true,
      messageText: 'Pomyślnie dodano załącznik.'
    };
  } catch (error) {
    console.error('Error uploading attachment:', error);
    return {
      showMessageModal: true,
      messageText: 'Błąd podczas przesyłania załącznika.'
    };
  }
};

export const removeFileFromParticipant = (participant, participantId) => {
  if (participant.id === participantId) {
    return {...participant, attachment: null};
  }
  return participant;
};

export const removeFileFromApplications = (applications, participantId) => {
  return applications.map(application => {
    const updatedParticipants = application.participants.map(participant => {
      return removeFileFromParticipant(participant, participantId);
    });
    return {...application, participants: updatedParticipants};
  });
};

export const handleRemoveFileLogic = async (participantId, prevApplications) => {
  try {
    // Wywołaj funkcję do usunięcia załącznika
    await deleteFile(participantId);

    // Zaktualizuj applicationData, usuwając plik z odpowiedniego uczestnika
    const updatedApplications = removeFileFromApplications(prevApplications, participantId);

    return {
      updatedApplications,
      showMessageModal: true,
      messageText: 'Plik został pomyślnie usunięty.'
    };
  } catch (error) {
    console.error('Error removing file:', error);
    return {
      showMessageModal: true,
      messageText: 'Błąd podczas usuwania pliku.'
    };
  }
};

export const handleDownloadFileLogic = async (attachmentId) => {
  try {
    // Wywołaj funkcję do pobrania pliku
    await downloadFile(attachmentId);

    return {
      showMessageModal: true,
      messageText: 'Plik został pomyślnie pobrany.'
    };
  } catch (error) {
    console.error('Error downloading file:', error);
    return {
      showMessageModal: true,
      messageText: 'Błąd podczas pobierania pliku.'
    };
  }
};
