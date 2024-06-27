import PropTypes from "prop-types";
export default function CsvTable({ csvData }) {
  const columnLabels = Object.keys(csvData);
  const columnValues = Object.values(csvData);
  const valueArr = columnValues.map((value) => Object.values(value));
  const transposedValues = valueArr[0].map((_, colIndex) =>
    valueArr.map((row) => row[colIndex])
  );
  return (
    <div className="result__table-constraint">
      <div className="result__table-container">
        <table className="result__table">
          <thead>
            <tr>
              {columnLabels.map((label, index) => (
                <th className="result__table-header" key={index}>
                  {label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="result__table-body">
            {transposedValues.map((row, rowIndex) => (
              <tr className="result__table-row" key={rowIndex}>
                {row.map((value, colIndex) => (
                  <td
                    className="result__table-content"
                    key={colIndex}
                    data-label={columnLabels[colIndex]}
                  >
                    {value}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

CsvTable.propTypes = {
  dataLoading: PropTypes.bool,
  fetchError: PropTypes.string,
  csvData: PropTypes.object,
};
