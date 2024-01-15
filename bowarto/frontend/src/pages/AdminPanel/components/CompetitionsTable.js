import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import SingleCompetitionTable from "./SingleCompetitionTable";

const CompetitionsTable = ({ competitionsList }) => {
  const [comingCompetitions, setComingCompetitions] = useState([]);
  const [ongoingCompetitions, setOngoingCompetitions] = useState([]);
  const [otherCompetitions, setOtherCompetitions] = useState([]);

  useEffect(() => {
    const now = new Date();
    const comingCompetitions = competitionsList
      .filter((competition) => new Date(competition.start_at) > now)
      .sort((a, b) => new Date(a.end_at) - new Date(b.end_at));


    const ongoingCompetitions = competitionsList
      .filter((competition) => {
        return new Date(competition.end_at) > now && new Date(competition.start_at) <= now
      })
      .sort((a, b) => new Date(a.end_at) - new Date(b.end_at));


    const otherCompetitions = competitionsList
      .filter((competition) => new Date(competition.end_at) <= now)
      .sort((a, b) => new Date(a.end_at) - new Date(b.end_at));

    setComingCompetitions(comingCompetitions);
    setOngoingCompetitions(ongoingCompetitions);
    setOtherCompetitions(otherCompetitions);
  }, [])
  return (
    <>
      <h1>Konkursy | Zgłoszenia</h1>
      <SingleCompetitionTable competitions={comingCompetitions} header={"Nadchodzące konkursy"} />
      <SingleCompetitionTable competitions={ongoingCompetitions} header={"Aktualne konkursy"} />
      <SingleCompetitionTable competitions={otherCompetitions} header={"Pozostałe konkursy"} />
    </>
  )
}

export default CompetitionsTable;
