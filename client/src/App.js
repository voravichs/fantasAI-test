import React, { useState, useRef, useEffect } from 'react';
import './App.css'; // Import your CSS file
import Modal from 'react-modal'; // Import Modal from react-modal library

function App() {
    const [selectedVoice, setSelectedVoice] = useState('Random');
    const [userDescription, setUserDescription] = useState('');
    const [conversation, setConversation] = useState([]);
    const [petText, setPetText] = useState('');
    const [uploadedImage, setUploadedImage] = useState(null);
    const [modalIsOpen, setModalIsOpen] = useState(false); // State to manage modal open/close
    const conversationRef = useRef(null);

    useEffect(() => {
        conversationRef.current.scrollTop = conversationRef.current.scrollHeight;
    }, [conversation]);

    const handleGenerateMeditation = () => {
        fetch('http://localhost:8000/api/pet', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ voice: selectedVoice, description: userDescription, image: uploadedImage })
        })
        .then(response => response.json())
        .then(data => {
            const newConversation = [...conversation, { role: 'user', content: userDescription }, { role: 'pet', content: data.petText }];
            setConversation(newConversation);
            setPetText(data.petText);
            setUserDescription('');
            setUploadedImage(null);
            setModalIsOpen(false); // Close the modal after generating pet response
        })
        .catch(error => console.error('Error:', error));
    };

    const handleImageUpload = (event) => {
        const file = event.target.files[0];
        setUploadedImage(file);
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent default behavior of form submission
            handleGenerateMeditation();
        }
    };

    return (
        <div className="App">
            <header>
                <h1>FantasAI</h1>
            </header>
            <main>
                <div className="container">
                    <h2>Frogbert</h2>
                    <img src={uploadedImage ? URL.createObjectURL(uploadedImage) : '/Frog.gif'} alt="Pet" className="pet-image" />
                    <div className="conversation" ref={conversationRef}>
                        {conversation.map((message, index) => (
                            <div key={index} className={`message ${message.role}`}>
                                {message.content}
                            </div>
                        ))}
                    </div>
                    <div className="input-group">
                        <label htmlFor="description">Enter your prompt:</label>
                        <textarea
                            id="description"
                            rows="2"
                            value={userDescription}
                            onChange={(e) => setUserDescription(e.target.value)}
                            onKeyDown={handleKeyPress} // Call handleKeyPress on key down event
                        ></textarea>
                        <button id="generate-btn" onClick={handleGenerateMeditation}>Generate Pet Response</button>
                    </div>
                    <button onClick={() => setModalIsOpen(true)}>Create New Pet</button>
                    <Modal
                        isOpen={modalIsOpen}
                        onRequestClose={() => setModalIsOpen(false)}
                        className="custom-modal"
                        overlayClassName="custom-overlay"
                    >
                        <h2>Upload Your Pet's Image</h2>
                        <input type="file" accept="image/*" onChange={handleImageUpload} />
                        <button onClick={() => setModalIsOpen(false)}>Done</button>
                    </Modal>
                </div>
            </main>
        </div>
    );
}

export default App;
