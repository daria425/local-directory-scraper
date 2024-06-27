import { useState } from "react";
import { api_base } from "./api/api_base";
import SelectRegion from "./SelectRegion";
import SelectSubcategories from "./SelectSubcategories";
export default function SearchComponent() {
  const [selectionStep, setSelectionStep] = useState(1);
  const [selectedRegion, setSelectedRegion] = useState(null);
  const [categories, setCategories] = useState({});
  const [fetchError, setFetchError] = useState(null);
  const [dataLoading, setDataLoading] = useState(false);

  async function getMainCategories(region) {
    setDataLoading(true);
    setSelectedRegion(region);
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
  async function getSubcategories(region, url) {
    setDataLoading(true);
    setSelectionStep(3);
    try {
      const response = await fetch(
        `${api_base}search/subcategories?region=${region}`,
        {
          method: "post",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ "url": url }),
        }
      );
      if (response.status === 200) {
        const subCategories = await response.json();
        console.log(subCategories);
        setCategories({ ...categories, subCategories: subCategories });
        setFetchError(null); // Clear any previous errors
      } else {
        const errorText = await response.text();
        setFetchError(`Error: ${response.status} - ${errorText}`);
        setCategories({ ...categories, subCategories: null }); // Clear categories if there's an error
      }
    } catch (error) {
      setFetchError(`Network error: ${error.message}`);
      setCategories({ ...categories, subCategories: null }); // Clear categories if there's an error
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
        <SelectRegion getMainCategories={getMainCategories} />
      )}
      {selectionStep > 1 && (
        <>
          <SelectSubcategories
            selectionStep={selectionStep}
            mainCategories={categories?.mainCategories}
            region={selectedRegion}
            getSubcategories={getSubcategories}
            subCategories={categories.subCategories}
            fetchError={fetchError}
            dataLoading={dataLoading}
          />
          <div className="search__footer">
            <button onClick={() => handleChangeStep(selectionStep - 1)}>
              Back
            </button>
          </div>
        </>
      )}
    </section>
  );
}
