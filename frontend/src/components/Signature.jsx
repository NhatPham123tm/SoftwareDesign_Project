import React, { useRef, useState, useEffect } from 'react';
import SignaturePad from 'react-signature-canvas';
import './Form.css';

const Signature = ({ onSave, onClear, initialSignature, label, width = 300, height = 150 }) => {
  const signaturePadRef = useRef(null);
  const [signatureData, setSignatureData] = useState(initialSignature || null);

  useEffect(() => {
    if (initialSignature) {
      signaturePadRef.current.fromDataURL(initialSignature);
    }
  }, [initialSignature]);

  const handleSave = () => {
    const data = signaturePadRef.current.toDataURL();
    setSignatureData(data);
    if (onSave) onSave(data);
  };

  const handleClear = () => {
    signaturePadRef.current.clear();
    setSignatureData(null);
    if (onClear) onClear();
  };

  return (
    <div className="signature-wrapper">
      <div className="signature-pad-container">
        <label>{label}</label>
        <div className="signature-pad">
          <SignaturePad
            ref={signaturePadRef}
            canvasProps={{
              width: width,
              height: height,
              className: 'signature-canvas'
            }}
          />
        </div>
        <button type="button" onClick={handleClear} className="clear-btn">Clear</button>
      </div>
      <div className="signature-buttons">
        <button onClick={handleSave} className="large-save-btn">
          Save Signature and Submit
        </button>
      </div>
      {signatureData && (
        <div className="signature-preview">
          <img 
            src={signatureData} 
            alt="signature preview" 
            style={{ maxWidth: '100%', maxHeight: '70px' }} 
          />
        </div>
      )}
    </div>
  );
};

export default Signature;