import React, { useState } from 'react';
import axios from 'axios'; 
import { FiSend, FiUpload } from 'react-icons/fi'; 
import { server_api } from '../server_api';
import Logo from '../assests/logo.svg';
import Clogo from "../assests/clogo.svg"
import Qlogo from "../assests/qlogo.svg"


function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [typingAnswer, setTypingAnswer] = useState(null);
  const [pdfFile, setPdfFile] = useState(null);
  const [pdfName, setPdfName] = useState('');
  const [file, setfile] = useState(null)


  const handleSend = async () => {
    if (!input.trim()) return;

    const question = input;
    setMessages([...messages, { type: 'question', text: question }]);
    setInput('');

    try {
      const response = await axios.post(`${server_api}/question`, {
        question,
      });
      const data = response.data;
      console.log(data)

      displayTypingAnswer(data.answer);
    } catch (error) {
      console.error('Error sending question:', error);
    }
  };


  const displayTypingAnswer = (answer) => {
    setTypingAnswer('');
    let words = answer.split(' ');
    let index = 0;

    const typingInterval = setInterval(() => {
      if (index < words.length) {
        setTypingAnswer((prev) => (prev ? prev + ' ' + words[index] : words[index]));
        index++;
      } else {
        clearInterval(typingInterval);
        setMessages((prevMessages) => [
          ...prevMessages,
          { type: 'answer', text: answer },
        ]);
        setTypingAnswer(null);
      }
    }, 200); 
  };

  
  const handlePdfChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setPdfFile(file);
      setPdfName(file.name); 
    } else {
      alert('Please select a PDF file');
    }
  };

  
  const handlePdfUpload = async () => {
    if (pdfFile) {
      const formData = new FormData();
      formData.append('file', pdfFile);

      try {
        const response = await axios.post(`${server_api}/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        if (response.status === 200) {
          const data = response.data;
     
          console.log(data)
          setfile(data)
          alert(`${data.file_name} has beed uploaded`)
         
        }
      } catch (error) {
        console.error('Error uploading PDF:', error);
        alert('Failed to upload PDF');
      }
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-between ">
  {/* Top Bar */}
  <div className="w-full flex items-center justify-between p-4 bg-white shadow-md">
    <div className="text-xl font-bold text-gray-800"><img src={Logo} alt="Your Logo" className="w-50 h-50" /></div>
    <div className="flex items-center space-x-2">
      {/* Upload PDF Icon */}
      <label htmlFor="file-upload" className="cursor-pointer">
        <FiUpload size={24} className="text-blue-600 hover:text-blue-700" />
      </label>
      <input
        id="file-upload"
        type="file"
        accept=".pdf"
        onChange={handlePdfChange}
        className="hidden"
      />
      {pdfFile && <a href={file?.file_url} target="_blank" rel="noopener noreferrer">
  <span className="text-sm text-gray-700">{pdfName}</span>
</a>
}
      {pdfFile && (
        <button
          onClick={handlePdfUpload}
          className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          Upload
        </button>
      )}
    </div>
  </div>

  {/* Messages Container */}
  <div className="flex-1 w-2/3 overflow-y-auto p-6 space-y-10 bg-white mt-4">
    {messages.map((message, index) => (
      <div key={index} className="flex items-start space-x-4">
        {/* Circular Logo */}
        {
          message.type ==='answer'? (
            <div className="w-10 h-8 rounded-full flex-shrink-0"><img src={Clogo} alt="Your Logo"/></div>
          ):(
            <div className="w-10 h-8 rounded-full flex-shrink-0"><img src={Qlogo} alt="Your Logo"/></div>
          )
        }
  
        <div
          className={`p-3 rounded-lg text-sm text-gray-900 ${
            message.type === 'question'
              ? 'bg-white bg-opacity-70'
              : message.type === 'answer'
              ? 'bg-white bg-opacity-70'
              : 'bg-green-100 bg-opacity-70'
          }`}
          style={{ maxWidth: '80%' }}
        >
          {message.text}
        </div>
      </div>
    ))}

    {/* Typing Answer (Animated) */}
    {typingAnswer && (
      <div className="flex items-start space-x-4">
        <div className="w-8 h-8 bg-blue-500 rounded-full flex-shrink-0"></div>
        <div
          className="p-3 rounded-lg bg-gray-200 bg-opacity-70 text-sm text-gray-900"
          style={{ maxWidth: '80%' }}
        >
          {typingAnswer}
        </div>
      </div>
    )}
  </div>

  {/* Full-Width Input Bar */}
  <div className="w-full p-4 bg-white shadow-md flex justify-center mt-4">
    <div className="relative flex items-center w-2/3 py-10">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask a question..."
        className="w-full px-4 py-2 border border-gray-100 rounded-sm shadow-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <button
        onClick={handleSend}
        className="absolute right-2 text-blue-600 hover:text-blue-700"
      >
        <FiSend size={24} />
      </button>
    </div>
  </div>
</div>

  );
}

export default Home;
