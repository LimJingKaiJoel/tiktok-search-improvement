<div className="search-results">
<div className="search-bar">
  <button className="back-button" onClick={onBack}>←</button>
  <input type="text" value={query} readOnly />
</div>
<div className="results">
  <div className="tabs">
    <div className="tab active">Top</div>
    <div className="tab">Videos</div>
    <div className="tab">Users</div>
    <div className="tab">Shop</div>
    <div className="tab">Sounds</div>
    <div className="tab">LIVE</div>
    <div className="tab">Playlists</div>
  </div>
  <div className={`prediction-box ${loading ? 'loading' : prediction === 'Question' ? 'question' : 'non-question'}`}>
    {loading ? (
      <>
        <p><strong>Loading...</strong></p>
        <p>This might take more than 50s if the serverless infrastructure is not started</p>
      </>
    ) : prediction === 'Question' ? (
      <>
        <p><strong>Question</strong></p>
        <p>Your query is a question, would you like some AI recommendations?</p>
        <button className="recommendation-button" onClick={onNavigate}>Get AI Recommendations</button>
      </>
    ) : (
      <>
        <p><strong>Non-Question</strong></p>
        <p>Your query is not a question, so no specific AI recommendations are displayed</p>
      </>
    )}
  </div>
  <div className="result-items">
    <div className="result-item">
      <img src="path/to/image1.jpg" alt="Result 1" />
      <div className="description">Result 1</div>
    </div>
    <div className="result-item">
      <img src="path/to/image2.jpg" alt="Result 2" />
      <div className="description">Result 2</div>
    </div>
    {/* Add more result items as needed */}
  </div>
</div>
</div>
);
};