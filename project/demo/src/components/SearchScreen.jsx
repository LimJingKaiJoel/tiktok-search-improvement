import { useState } from 'react';
import './SearchScreen.css';

const SearchScreen = ({ onClose, onSubmit }) => {
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

  return (
    <div className="search-screen">
      <div className="search-bar">
        <button className="back-button" onClick={onClose}>←</button>
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
          <li>Lego Filter 🔥</li>
          <li>Programming</li>
          <li>TikTok TechJam 🔥</li>
          <li>Singapore City</li>
          <li>Best Cafe In Singapore</li>
        </ul>
      </div>
    </div>
  );
};

export default SearchScreen;
