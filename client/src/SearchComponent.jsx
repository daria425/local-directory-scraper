import PropTypes from "prop-types";
import SelectRegion from "./SelectRegion";
import SelectSubcategories from "./SelectSubcategories";

export default function SearchComponent({
  subCategories,
  selectionStep,
  getSubcategories,
  mainCategories,

  region,

  getCSV,
  handleChangeStep,
  getMainCategories,
}) {
  return (
    <div className="search">
      <>
        {selectionStep === 1 && (
          <SelectRegion getMainCategories={getMainCategories} />
        )}
        {selectionStep > 1 && (
          <>
            <SelectSubcategories
              selectionStep={selectionStep}
              mainCategories={mainCategories}
              region={region}
              getSubcategories={getSubcategories}
              getCSV={getCSV} // Use the local handler
              subCategories={subCategories}
            />
            <div className="search__footer">
              <button
                className="search__btn"
                onClick={() => handleChangeStep(selectionStep - 1)}
              >
                Back
              </button>
            </div>
          </>
        )}
      </>
    </div>
  );
}

SearchComponent.propTypes = {
  mainCategories: PropTypes.array,
  subCategories: PropTypes.array,
  selectionStep: PropTypes.number,
  fetchError: PropTypes.string,
  dataLoading: PropTypes.bool,
  getSubcategories: PropTypes.func,
  getMainCategories: PropTypes.func,
  region: PropTypes.string,
  getCSV: PropTypes.func,
  handleChangeStep: PropTypes.func,
};
