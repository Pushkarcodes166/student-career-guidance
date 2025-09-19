import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000';

const questions = [
  { id: 'q1_enjoy_subject', text: 'Which subject do you enjoy the most?', options: ['Maths', 'Physics', 'Chemistry', 'Biology', 'English'] },
  { id: 'q4_math_performance', text: 'How would you rate your performance in Mathematics?', options: ['Poor', 'Average', 'Good', 'Excellent'] },
  { id: 'q5_bio_performance', text: 'How would you rate your performance in Biology?', options: ['Poor', 'Average', 'Good', 'Excellent'] },
  { id: 'q6_tech_interest', text: 'Do you enjoy working with machines, software, or technology?', options: ['Yes', 'No'] },
  { id: 'q7_medicine_interest', text: 'Do you have interest in helping and treating people?', options: ['Yes', 'No'] },
  { id: 'q8_design_interest', text: 'Do you like designing and creating structures (architecture/design)?', options: ['Yes', 'No'] },
  { id: 'q9_research_interest', text: 'Do you enjoy scientific experiments and research?', options: ['Yes', 'No'] },
  { id: 'q14_coding_interest', text: 'Do you enjoy coding and software-related tasks?', options: ['Yes', 'No'] },
  { id: 'q15_creative_interest', text: 'Do you like working on creative projects (art/design)?', options: ['Yes', 'No'] },
];

function Questionnaire() {
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setAnswers(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (Object.keys(answers).length < questions.length) {
      alert('Please answer all the questions.');
      return;
    }
    setLoading(true);
    setError('');
    setResults([]);
    try {
      const response = await axios.post(`${API_URL}/predict`, answers);
      setResults(response.data);
    } catch (err) {
      setError('Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getTrophyIcon = (index) => {
    if (index === 0) return <i className='bx bxs-trophy' style={{color: '#FFD700'}}></i>; // Gold
    if (index === 1) return <i className='bx bxs-trophy' style={{color: '#C0C0C0'}}></i>; // Silver
    if (index === 2) return <i className='bx bxs-trophy' style={{color: '#CD7F32'}}></i>; // Bronze
    return null;
  };

  return (
    <div>
      <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>AI Career Prediction</h2>
      <form onSubmit={handleSubmit} className="questionnaire-form">
        {questions.map((q, index) => (
          <div key={q.id} className="form-group">
            <label htmlFor={q.id}>{index + 1}. {q.text}</label>
            <select name={q.id} id={q.id} onChange={handleInputChange} required defaultValue="">
              <option value="" disabled>Select an option</option>
              {q.options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
            </select>
          </div>
        ))}
        <button type="submit" className="button" style={{width: '100%', justifyContent: 'center'}} disabled={loading}>
          {loading ? 'Analyzing...' : 'Get My Career Prediction'}
          <i className='bx bx-right-arrow-alt'></i>
        </button>
      </form>

      {error && <p style={{ color: 'red', textAlign: 'center', marginTop: '1rem' }}>{error}</p>}
      
      {results.length > 0 && (
        <div className="prediction-result">
          <h3>Your Top 3 Recommendations:</h3>
          {results.map((result, index) => (
            <div key={index} className="prediction-item">
              <span className="career-name">
                {getTrophyIcon(index)}
                {result.career}
              </span>
              <span className="confidence-score">{result.score}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Questionnaire;