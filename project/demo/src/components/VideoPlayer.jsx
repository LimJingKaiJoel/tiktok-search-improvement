import { useRef } from 'react';
import './VideoPlayer.css';
import video from '../assets/video.mp4'

const VideoPlayer = () => {
    const videoRef = useRef(null);
  
    const handleVideoClick = () => {
      if (videoRef.current.paused) {
        videoRef.current.play();
      } else {
        videoRef.current.pause();
      }
    };
  
    return (
      <video
        className="phone-video"
        autoPlay
        loop
        muted
        ref={videoRef}
        onClick={handleVideoClick}
      >
        <source src={video} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    );
  };
  
  export default VideoPlayer;