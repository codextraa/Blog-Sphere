// components/ErrorAlert.js
// import React, { useState } from 'react';
// import styles from './ErrorAlert.module.css'; // Optional: for custom styles

// const ErrorAlert = ({ message, onClose }) => {
//   const [visible, setVisible] = useState(true);

//   const handleClose = () => {
//     setVisible(false);
//     onClose(); // Call the onClose prop to notify the parent component
//   };

//   if (!visible) return null;

//   return (
//     <div className={styles.alert}>
//       <span>{message}</span>
//       <button onClick={handleClose} className={styles.closeButton}>
//         &times; {/* Cross icon */}
//       </button>
//     </div>
//   );
// };

// export default ErrorAlert;