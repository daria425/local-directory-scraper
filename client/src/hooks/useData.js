import { useState, useEffect } from "react";

function useData(url) {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);
  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        console.log(url);
        const response = await fetch(url);
        const data = await response.json();
        setData(data);
      } catch (err) {
        console.log(err);
        setError(err);
      } finally {
        setLoading(false);
      }
    }
    fetchData(url);
  }, [url]);
  return {
    loading,
    error,
    data,
  };
}

export { useData };
