import { useNavigate, Link } from "react-router-dom";

const AboutPage = () => {
    const Navigate = useNavigate();

    const handleClick = () => {
        Navigate('/');
    }
    
    const back = "◄ Back"

  return (
    <div className="left h-full py-2 text-white">
        <h1 onClick={handleClick} className='text-green-600 text-3xl m-2 font-bold'>Sentiment Analyzer</h1>
        <div className="border border-gray-500 mb-2"></div>
        <span>
            <Link className="text-white" to="/">
                <p className="ml-4 hover:underline">{back}</p>
            </Link>
        </span>

        <div className=" mx-8 py-4">
        <h1 className="text-3xl font-bold mb-4">About Sentiment Analyzer</h1>

        <p className="mb-4 text-lg">
            Sentiment Analyzer is a powerful tool designed to analyze the sentiment of text data. It helps users understand the emotional tone and attitude expressed in a piece of text, whether it is positive, negative, or neutral.
        </p>

        <h2 className="text-xl font-semibold mb-2">Key Features:</h2>
        <ul className="list-disc ml-6 mb-4">
            <li className="mb-2">Accurate sentiment analysis of individual sentences.</li>
            <li className="mb-2">User-friendly interface for easy interaction.</li>
            <li className="mb-2">Quick and efficient processing of text data.</li>
            <li className="mb-2">Support for various languages and contexts.</li>
        </ul>

        <h2 className="text-xl font-semibold mb-2">How It Works:</h2>
        <p className="mb-4 text-lg">
            Sentiment Analyzer uses advanced natural language processing (NLP) algorithms to analyze text and determine the sentiment expressed. The algorithm considers various linguistic factors and contextual information to provide accurate results.
        </p>

        <h2 className="text-xl font-semibold mb-2">Contact Information:</h2>
        <p className="mb-4 text-lg">
            If you have any questions, suggestions, or need assistance, please feel free to contact us at{' '}
            <a href="mailto:chimakingsley216@gmail.com" className="text-blue-500">info@sentimentanalyzer.com</a>.
        </p>

        <p className="text-lg">
            Thank you for using Sentiment Analyzer! We are committed to providing a valuable and user-friendly experience for all our users.
        </p>
        </div>
        <div className="text-center text-xl mt-4 mb-2 font-semibold">
            <p>Created by Slanconcept ©2024</p>
        </div>
    </div>
  );
};

export default AboutPage;