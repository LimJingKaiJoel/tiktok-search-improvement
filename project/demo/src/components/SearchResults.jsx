import { useState, useEffect } from 'react';
import axios from 'axios';
import './SearchResults.css';

const SearchResults = ({ query, onBack }) => {
  const [prediction, setPrediction] = useState('Loading...');

  useEffect(() => {
    if (query) {
      const fetchPrediction = async () => {
        try {
          const response = await axios.post('https://tiktok-search-improvement.onrender.com/predict', { text: query });
          setPrediction(response.data.prediction);
        } catch (error) {
          console.error('Error fetching prediction:', error);
        }
      };

      fetchPrediction();
    }
  }, [query]);
  return (
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
        {prediction && (
          <div className="prediction-result">
            <strong>Prediction:</strong> {prediction}
          </div>
        )}
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

export default SearchResults;
