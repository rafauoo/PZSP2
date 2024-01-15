import { Form } from "react-bootstrap";

const CompetitionSearchBar = ({ selectValues, setSelectSearch }) => {

  const preventSubmiting = (e) => {
    e.preventDefault();
  };

  return (
    <Form className="w-50 pe-5" onSubmit={preventSubmiting}>
      <Form.Select className="underline-search" onChange={setSelectSearch} >
        <option value="">All</option>
        {selectValues.map((option, index) => (
          <option key={index} value={option}>{option}</option>
        ))}
      </Form.Select>
    </Form>
  )
}
export default CompetitionSearchBar;
