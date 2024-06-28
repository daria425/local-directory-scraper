import PropTypes from "prop-types";
import CsvTable from "./CSVTable.jsx";
import { capitalize } from "./helpers/capitalize.js";
export default function SearchResult({
  csvData,
  userSelection,
  startNewSearch,
}) {
  const { subCategory, region } = userSelection;
  const { downloadInfo, jsonData } = csvData;
  return (
    <div className="result__container">
      <h2 className="result__preview">CSV Preview:</h2>
      <p className="result__heading">
        Services and organizations for {subCategory} in {capitalize(region)}
      </p>
      <CsvTable csvData={jsonData} />
      <div className="result__btns">
        <a
          className="result__btn"
          href={downloadInfo.downloadURL}
          download={downloadInfo.downloadName}
        >
          Download CSV
        </a>
        <button
          onClick={startNewSearch}
          className="result__btn result__btn--new-search"
        >
          New Search
        </button>
      </div>
    </div>
  );
}

SearchResult.propTypes = {
  csvData: PropTypes.object,
  userSelection: PropTypes.object,
  dataLoading: PropTypes.bool,
  fetchError: PropTypes.string,
  startNewSearch: PropTypes.func,
};
