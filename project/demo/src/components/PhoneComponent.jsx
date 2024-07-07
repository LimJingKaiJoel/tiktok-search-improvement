import React, { useState } from 'react';
import './PhoneComponent.css';
import NavigationBar from './NavigationBar';
import VideoPlayer from './VideoPlayer';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import SearchScreen from './SearchScreen';
import SearchResults from './SearchResults';
import FullScreenVideo from './FullScreenVideo';

const PhoneComponent = () => {
  const [screen, setScreen] = useState('home'); // 'home', 'search', 'results', 'fullScreenVideo'
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedVideo, setSelectedVideo] = useState(null);

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

  const handleVideoSelect = (videoSrc) => {
    setSelectedVideo(videoSrc);
    setScreen('fullScreenVideo');
  };

  const handleBackFromFullScreen = () => {
    setScreen('results');
    setSelectedVideo(null);
  };

  return (
    <div className="phone-container">
      <div className="phone">
        <div className="phone-screen">
          {screen === 'search' ? (
            <SearchScreen onBack={handleCloseSearch} onSubmit={handleSearchSubmit} />
          ) : screen === 'results' ? (
            <SearchResults query={searchQuery} onBack={handleBackFromResults} onVideoSelect={handleVideoSelect} />
          ) : screen === 'fullScreenVideo' ? (
            <FullScreenVideo videoSrc={selectedVideo} onBack={handleBackFromFullScreen} />
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
