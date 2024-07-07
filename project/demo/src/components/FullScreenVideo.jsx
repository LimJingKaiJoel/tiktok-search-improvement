import React from 'react';
import './FullScreenVideo.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleArrowLeft } from '@fortawesome/free-solid-svg-icons';

const FullScreenVideo = ({ videoSrc, onBack }) => {
  return (
    <div className="full-screen-video">
      <div className="back-button-video" onClick={onBack}>
        <FontAwesomeIcon icon={faCircleArrowLeft} />
      </div>
      <video controls={false} autoPlay className="video-player">
        <source src={videoSrc} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  );
};

export default FullScreenVideo;
