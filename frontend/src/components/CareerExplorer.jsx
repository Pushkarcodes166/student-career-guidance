import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000';

const DetailSection = ({ title, icon, children }) => (
    <div className="detail-section">
        <h4><i className={`bx ${icon}`}></i> {title}</h4>
        {children}
    </div>
);

const TagList = ({ items }) => (
    <div className="tag-list">
        {items.map(item => <span key={item} className="tag">{item}</span>)}
    </div>
);

const BulletList = ({ items, icon }) => (
    <ul className="detail-list">
        {items.map((item, index) => (
            <li key={index}><i className={`bx ${icon}`}></i><span>{item}</span></li>
        ))}
    </ul>
);

const CareerCard = ({ career }) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className={`career-card ${isOpen ? 'active' : ''}`} onClick={() => setIsOpen(!isOpen)}>
            <div className="card-header">
                <h3>{career.title}</h3>
                <i className={`bx bx-chevron-down`}></i>
            </div>
            <div className="card-details">
                <DetailSection title="Description" icon="bxs-info-circle">
                    <p>{career.description}</p>
                </DetailSection>

                <DetailSection title="Eligibility" icon="bxs-user-check">
                    <p>{career.eligibility}</p>
                </DetailSection>

                <DetailSection title="Key Entrance Exams" icon="bxs-file-doc">
                    <TagList items={career.entrance_exams} />
                </DetailSection>

                <DetailSection title="Roadmap" icon="bxs-flag-alt">
                    <BulletList items={career.roadmap_steps} icon="bxs-chevrons-right" />
                </DetailSection>

                <DetailSection title="Popular Specializations" icon="bxs-star">
                    <TagList items={career.popular_specializations} />
                </DetailSection>
            </div>
        </div>
    );
};

function CareerExplorer() {
    const [careers, setCareers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchCareers = async () => {
            try {
                const response = await axios.get(`${API_URL}/career-path/science`);
                setCareers(response.data.Science.careers);
            } catch (err) {
                setError('Failed to fetch career data. Ensure the backend is running.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchCareers();
    }, []);

    if (loading) return <p>Loading career paths...</p>;
    if (error) return <p style={{ color: 'red' }}>{error}</p>;

    return (
        <div>
            <h2 style={{ textAlign: 'center', marginBottom: '2rem' }}>Explore Science Career Paths</h2>
            <div className="career-explorer-grid">
                {careers.map((career) => (
                    <CareerCard key={career.id} career={career} />
                ))}
            </div>
        </div>
    );
}

export default CareerExplorer;