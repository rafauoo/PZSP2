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
      <br></br>
      <h1>Zgłoszenia do konkursów</h1>
      <br></br>
      <SingleCompetitionTable competitions={ongoingCompetitions}/>
      <br></br>
      <br></br>
      <SingleCompetitionTable competitions={otherCompetitions} header={"Zakończone konkursy"} />
      <br></br>
      <br></br>
    </>
  )
}

export default CompetitionsTable;
