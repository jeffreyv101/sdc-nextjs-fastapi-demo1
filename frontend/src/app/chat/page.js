"use client";
import { useState, useEffect } from "react";
import Header from "@/components/header";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function getChatMessages() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/ai-chat/messages`);
        if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data.messages;

    } catch (error) {
        console.error('Error fetching messages:', error);
        throw error;
    }
}

async function sendMessage(message) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/ai-chat/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: message }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
}

export default function ChatPage() {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [inputMessage, setInputMessage] = useState("");
    const [sending, setSending] = useState(false);
    const [loadingDots, setLoadingDots] = useState("");

    useEffect(() => {
        async function fetchMessages() {
            try {
                const fetchedMessages = await getChatMessages();
                setMessages(fetchedMessages || []);
            } catch (error) {
                console.error('Failed to fetch messages:', error);
                setMessages([]);
            } finally {
                setLoading(false);
            }
        }

        fetchMessages();
    }, []);

    useEffect(() => {
        const intervalId = setInterval(() => {
            if (loadingDots.length >= 3){
                setLoadingDots("")
            } else{
                setLoadingDots((prevState) => (prevState + "."));
            }
        }, 500); // Adjust speed (milliseconds)

        return () => clearInterval(intervalId); // Cleanup on unmount
    }, [loadingDots]);

    const handleSendMessage = async (e) => {
        e.preventDefault();
        
        if (!inputMessage.trim() || sending) {
            return;
        }

        setSending(true);
        
        try {
            // Add user message to local state immediately for better UX
            const userMessage = { role: "user", content: inputMessage };
            setMessages(prevMessages => [...prevMessages, userMessage]);
            
            // Clear input
            setInputMessage("");
            
            // Send message to backend
            const aiResponse = await sendMessage(inputMessage);
            
            // Add AI response to messages
            setMessages(prevMessages => [...prevMessages, aiResponse]);
            
        } catch (error) {
            console.error('Failed to send message:', error);
            // Optionally show error to user
        } finally {
            setSending(false);
        }
    };
    return (
        <>
            <Header />
            <div className="max-w-4xl mx-auto p-4">
                <h2 className="text-3xl font-bold mb-4">Chat with AI</h2>

                {/* Chat Interface */}
                <div className="border rounded-lg p-4 h-96 overflow-y-auto mb-4">
                    {/* Messages will be displayed here */}
                    {loading ? (
                        <div className="text-gray-500">Loading messages...</div>
                    ) : (
                        messages.map((message, index) => (
                            <div key={index} className={`mb-2 ${message.role === "assistant" ? "text-blue-400" : "text-gray-100"}`}>
                                <strong>{message.role === "assistant" ? "AI" : "You"}:</strong> {message.content}
                            </div>
                        ))
                    )}
                    {sending && <div className="flex items-center justify-center space-x-2 text-gray-600">Thinking{loadingDots}</div>}

                    {/* Input field */}
                    <form onSubmit={handleSendMessage} className="mt-4">
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={inputMessage}
                                onChange={(e) => setInputMessage(e.target.value)}
                                placeholder="Type your message..."
                                className="flex-1 border rounded-lg p-2"
                                disabled={sending}
                            />
                            <button
                                type="submit"
                                disabled={sending || !inputMessage.trim()}
                                className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed"
                            >
                                {sending ? "Sending..." : "Send"}
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </>
    );
}