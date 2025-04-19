import React from "react";
import './Modal.css';

const Modal = ( { children, modal, setModal }) => {
    const toggleModal = () => {
        setModal(!modal)
    };

    return (
        modal && (
            <div className="modal">
                <div onClick={() => toggleModal()} className="overlay"></div>
                <div className="modal-content">
                    {children}
                    <button className="close-modal" onClick={() => toggleModal()}>Close</button>
                </div>
            </div>
        )
    )
}

export default Modal;