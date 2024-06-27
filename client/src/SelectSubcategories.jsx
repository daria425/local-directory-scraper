import PropTypes from "prop-types";
import Loader from "./hooks/Loader";
export default function SelectSubcategories({
  subCategories,
  selectionStep,
  getSubcategories,
  mainCategories,
  fetchError,
  region,
  dataLoading,
}) {
  const selectionSteps = {
    2: {
      heading_label: "Select a category",
      categories: mainCategories,
      selectFn: getSubcategories,
      nameLabel: "category_name",
      urlLabel: "category_link",
    },
    3: {
      heading_label: "Select a subcategory",
      categories: subCategories,
      selectFn: () => {},
      nameLabel: "subcategory_name",
      urlLabel: "subcategory_link",
    },
    // You can add more steps here if needed
  };

  const currentStep = selectionSteps[selectionStep];

  if (fetchError) {
    return <div className="error">{fetchError}</div>;
  }

  if (dataLoading) {
    return <Loader />;
  }

  return (
    <>
      <p className="search__heading">{currentStep.heading_label}</p>
      {currentStep.categories &&
        currentStep.categories.length > 0 &&
        currentStep.categories.map((category) => (
          <button
            key={category[currentStep.urlLabel]} // Make sure category has a unique id
            onClick={() =>
              currentStep.selectFn(region, category[currentStep.urlLabel])
            }
          >
            {category[currentStep.nameLabel]}
          </button>
        ))}
    </>
  );
}
SelectSubcategories.propTypes = {
  mainCategories: PropTypes.array,
  subCategories: PropTypes.array,
  selectionStep: PropTypes.number,
  fetchError: PropTypes.string,
  dataLoading: PropTypes.bool,
  getSubcategories: PropTypes.func,
  region: PropTypes.string,
};
