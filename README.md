# Platforma konkursowa dla fundacji BoWarto

## Cel Projektu
Stworzenie nowoczesnej platformy, która usprawni proces rejestracji, zbierania zgłoszeń oraz oceniania konkursów fotograficznych, literackich i innych aktywności. Ma umożliwić łatwą integrację z istniejącą stroną internetową fundacji. Celem jest zwiększenie efektywności organizacyjnej, poprawa przejrzystości procesu oceniania oraz zwiększenie zaangażowania społeczności lokalnej poprzez uproszczenie i ułatwienie udziału w aktywnościach fundacji.

## Architektura
Realizacja projektu opiera się na architekturze modularnego monolitu. Modularność pozwala na elastyczne dostosowanie systemu do zmian i rozbudowę projektu. Użyte szablony architektoniczne to: 
* MVC (Model-View-Controller)
* Architektura trójwarstwowa: Podział na bazę danych, back-end odpowiedzialny za logikę biznesową oraz front-end.

## Logika
* Serwer aplikacyjny: Środowisko Django dla obsługi warstwy biznesowej.
* System bazy danych: Relacyjna baza danych do przechowywania danych PostgreSQL. Baza danych została postawiona na platformie Azure.
* Mechanizmy zarządzania: Systemy takie jak Git, Trello oraz platform do zarządzania projektem w celu skutecznego zarządzania rozwojem systemu.
