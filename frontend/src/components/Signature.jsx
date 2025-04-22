import React, { useRef, useState, useEffect } from 'react';
import SignaturePad from 'react-signature-canvas';
import './Form.css';

const Signature = ({ onSave, onClear, initialSignature, label }) => {
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
        <SignaturePad ref={signaturePadRef} />

        <button type="button" onClick={handleClear} className="clear-btn">Clear</button>
      </div>

      <div className="signature-buttons">
        <button onClick={handleSave} className="large-save-btn">
          Save Signature and Submit
        </button>
      </div>

      {signatureData && <img src={signatureData} alt="signature preview" />}
    </div>
  );
};

export default Signature;