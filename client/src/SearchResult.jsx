import PropTypes from "prop-types";
import CsvTable from "./CSVTable.jsx";
import { capitalize } from "./helpers/capitalize.js";
export default function SearchResult({ csvData, userSelection }) {
  const { subCategory, region } = userSelection;
  const { downloadInfo, jsonData } = csvData;
  return (
    <div className="result__container">
      <p className="result__heading">
        Services and organizations for {subCategory} in {capitalize(region)}
      </p>
      <CsvTable csvData={jsonData} />
      <a
        className="result__download-btn"
        href={downloadInfo.downloadURL}
        download={downloadInfo.downloadName}
      >
        Download CSV
      </a>
    </div>
  );
}

SearchResult.propTypes = {
  csvData: PropTypes.object,
  userSelection: PropTypes.object,
  dataLoading: PropTypes.bool,
  fetchError: PropTypes.string,
};
