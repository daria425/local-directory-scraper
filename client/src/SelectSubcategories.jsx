import PropTypes from "prop-types";
export default function SelectSubcategories({
  subCategories,
  selectionStep,
  getSubcategories,
  mainCategories,
  region,
  getCSV,
}) {
  const selectionSteps = {
    2: {
      heading_label: "Select a category to scrape",
      categories: mainCategories,
      selectFn: getSubcategories,
      nameLabel: "category_name",
      urlLabel: "category_link",
    },
    3: {
      heading_label: "Select a further subcategory to scrape",
      categories: subCategories,
      selectFn: getCSV,
      nameLabel: "subcategory_name",
      urlLabel: "subcategory_link",
    },
    // You can add more steps here if needed
  };

  const currentStep = selectionSteps[selectionStep];

  if (currentStep.categories && currentStep.categories.length > 0) {
    return (
      <>
        <p className="search__heading">{currentStep.heading_label}</p>
        <div className="search__btn-container">
          {currentStep.categories.map((category) => (
            <button
              className="search__btn"
              key={category[currentStep.urlLabel]}
              onClick={() =>
                currentStep.selectFn(
                  region,
                  category[currentStep.urlLabel],
                  category[currentStep.nameLabel]
                )
              }
            >
              {category[currentStep.nameLabel]}
            </button>
          ))}
        </div>
      </>
    );
  }
}
SelectSubcategories.propTypes = {
  mainCategories: PropTypes.array,
  subCategories: PropTypes.array,
  selectionStep: PropTypes.number,
  fetchError: PropTypes.string,
  dataLoading: PropTypes.bool,
  getSubcategories: PropTypes.func,
  region: PropTypes.string,
  getCSV: PropTypes.func,
};
