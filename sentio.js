import React, { useState, useEffect, useRef } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Mic, Send } from 'lucide-react';
import axios from 'axios';

const Sentio = () => {
    const [messages, setMessages] = useState([]);
    const [userMessage, setUserMessage] = useState('');
    const [listening, setListening] = useState(false);
    const chatContainerRef = useRef();

    const sendMessage = async () => {
        if (!userMessage.trim()) return;

        const userText = userMessage.trim();
        setMessages([...messages, { sender: 'User', text: userText }]);
        setUserMessage('');

        try {
            const response = await axios.post('http://localhost:5000/ask', { message: userText });
            const botResponse = response.data.response || "Sorry, I didn't understand that.";
            setMessages((prev) => [...prev, { sender: 'Sentio', text: botResponse }]);
        } catch (error) {
            console.error('Error fetching response:', error);
            setMessages((prev) => [...prev, { sender: 'Sentio', text: 'Error connecting to the server.' }]);
        }
    };

    useEffect(() => {
        chatContainerRef.current?.scrollTo(0, chatContainerRef.current.scrollHeight);
    }, [messages]);

    return (
        <div className="flex flex-col h-screen items-center bg-gray-100 p-4">
            <Card className="w-full max-w-3xl h-[80vh] p-4 mb-4 overflow-y-auto rounded-2xl shadow-lg bg-white" ref={chatContainerRef}>
                <CardContent>
                    {messages.map((msg, index) => (
                        <div key={index} className={`my-2 ${msg.sender === 'User' ? 'text-right' : 'text-left'} px-4 py-2 rounded-xl ${msg.sender === 'User' ? 'bg-blue-500 text-white ml-auto' : 'bg-gray-200 text-gray-900 mr-auto'}`}>{msg.text}</div>
                    ))}
                </CardContent>
            </Card>
            <div className="flex w-full max-w-3xl">
                <input
                    type="text"
                    className="flex-grow p-3 rounded-l-2xl shadow-sm bg-gray-100 focus:outline-none"
                    placeholder="Type a message..."
                    value={userMessage}
                    onChange={(e) => setUserMessage(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                />
                <Button className="p-3 bg-blue-600 text-white rounded-r-2xl shadow-md" onClick={sendMessage}><Send size={20} /></Button>
            </div>
        </div>
    );
};

export default Sentio;
