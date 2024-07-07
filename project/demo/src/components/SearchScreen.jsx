import { useState } from 'react';
import './SearchScreen.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faSearch } from '@fortawesome/free-solid-svg-icons';

const suggestions = [
  'How Do I Win A Hackathon 🔥',
  'Cute Dogs',
  'TikTok TechJam',
  'What Is The Most Beautiful Country 🔥',
  'Best Cafe In Singapore',
  'Where Do I Learn To Program 🔥'
];

const SearchScreen = ({ onBack, onSubmit }) => {
  const [query, setQuery] = useState('');

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSearch = () => {
    if (query.trim() === '') {
      return;
    }
    onSubmit(query);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleSuggestionClick = (suggestion) => {
    const cleanedQuery = suggestion.replace(/🔥/g, '').trim();
    onSubmit(cleanedQuery);
  };

  return (
    <div className="search-screen">
      <div className="search-bar">
        <FontAwesomeIcon className="back-button" icon={faArrowLeft} onClick={onBack}/>
        <FontAwesomeIcon className="search-icon" icon={faSearch} />
        <input
          type="text"
          placeholder="Search"
          value={query}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
        />
        <button
          className={`search-button ${query.trim() === '' ? 'disabled' : ''}`}
          onClick={handleSearch}
        >
          Search
        </button>
      </div>
      <div className="suggestions">
        <h3>You may like</h3>
        <ul>
          {suggestions.map((suggestion, index) => (
            <li key={index} onClick={() => handleSuggestionClick(suggestion)}>
              {suggestion}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default SearchScreen;
