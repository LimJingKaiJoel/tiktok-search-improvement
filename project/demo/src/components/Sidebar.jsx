import './Sidebar.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleUser ,faHeart, faMessage, faBookmark, faShareSquare } from '@fortawesome/free-regular-svg-icons';

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-item">
        <FontAwesomeIcon icon={faCircleUser} className="custom-icon-profile" />
      </div>
      <div className="sidebar-item">
        <FontAwesomeIcon icon={faHeart} className="custom-icon" />
        <div className="text">35.4K</div>
      </div>
      <div className="sidebar-item">
        <FontAwesomeIcon icon={faMessage} className="custom-icon" />
        <div className="text">355</div>
      </div>
      <div className="sidebar-item">
        <FontAwesomeIcon icon={faBookmark} className="custom-icon" />
        <div className="text">2,092</div>
      </div>
      <div className="sidebar-item">
        <FontAwesomeIcon icon={faShareSquare} className="custom-icon" />
      </div>
    </div>
  );
};

export default Sidebar;
