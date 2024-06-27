import PropTypes from "prop-types";
import CsvTable from "./CSVTable.jsx";

export default function SearchResult({ csvData, userSelection }) {
  const { subCategory, region } = userSelection;
  return (
    <section className="result">
      <p className="result__heading">
        Data for {subCategory} in {region}
      </p>
      <CsvTable csvData={csvData} />
    </section>
  );
}

SearchResult.propTypes = {
  csvData: PropTypes.object,
  userSelection: PropTypes.object,
  dataLoading: PropTypes.bool,
  fetchError: PropTypes.string,
};
