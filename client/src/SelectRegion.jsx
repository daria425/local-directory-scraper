import PropTypes from "prop-types";
import { capitalize } from "./helpers/capitalize";
export default function SelectRegion({ getMainCategories }) {
  const regions = ["camden", "islington"];
  return (
    <>
      <p className="search__heading">Select a council to begin:</p>
      <div className="search__btn-container search__btn-container--regions">
        {regions.map((region) => (
          <button
            className="search__btn"
            key={region}
            onClick={() => getMainCategories(region)}
          >
            {capitalize(region)}
          </button>
        ))}
      </div>
    </>
  );
}

SelectRegion.propTypes = {
  getMainCategories: PropTypes.func,
};
