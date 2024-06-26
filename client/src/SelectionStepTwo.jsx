import PropTypes from "prop-types";
import Loader from "./hooks/Loader";
export default function SelectionStepTwo({
  mainCategories,
  fetchError,
  dataLoading,
}) {
  if (fetchError) {
    return <div className="error">{fetchError}</div>;
  }

  if (dataLoading) {
    return <Loader />;
  }
  return (
    <>
      <p className="search__heading">Select a category:</p>
      {mainCategories.map((category) => (
        <button
          key={category["category_name"]}
          onClick={() => console.log(category)}
        >
          {category["category_name"]}
        </button>
      ))}
    </>
  );
}

SelectionStepTwo.propTypes = {
  mainCategories: PropTypes.array,
  fetchError: PropTypes.string,
  dataLoading: PropTypes.bool,
};
