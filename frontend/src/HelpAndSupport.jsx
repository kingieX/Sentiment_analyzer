// import React from 'react';
import { useNavigate, Link } from "react-router-dom";

const HelpAndSupport = () => {
    const Navigate = useNavigate();

    const handleClick = () => {
        Navigate('/');
    }
    
    const back = "◄ Back"
  return (
    <div className="left h-full py-2">
        <h1 onClick={handleClick} className='text-green-600 text-3xl m-2 font-bold'>Sentiment Analyzer</h1>
        <div className="border border-gray-500 mb-2"></div>
        <span>
            <Link className="text-white" to="/">
                <p className="ml-4 hover:underline">{back}</p>
            </Link>
        </span>

        <div className="px-8 py-4 text-white">
            <h1 className="text-3xl font-bold mb-4">Help & Support</h1>

            <div className="mb-8">
                <h2 className="text-xl font-semibold mb-2">Frequently Asked Questions (FAQ)</h2>
                <ul>
                <li className="mb-4">
                    <span className="font-semibold">Q:</span> How does the sentiment analysis work?
                    <br />
                    <span className="ml-4">A: The sentiment analysis algorithm analyzes text and determines whether it expresses positive, negative, or neutral sentiment.</span>
                </li>

                <li className="mb-4">
                    <span className="font-semibold">Q:</span> Is the sentiment analysis accurate?
                    <br />
                    <span className="ml-4">A: While we strive for accuracy, sentiment analysis is subjective and may vary based on language nuances and context.</span>
                </li>

                <li className="mb-4">
                    <span className="font-semibold">Q:</span> Can I analyze multiple sentences at once?
                    <br />
                    <span className="ml-4">A: Currently, the analyzer processes one sentence at a time. You can make separate requests for each sentence.</span>
                </li>

                <li className="mb-4">
                    <span className="font-semibold">Q:</span> How often is the sentiment model updated?
                    <br />
                    <span className="ml-4">A: We continuously strive to improve our models, and updates may occur periodically.</span>
                </li>

                {/* Add more FAQ items as needed */}
                </ul>
            </div>

            <div className="mb-8">
                <h2 className="text-xl font-semibold mb-2">Contact Us</h2>
                <p>
                If you have any questions or need assistance, please feel free to contact our support team at{' '}
                <a href="mailto:chimakingsley216@gmail.com" className="text-blue-500">support@SentimentAnalyzer.com</a>.
                </p>
            </div>

            <div>
                <h2 className="text-xl font-semibold mb-2">Feedback</h2>
                <p>
                We appreciate your feedback! If you have any suggestions or want to report an issue, please use our{' '}
                <a href="#" className="text-blue-500">Feedback Form</a>.
                </p>
            </div>
            <div className="text-center text-xl mt-4 font-semibold">
                <p>Created by Slanconcept ©2024</p>
            </div>
        </div>
    </div>
  );
};

export default HelpAndSupport;
