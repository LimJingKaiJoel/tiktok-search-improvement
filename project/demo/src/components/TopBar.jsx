import './TopBar.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

const TopBar = ({ onSearchClick }) => {
  return (
    <div className="top-bar">
      <div className="top-bar-items">
        <div className="top-bar-item">Following</div>
        <div className="top-bar-item">Friends</div>
        <div className="top-bar-item active">For You</div>
      </div>
      <div className="top-bar-search" onClick={onSearchClick}>
        <FontAwesomeIcon icon={faSearch} />
      </div>
    </div>
  );
};

export default TopBar;
