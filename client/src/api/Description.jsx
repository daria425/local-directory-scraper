export default function Description() {
  return (
    <div className="description">
      <h1 className="description__title">Council Directory Scraper</h1>
      <p className="description__text">
        This is a web scraper for community directories of UK Councils, which
        creates an aggregated CSV file of information on local support, services
        and activities available.
      </p>
      <ol className="list">
        <p className="list__title">Usage:</p>
        <li className="list__list-item">1. Select a council to get started</li>
        <li className="list__list-item">
          2. Select one of the available categories
        </li>
        <li className="list__list-item">
          3. Select a subcategory to retrieve information from
        </li>
      </ol>
    </div>
  );
}
