import 'chart.js/auto';
import React, {useEffect, useState} from "react";
import {getStats} from "../api/requests/stats";
import refreshAccessToken from "../requests/refresh";
import {Bar, Doughnut} from "react-chartjs-2";
import {Chart, ArcElement} from 'chart.js'

Chart.register(ArcElement);


const LOADING_MESSAGE = "Trwa ładowanie...";


const styles = {
  statsContainer: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100%",
    padding: "20px", // Dodatkowy padding dla estetyki
  },
  statsGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gridTemplateRows: "repeat(2, 1fr)",
    gap: "20px",
    width: "100%", // Wypełnia całą dostępną szerokość
    height: "100%",
  },
  gridItem: {
    padding: "20px",
    border: "1px solid #ccc",
    // height: "100%", // Wypełnia całą dostępną wysokość
  },
  chartContainer: {
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
};

// ...

const options = {
  plugins: {
    legend: {
      display: true,
      position: 'center', // Możesz dostosować pozycję legendy
    },
  },
};

const Stats = () => {
  const [stats, setStats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      await refreshAccessToken();
      const stats = await getStats();
      setStats(stats);
      setLoading(false);
      console.log(stats);
    } catch (error) {
      console.error("Error fetching data:", error);
      setLoading(false);
    }
  };

  const competitionsData = {
    labels: ["Trwające", "Nadchodzące", "Zakończone"],
    datasets: [
      {
        data: [
          stats.ongoing_competitions_count,
          stats.upcoming_competitions_count,
          stats.finished_competitions_count,
        ],
        backgroundColor: ["lightcoral", "lightblue", "lightgreen"],
      },
    ],
  };

  const userChartData = {
    labels: ["Zwykli użytkownicy", "Nauczyciele"],
    datasets: [
      {
        data: [stats.users_count - stats.school_user_count, stats.school_user_count],
        backgroundColor: ["lightcoral", "lightblue"],
      },
    ],
  };

  const competitionParticipants = stats.competition_participants || {};
  const competitionParticipantsData = {
    labels: Object.values(competitionParticipants).map(competition => competition.title),
    datasets: [
      {
        label: 'Liczba uczestników',
        data: Object.values(competitionParticipants).map(competition => competition.participants_count),
        backgroundColor: 'rgba(75, 192, 192, 0.7)',
      },
    ],
  };
  const competitionParticipantsOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text: 'Konkursy',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Liczba uczestników',
        },
        min: 0,
      },
    },
  };
  const userParticipants = stats.user_participants || {};
  const userParticipantsData = {
    labels: Object.values(userParticipants).map(user => user.user),
    datasets: [
      {
        label: 'Liczba uczestnictw',
        data: Object.values(userParticipants).map(user => user.participants_count),
        backgroundColor: 'rgba(75, 192, 192, 0.7)',
      },
    ],
  };
  const userParticipantsOptions = {
    scales: {
      x: {
        title: {
          display: true,
          text: 'Użytkownicy',
        },
      },
      y: {
        title: {
          display: true,
          text: 'Liczba uczestnictw',
        },
        min: 0,
      },
    },
  };
  return (
    <div style={styles.statsContainer}>
      {loading ? (
        LOADING_MESSAGE
      ) : (
        <div
          style={{...styles.statsGrid, gridTemplateColumns: "repeat(3, 1fr)"}}>
          <div style={styles.gridItem}>
            <h2>Statystyki</h2>
            <p>Zgłoszonych uczestników: {stats.participants_count}</p>
            <p>Złożonych aplikacji: {stats.applications_count}</p>
            <p>Przesłanych prac: {stats.attachments_count}</p>
            <p>Oczekujących zatwierdzeń: {stats.approvals_count}</p>
          </div>
          <div style={styles.gridItem}>
            <h2>Konkursy</h2>
            <div style={styles.chartContainer}>
              <Doughnut data={competitionsData} options={{
                ...options,
                plugins: {legend: {display: false}}
              }}/>
            </div>
          </div>
          <div style={styles.gridItem}>
            <h2>Użytkownicy</h2>
            <div style={styles.chartContainer}>
              <Doughnut data={userChartData} options={{
                ...options,
                plugins: {legend: {display: false}}
              }}/>
            </div>
          </div>
          {/* Dodaj nowy grid item na wykres słupkowy */}
          <div style={{...styles.gridItem, gridColumn: 'span 3'}}>
            <h2>Popularnosć konkursów</h2>
            <div style={styles.chartContainer}>
              <Bar data={competitionParticipantsData}
                   options={competitionParticipantsOptions}/>
            </div>
          </div>
          <div style={{...styles.gridItem, gridColumn: 'span 3'}}>
            <h2>Aktywność użytkownikow</h2>
            <div style={styles.chartContainer}>
              <Bar data={userParticipantsData}
                   options={userParticipantsOptions}/>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Stats;
