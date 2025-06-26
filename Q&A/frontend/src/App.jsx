import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [imageFile, setImageFile] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [previewUrl, setPreviewUrl] = useState('');
  const [inputMethod, setInputMethod] = useState('file'); // 'file' or 'url'

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setImageUrl('');
    }
  };

  const handleUrlChange = (e) => {
    setImageUrl(e.target.value);
    setImageFile(null);
    setPreviewUrl(e.target.value);
  };

  const handleQuestionChange = (e) => {
    setQuestion(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate inputs
    if (inputMethod === 'file' && !imageFile) {
      setError('Please upload an image');
      return;
    }
    
    if (inputMethod === 'url' && !imageUrl) {
      setError('Please enter an image URL');
      return;
    }
    
    if (!question) {
      setError('Please enter a question');
      return;
    }
    
    setLoading(true);
    setError('');
    setResponse(null);
    
    try {
      const formData = new FormData();
      
      if (inputMethod === 'file') {
        formData.append('image', imageFile);
      } else {
        formData.append('image_url', imageUrl);
      }
      
      formData.append('question', question);
      
      const response = await axios.post('http://localhost:8000/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      
      setResponse(response.data);
    } catch (err) {
      console.error('Error:', err);
      setError(err.response?.data?.detail || 'An error occurred while processing your request');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Multimodal QA App</h1>
      <h2>Powered by Google Gemini 1.5 Flash</h2>
      <p>Upload an image or provide a URL and ask a question about it</p>
      
      <form onSubmit={handleSubmit}>
        <div>
          <div style={{ marginBottom: '1rem' }}>
            <label>
              <input 
                type="radio" 
                name="inputMethod" 
                value="file" 
                checked={inputMethod === 'file'} 
                onChange={() => setInputMethod('file')} 
              /> 
              Upload Image
            </label>
            <label style={{ marginLeft: '1rem' }}>
              <input 
                type="radio" 
                name="inputMethod" 
                value="url" 
                checked={inputMethod === 'url'} 
                onChange={() => setInputMethod('url')} 
              /> 
              Image URL
            </label>
          </div>

          {inputMethod === 'file' ? (
            <input
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              style={{ width: '100%' }}
            />
          ) : (
            <input
              type="text"
              placeholder="Enter image URL"
              value={imageUrl}
              onChange={handleUrlChange}
              style={{ width: '100%' }}
            />
          )}
        </div>
        
        {previewUrl && (
          <div className="image-container">
            <img src={previewUrl} alt="Preview" />
          </div>
        )}
        
        <div>
          <textarea
            placeholder="Ask a question about the image..."
            value={question}
            onChange={handleQuestionChange}
            style={{ width: '100%', minHeight: '100px' }}
          />
        </div>
        
        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Image'}
        </button>
      </form>
      
      {error && <div className="error">{error}</div>}
      
      {loading && <div style={{ marginTop: '2rem' }}><div className="loading"></div></div>}
      
      {response && (
        <div className="response-container">
          <h3>Response:</h3>
          <p>{response.answer}</p>
          <p><em>Model used: {response.model_used}</em></p>
          {response.error && <p className="error">Error: {response.error}</p>}
        </div>
      )}
    </div>
  );
}

export default App; 