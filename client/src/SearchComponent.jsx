import PropTypes from "prop-types";
import SelectRegion from "./SelectRegion";
import SelectSubcategories from "./SelectSubcategories";
export default function SearchComponent({
  subCategories,
  selectionStep,
  getSubcategories,
  mainCategories,
  fetchError,
  region,
  dataLoading,
  getCSV,
  handleChangeStep,
  getMainCategories,
}) {
  return (
    <section className="search">
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
            getCSV={getCSV}
            subCategories={subCategories}
            fetchError={fetchError}
            dataLoading={dataLoading}
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
    </section>
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
