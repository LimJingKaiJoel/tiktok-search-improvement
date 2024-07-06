import { useState, useEffect } from 'react';
import axios from 'axios';
import './SearchResults.css';
import OpenAI from "openai";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faWandMagicSparkles } from '@fortawesome/free-solid-svg-icons';

const SearchResults = ({ query, onBack, onNavigate }) => {
  const [prediction, setPrediction] = useState('Loading...');
  const [loadingPrediction, setLoadingPrediction] = useState(true);
  const [loadingRecommendation, setLoadingRecommendation] = useState(false);
  const [aiRecommendation, setAiRecommendation] = useState('');
  const [keywords, setKeywords] = useState('');
  const openai = new OpenAI({ apiKey: import.meta.env.VITE_OPENAI_API_KEY, dangerouslyAllowBrowser: true });

  useEffect(() => {
    if (query) {
      const fetchPrediction = async () => {
        try {
          setLoadingPrediction(true);
          setAiRecommendation('');  // Clear previous recommendation
          setKeywords('');  // Clear previous keywords
          const response = await axios.post('https://tiktok-search-improvement.onrender.com/predict', { text: query });
          setPrediction(response.data.prediction);
        } catch (error) {
          console.error('Error fetching prediction:', error);
          setPrediction('Error');
        } finally {
          setLoadingPrediction(false);
        }
      };

      fetchPrediction();
    }
  }, [query]);

  useEffect(() => {
    if (prediction === 'Question') {
      const handleGetRecommendations = async () => {
        try {
          setLoadingRecommendation(true);
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
          const recommendation = response.choices[0].message.content;
          setAiRecommendation(recommendation);

          // New prompt to get keywords
          const keywordsPrompt = `Based on the following question, '${question}', and answer, '${recommendation}', give me up to 3 comma separated keywords that can help me find informative and actionable videos on a short form social media app. The keywords should be directly related to the specific content and themes mentioned in both the question and the answer.`;
          const keywordsResponse = await openai.chat.completions.create({
            model: "gpt-3.5-turbo-0125",
            messages: [
              {
                "role": "user",
                "content": keywordsPrompt
              },
            ],
          });
          setKeywords(keywordsResponse.choices[0].message.content);
        } catch (error) {
          console.error('Error fetching AI recommendation or keywords:', error);
          setAiRecommendation('Error fetching AI recommendation');
          setKeywords('Error fetching keywords');
        } finally {
          setLoadingRecommendation(false);
        }
      };

      handleGetRecommendations();
    }
  }, [prediction]);

  return (
    <div className="search-results">
      <div className="search-bar-disabled">
        <FontAwesomeIcon className="back-button" icon={faArrowLeft} onClick={onBack} />
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
        <div className="ai-suggestion-box">
          <div className="ai-recommendation-content">
            <p><strong>
              <FontAwesomeIcon className="wand-icon" icon={faWandMagicSparkles} />
              Tiktok Assistant</strong></p>
            <p>
              {loadingPrediction
                ? "Loading prediction..."
                : prediction === 'Question'
                ? loadingRecommendation
                  ? "Your query has been identified to be a question, loading recommendations"
                  : aiRecommendation
                : "Your query is not a question, so no specific AI recommendations are displayed"}
            </p>
            <p>{!loadingRecommendation && keywords && `Keywords: ${keywords}`}</p>
            <p className="disclaimer">Always verify important information.</p>
          </div>
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
