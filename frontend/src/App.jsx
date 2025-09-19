import React, { useState } from 'react';
import HomePage from './components/HomePage';
import Questionnaire from './components/Questionnaire';
import CareerExplorer from './components/CareerExplorer';

function App() {
  const [view, setView] = useState('home'); // 'home', 'questionnaire', 'explorer'

  const renderView = () => {
    switch (view) {
      case 'questionnaire':
        return <Questionnaire />;
      case 'explorer':
        return <CareerExplorer />;
      default:
        return <HomePage setView={setView} />;
    }
  };

  return (
    <div className="container">
      <header className="app-header">
        <h1>🎓 Career Compass</h1>
        {view !== 'home' && (
          <button className="button button-secondary" onClick={() => setView('home')}>
            <i className='bx bx-arrow-back'></i>
            Back to Home
          </button>
        )}
      </header>
      <main>
        {renderView()}
      </main>
    </div>
  );
}

export default App;