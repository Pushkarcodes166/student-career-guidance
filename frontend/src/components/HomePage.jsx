import React from 'react';

function HomePage({ setView }) {
  return (
    <div className="home-page">
      <h2>Find Your Future Path</h2>
      <div className="mode-selection">
        <div className="mode-card" onClick={() => setView('questionnaire')}>
          <i className='bx bxs-brain'></i>
          <h3>AI-Powered Prediction</h3>
          <p>Answer a few questions and let our AI suggest the best career paths for you.</p>
        </div>
        <div className="mode-card" onClick={() => setView('explorer')}>
          <i className='bx bxs-flask'></i>
          <h3>Explore Science Careers</h3>
          <p>Browse a detailed directory of science-stream careers and their roadmaps.</p>
        </div>
      </div>
    </div>
  );
}

export default HomePage;