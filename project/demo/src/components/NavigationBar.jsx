import './NavigationBar.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faHouse, faBagShopping, faSquarePlus, faInbox, faUser } from '@fortawesome/free-solid-svg-icons';
const NavigationBar = () => {
    return (
        <div className="navbar">
          <div className="nav-item">
            <FontAwesomeIcon icon={faHouse} className="custom-icon-nav" />
            <div className="text">Home</div>
          </div>
          <div className="nav-item">
            <FontAwesomeIcon icon={faBagShopping} className="custom-icon-nav" />
            <div className="text">Shop</div>
          </div>
          <div className="nav-item">
            <FontAwesomeIcon icon={faSquarePlus} className="custom-icon-add" />
          </div>
          <div className="nav-item">
            <FontAwesomeIcon icon={faInbox} className="custom-icon-nav" />
            <div className="text">Inbox</div>
          </div>
          <div className="nav-item">
            <FontAwesomeIcon icon={faUser} className="custom-icon-nav" />
            <div className="text">Profile</div>
          </div>
        </div>
    );
};

export default NavigationBar;