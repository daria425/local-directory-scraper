import PropTypes from "prop-types";

export default function Error({
  errorMessage,
  retryFunction = () => {},
  startNewSearch,
}) {
  return (
    <div className="error">
      <p className="error_message">An error occured while fetching data.</p>
      <p className="error__message">{errorMessage}</p>
      <div className="error__btn-container">
        <button className="error__btn" onClick={retryFunction}>
          Try Again
        </button>
        <button
          onClick={startNewSearch}
          className="error__btn error__btn--new-search"
        >
          New Search
        </button>
      </div>
    </div>
  );
}

Error.propTypes = {
  errorMessage: PropTypes.string,
  retryFunction: PropTypes.func,
  startNewSearch: PropTypes.func,
};
