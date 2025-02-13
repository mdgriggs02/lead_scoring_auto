import { Message } from '@/types';

interface ChatMessageProps {
    message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
    return (
        <div className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
                className={`max-w-[80%] p-3 rounded-lg ${message.role === 'user'
                        ? 'bg-blue-500 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
            >
                <p>{message.content}</p>
                {message.recommendations && (
                    <div className="mt-3 space-y-2">
                        {message.recommendations.map((rec, index) => (
                            <div key={index} className="p-2 bg-white rounded shadow-sm">
                                <h4 className="font-semibold">{rec.title}</h4>
                                <p className="text-sm text-gray-600">{rec.description}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
} 