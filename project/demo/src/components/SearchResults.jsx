import { useState, useEffect } from 'react';
import axios from 'axios';
import './SearchResults.css';
import OpenAI from "openai";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faSearch } from '@fortawesome/free-solid-svg-icons';
import tiktokStar from '../assets/tiktokstar.png';
import tiktokAI from '../assets/tiktokai.png';
import joelVid from '../assets/set-up-for-demo.mp4';

// Import all video files
import vid1 from '../assets/question-videos/1.mp4';
import vid2 from '../assets/question-videos/2.mp4';
import vid3 from '../assets/question-videos/3.mp4';
import vid4 from '../assets/question-videos/4.mp4';
import vid5 from '../assets/question-videos/5.mp4';
import vid6 from '../assets/question-videos/6.mp4';
import vid7 from '../assets/question-videos/7.mp4';
import vid8 from '../assets/question-videos/8.mp4';
import vid9 from '../assets/question-videos/9.mp4';
import vid10 from '../assets/question-videos/10.mp4';
import vid11 from '../assets/question-videos/11.mp4';
import vid12 from '../assets/question-videos/12.mp4';
import vid13 from '../assets/question-videos/13.mp4';
import vid14 from '../assets/question-videos/14.mp4';
import vid15 from '../assets/question-videos/15.mp4';
import vid16 from '../assets/question-videos/16.mp4';
import vid17 from '../assets/question-videos/17.mp4';
import vid18 from '../assets/question-videos/18.mp4';
import vid19 from '../assets/question-videos/19.mp4';
import vid20 from '../assets/question-videos/20.mp4';
import vid21 from '../assets/question-videos/21.mp4';
import vid22 from '../assets/question-videos/22.mp4';
import vid23 from '../assets/question-videos/23.mp4';
import vid24 from '../assets/question-videos/24.mp4';
import vid25 from '../assets/question-videos/25.mp4';
import vid26 from '../assets/question-videos/26.mp4';
import vid27 from '../assets/question-videos/27.mp4';
import vid28 from '../assets/question-videos/28.mp4';
import vid29 from '../assets/question-videos/29.mp4';
import vid30 from '../assets/question-videos/30.mp4';
import vid31 from '../assets/question-videos/31.mp4';
import vid32 from '../assets/question-videos/32.mp4';
import vid33 from '../assets/question-videos/33.mp4';
import vid34 from '../assets/question-videos/34.mp4';
import vid35 from '../assets/question-videos/35.mp4';
import vid36 from '../assets/question-videos/36.mp4';
import vid37 from '../assets/question-videos/37.mp4';
import vid38 from '../assets/question-videos/38.mp4';
import vid39 from '../assets/question-videos/39.mp4';
import vid40 from '../assets/question-videos/40.mp4';

const videoMap = {
  1: vid1,
  2: vid2,
  3: vid3,
  4: vid4,
  5: vid5,
  6: vid6,
  7: vid7,
  8: vid8,
  9: vid9,
  10: vid10,
  11: vid11,
  12: vid12,
  13: vid13,
  14: vid14,
  15: vid15,
  16: vid16,
  17: vid17,
  18: vid18,
  19: vid19,
  20: vid20,
  21: vid21,
  22: vid22,
  23: vid23,
  24: vid24,
  25: vid25,
  26: vid26,
  27: vid27,
  28: vid28,
  29: vid29,
  30: vid30,
  31: vid31,
  32: vid32,
  33: vid33,
  34: vid34,
  35: vid35,
  36: vid36,
  37: vid37,
  38: vid38,
  39: vid39,
  40: vid40,
  41: joelVid
};

const SearchResults = ({ query, onBack, onVideoSelect }) => {
  const [prediction, setPrediction] = useState('Loading...');
  const [loadingPrediction, setLoadingPrediction] = useState(true);
  const [loadingRecommendation, setLoadingRecommendation] = useState(false);
  const [aiRecommendation, setAiRecommendation] = useState('');
  const [videoIds, setVideoIds] = useState([]);
  const [hasFetchedVideos, setHasFetchedVideos] = useState(false);
  const openai = new OpenAI({ apiKey: import.meta.env.VITE_OPENAI_API_KEY, dangerouslyAllowBrowser: true });

  useEffect(() => {
    if (query) {
      const fetchPrediction = async () => {
        try {
          setLoadingPrediction(true);
          setAiRecommendation('');  // Clear previous recommendation
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

          // Make API call to http://127.0.0.1:8000/query
          const queryResponse = await axios.post('http://127.0.0.1:8000/query', {
            text: recommendation,
            top_x: 5
          });

          // Extract video IDs from the API response
          const videoData = queryResponse.data;
          const ids = videoData.map(video => video.id).concat(41);
          setVideoIds(ids);
        } catch (error) {
          console.error('Error fetching AI recommendation or video IDs:', error);
          setAiRecommendation('Error fetching AI recommendation');
          setVideoIds([]);
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
        <FontAwesomeIcon className="search-icon" icon={faSearch} />
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
            <p>
              <img src={tiktokStar} alt="Description" className="tiktok-star" />
              <img src={tiktokAI} alt="Description" className="tiktok-ai" />
            </p>
            <p>
              {loadingPrediction
                ? "Loading prediction..."
                : prediction === 'Question'
                ? loadingRecommendation
                  ? "Your query has been identified to be a question, loading recommendations"
                  : aiRecommendation
                : "Your query is not a question, so no specific AI recommendations are displayed"}
            </p>
            <div className="result-items">
              {videoIds.map(id => (
                <div className="result-item" key={id} onClick={() => onVideoSelect(videoMap[id])}>
                  <video controls={false} width="250">
                    <source src={videoMap[id]} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                  <div className="description">Result {id}</div>
                </div>
              ))}
            </div>
            <p className="disclaimer">Always verify important information.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchResults;
