import { useState } from 'react';
import { Lock, X } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { Button } from './ui/Button';

interface LoginModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function LoginModal({ isOpen, onClose }: LoginModalProps) {
  const [pin, setPin] = useState('');
  const [error, setError] = useState(false);
  const { login } = useAuth();

  if (!isOpen) return null;

  const handleDigit = (digit: string) => {
    if (pin.length < 4) {
      const newPin = pin + digit;
      setPin(newPin);
      setError(false);

      // Auto-submit when 4 digits entered
      if (newPin.length === 4) {
        if (login(newPin)) {
          setPin('');
          setError(false);
          onClose();
        } else {
          setError(true);
          setPin('');
        }
      }
    }
  };

  const handleBackspace = () => {
    setPin(pin.slice(0, -1));
    setError(false);
  };

  const handleClear = () => {
    setPin('');
    setError(false);
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-[100] p-4">
      <div className="bg-gray-900 rounded-2xl p-6 w-full max-w-sm border border-gray-700 shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-orange-500/20 rounded-lg">
              <Lock className="w-6 h-6 text-orange-500" />
            </div>
            <div>
              <h2 className="text-lg font-bold">Admin Login</h2>
              <p className="text-sm text-gray-400">Enter 4-digit PIN</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* PIN Display */}
        <div className="flex justify-center gap-3 mb-6">
          {[0, 1, 2, 3].map((i) => (
            <div
              key={i}
              className={`w-12 h-14 rounded-lg border-2 flex items-center justify-center text-2xl font-bold transition-colors ${
                error
                  ? 'border-red-500 bg-red-500/10'
                  : pin[i]
                  ? 'border-orange-500 bg-orange-500/10'
                  : 'border-gray-700 bg-gray-800'
              }`}
            >
              {pin[i] ? '*' : ''}
            </div>
          ))}
        </div>

        {/* Error Message */}
        {error && (
          <p className="text-center text-red-400 text-sm mb-4">
            Incorrect PIN. Try again.
          </p>
        )}

        {/* Number Pad */}
        <div className="grid grid-cols-3 gap-3">
          {['1', '2', '3', '4', '5', '6', '7', '8', '9', 'C', '0', '<'].map((key) => (
            <button
              key={key}
              onClick={() => {
                if (key === 'C') handleClear();
                else if (key === '<') handleBackspace();
                else handleDigit(key);
              }}
              className={`h-14 rounded-lg text-xl font-semibold transition-colors ${
                key === 'C'
                  ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                  : key === '<'
                  ? 'bg-gray-700 hover:bg-gray-600 text-gray-300'
                  : 'bg-gray-800 hover:bg-gray-700 text-white'
              }`}
            >
              {key === '<' ? '←' : key}
            </button>
          ))}
        </div>

        {/* Cancel Button */}
        <Button
          variant="ghost"
          onClick={onClose}
          className="w-full mt-4"
        >
          Cancel
        </Button>
      </div>
    </div>
  );
}
