import React, { useState } from 'react';
import './PhoneComponent.css';
import NavigationBar from './NavigationBar';
import VideoPlayer from './VideoPlayer';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import SearchScreen from './SearchScreen';
import SearchResults from './SearchResults';


const PhoneComponent = () => {
  const [screen, setScreen] = useState('home'); // 'home', 'search', 'results'
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearchClick = () => {
    setScreen('search');
  };

  const handleCloseSearch = () => {
    setScreen('home');
  };

  const handleSearchSubmit = (query) => {
    setSearchQuery(query);
    setScreen('results');
  };

  const handleBackFromResults = () => {
    setScreen('search');
  };

  return (
    <div className="phone-container">
      <div className="phone">
        <div className="phone-screen">
          {screen === 'search' ? (
            <SearchScreen onClose={handleCloseSearch} onSubmit={handleSearchSubmit} />
          ) : screen === 'results' ? (
            <SearchResults query={searchQuery} onBack={handleBackFromResults} />
          ) : (
            <>
              <TopBar onSearchClick={handleSearchClick} />
              <VideoPlayer />
              <Sidebar />
              <NavigationBar />
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default PhoneComponent;
