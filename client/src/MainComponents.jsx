import { useState } from "react";
import { api_base } from "./api/api_base";
import { testCSVData } from "../testData"; //eslint-disable-line
import Loader from "./Loader";
import Papa from "papaparse";
import SearchComponent from "./SearchComponent";
import SearchResult from "./SearchResult";
export default function MainComponents() {
  const [selectionStep, setSelectionStep] = useState(1);
  const [userSelection, setUserSelection] = useState({});
  const [categories, setCategories] = useState({});
  const [csvData, setCsvData] = useState(null);
  const [fetchError, setFetchError] = useState(null);
  const [dataLoading, setDataLoading] = useState(false);

  async function getMainCategories(region) {
    setDataLoading(true);
    setUserSelection({ ...userSelection, region: region });
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
  async function getSubcategories(region, url, mainCategory) {
    setUserSelection({ ...userSelection, mainCategory: mainCategory });
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
    console.log(selectionStep);
    if (selectionStep === 2) {
      setCategories({ ...categories, subCategories: null });
    } else if (selectionStep === 1) {
      setCategories({
        ...categories,
        mainCategories: null,
        subCategories: null,
      });
    }

    setSelectionStep(selectionStep);
  }

  async function getCSV(region, url, subCategory) {
    setDataLoading(true);
    setSelectionStep(0);
    setUserSelection({ ...userSelection, subCategory: subCategory });
    console.log(url);
    try {
      const response = await fetch(`${api_base}csv-file/?region=${region}`, {
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ "url": url }),
      });
      if (response.status === 200) {
        const blob = await response.blob();
        const downloadURL = window.URL.createObjectURL(blob);
        const downloadName = `${subCategory}-${region}.csv`;
        const reader = new FileReader();
        reader.onload = (event) => {
          const csvContent = event.target.result;
          Papa.parse(csvContent, {
            complete: (results) => {
              const data = results.data;
              console.log(data);
              setCsvData({
                downloadInfo: { downloadURL, downloadName },
                jsonData: data,
              });
            },
            error: (error) => {
              setFetchError(`Parsing error: ${error.message}`);
            },
          });
        };

        reader.readAsText(blob);
        setFetchError(null); // Clear any previous errors
      } else {
        const errorText = await response.text();
        setFetchError(`Error: ${response.status} - ${errorText}`);
        setCsvData(null); // Clear categories if there's an error
      }
    } catch (error) {
      setFetchError(`Network error: ${error.message}`);
      setCsvData(null); // Clear categories if there's an error
    } finally {
      setDataLoading(false);
    }
  }
  return (
    <section className="container">
      {dataLoading && <Loader />}
      {fetchError && <div className="error">{fetchError}</div>}
      {!dataLoading && !fetchError && csvData ? (
        <section className="result">
          <SearchResult csvData={csvData} userSelection={userSelection} />
        </section>
      ) : (
        <SearchComponent
          selectionStep={selectionStep}
          mainCategories={categories?.mainCategories}
          region={userSelection?.region}
          getSubcategories={getSubcategories}
          getCSV={getCSV}
          subCategories={categories.subCategories}
          getMainCategories={getMainCategories}
          handleChangeStep={handleChangeStep}
        />
      )}
    </section>
  );
}
