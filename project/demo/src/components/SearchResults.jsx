import { useState, useEffect } from 'react';
import axios from 'axios';
import openai from 'openai';
import './SearchResults.css';

const SearchResults = ({ query, onBack }) => {
  const [prediction, setPrediction] = useState('Loading...');
  const [loading, setLoading] = useState(true);
  const [aiRecommendation, setAiRecommendation] = useState('');

  useEffect(() => {
    if (query) {
      const fetchPrediction = async () => {
        try {
          setLoading(true);
          const response = await axios.post('https://tiktok-search-improvement.onrender.com/predict', { text: query });
          setPrediction(response.data.prediction);
          setLoading(false);
        } catch (error) {
          console.error('Error fetching prediction:', error);
          setPrediction('Error');
          setLoading(false);
        }
      };

      fetchPrediction();
    }
  }, [query]);

  const handleGetRecommendations = async () => {
    try {
      setLoading(true);
      openai.api_key = process.env.REACT_APP_OPENAI_API_KEY;
      const prompt = `In 1 sentence, answer the following concisely: ${query}`;
      const response = await openai.chat.completions.create({
        model: "gpt-3.5-turbo-0125",
        messages: [
          {
            "role": "user",
            "content": prompt,
          },
        ],
      });
      setAiRecommendation(response.choices[0].message.content);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching AI recommendation:', error);
      setAiRecommendation('Error fetching AI recommendation');
      setLoading(false);
    }
  };

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
              <button className="recommendation-button" onClick={handleGetRecommendations}>Get AI Recommendations</button>
              {aiRecommendation && (
                <div className="ai-recommendation">
                  <p><strong>AI Recommendation:</strong></p>
                  <p>{aiRecommendation}</p>
                </div>
              )}
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

export default SearchResults;
