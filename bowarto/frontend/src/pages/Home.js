import React from "react";
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ErrorModal from "./ErrorModal"

function Home() {

  return (
    <div>
      <div>
        <h1 className="mt-5">Witamy na platformie konkursowej fundacji BoWarto!</h1>
      </div>
    </div>
  );
}
export default Home;
