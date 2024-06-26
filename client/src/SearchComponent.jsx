import { useState } from "react";
import { api_base } from "./api/api_base";
import SelectionStepOne from "./SelectionStepOne";
import SelectionStepTwo from "./SelectionStepTwo";
export default function SearchComponent() {
  const [selectionStep, setSelectionStep] = useState(1);
  const [categories, setCategories] = useState({});
  const [fetchError, setFetchError] = useState(null);
  const [dataLoading, setDataLoading] = useState(false);

  async function getMainCategories(region) {
    setDataLoading(true);
    setSelectionStep(2);
    try {
      const response = await fetch(`${api_base}search/?region=${region}`);
      if (response.status === 200) {
        const mainCategories = await response.json();
        console.log(mainCategories);
        setCategories({ ...categories, mainCategories: mainCategories });
        setFetchError(null); // Clear any previous errors
      } else {
        const errorText = await response.text();
        setFetchError(`Error: ${response.status} - ${errorText}`);
        setCategories({ ...categories, mainCategories: null }); // Clear categories if there's an error
      }
    } catch (error) {
      setFetchError(`Network error: ${error.message}`);
      setCategories({ ...categories, mainCategories: null }); // Clear categories if there's an error
    } finally {
      setDataLoading(false);
    }
  }

  function handleChangeStep(selectionStep) {
    setSelectionStep(selectionStep);
  }

  return (
    <section className="search">
      {selectionStep === 1 && (
        <SelectionStepOne getMainCategories={getMainCategories} />
      )}
      {selectionStep === 2 && (
        <SelectionStepTwo
          mainCategories={categories?.mainCategories}
          fetchError={fetchError}
          dataLoading={dataLoading}
        />
      )}
      {selectionStep > 1 && (
        <div className="search__footer">
          <button onClick={() => handleChangeStep(selectionStep - 1)}>
            Back
          </button>
        </div>
      )}
    </section>
  );
}
