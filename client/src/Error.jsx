import PropTypes from "prop-types";

export default function Error({ errorMessage }) {
  return (
    <div className="error">
      <p className="error__message">{errorMessage}</p>
    </div>
  );
}

Error.propTypes = {
  errorMessage: PropTypes.string,
};
