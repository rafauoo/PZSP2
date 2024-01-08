import React from "react";
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ErrorModal from "./ErrorModal"

function Home() {

  return (
    <div>
      <ErrorModal title="Nie jesteś zalogowany" description="Musisz się zalogować aby móc przeglądać tą stronę" link="login" link_title="Zaloguj" />
      <div>
        <h1 className="mt-5">Witamy na platformie konkursowej BoWarto!</h1>
      </div>

    </div>
  );
}
export default Home;
