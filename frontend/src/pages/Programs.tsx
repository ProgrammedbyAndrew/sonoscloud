import { useEffect, useState } from 'react';
import { Music, Play, Volume2, RefreshCw, Filter } from 'lucide-react';
import { Card, CardHeader, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { api } from '../api/client';
import type { Program } from '../types';
import { clsx } from 'clsx';

const TYPE_COLORS: Record<string, string> = {
  ad: 'bg-purple-900/50 border-purple-600',
  fm: 'bg-green-900/50 border-green-600',
  sm: 'bg-blue-900/50 border-blue-600',
  parking: 'bg-yellow-900/50 border-yellow-600',
  TIGS: 'bg-pink-900/50 border-pink-600',
  adfire: 'bg-red-900/50 border-red-600',
  fireparking: 'bg-orange-900/50 border-orange-600',
  pause: 'bg-gray-800/50 border-gray-600',
};

// Updated with correct names
const TYPE_LABELS: Record<string, string> = {
  ad: 'Business Ads',
  fm: 'Music',
  sm: 'Social Media Ads',
  parking: 'Parking Announcements',
  TIGS: 'Gift Shop Ads',
  adfire: 'Fire Show Ads',
  fireparking: 'Fire Show Parking',
  pause: 'Pause',
};

export function Programs() {
  const [programs, setPrograms] = useState<Program[]>([]);
  const [selectedType, setSelectedType] = useState<string>('all');
  const [loading, setLoading] = useState(true);
  const [playingProgram, setPlayingProgram] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const programsData = await api.getPrograms();
      setPrograms(programsData.available_scripts as Program[]);
    } catch (error) {
      console.error('Error fetching programs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handlePlayProgram = async (programName: string) => {
    setPlayingProgram(programName);
    try {
      await api.runProgram(programName);
    } catch (error) {
      console.error('Error playing program:', error);
    } finally {
      setTimeout(() => setPlayingProgram(null), 2000);
    }
  };

  // Group programs by type
  const groupedPrograms = programs.reduce((acc, program) => {
    const type = program.program_type;
    if (!acc[type]) acc[type] = [];
    acc[type].push(program);
    return acc;
  }, {} as Record<string, Program[]>);

  // Sort each group by volume
  Object.keys(groupedPrograms).forEach((type) => {
    groupedPrograms[type].sort((a, b) => a.volume - b.volume);
  });

  // Get unique types
  const types = Object.keys(groupedPrograms).sort();

  const filteredTypes = selectedType === 'all' ? types : [selectedType];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-orange-500" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Program Library</h1>
          <p className="text-gray-400">{programs.length} programs available</p>
        </div>
        <Button variant="ghost" size="sm" onClick={fetchData}>
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* Type Filter */}
      <Card>
        <CardContent className="py-3">
          <div className="flex items-center gap-3 overflow-x-auto">
            <Filter className="w-5 h-5 text-gray-500" />
            <button
              onClick={() => setSelectedType('all')}
              className={clsx(
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
                selectedType === 'all'
                  ? 'bg-orange-500 text-white'
                  : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
              )}
            >
              All ({programs.length})
            </button>
            {types.map((type) => (
              <button
                key={type}
                onClick={() => setSelectedType(type)}
                className={clsx(
                  'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
                  selectedType === type
                    ? 'bg-orange-500 text-white'
                    : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                )}
              >
                {TYPE_LABELS[type] || type} ({groupedPrograms[type]?.length || 0})
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Program Groups */}
      <div className="space-y-6">
        {filteredTypes.map((type) => {
          const typePrograms = groupedPrograms[type] || [];
          if (typePrograms.length === 0) return null;

          return (
            <Card
              key={type}
              className={clsx('border-l-4', TYPE_COLORS[type] || 'border-gray-600')}
            >
              <CardHeader>
                <div className="flex items-center gap-2">
                  <Music className="w-5 h-5 text-orange-500" />
                  <h2 className="font-semibold">{TYPE_LABELS[type] || type}</h2>
                  <Badge variant="info">{typePrograms.length} programs</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-3">
                  {typePrograms.map((program) => (
                    <button
                      key={program.name}
                      onClick={() => handlePlayProgram(program.name)}
                      disabled={playingProgram === program.name}
                      className={clsx(
                        'flex flex-col items-center p-4 rounded-lg border transition-all',
                        'bg-gray-800 border-gray-700 hover:border-orange-500 hover:bg-gray-750',
                        playingProgram === program.name && 'border-green-500 bg-green-900/20'
                      )}
                    >
                      <div className="flex items-center gap-2 mb-2">
                        <Volume2 className="w-5 h-5 text-gray-400" />
                        <span className="text-2xl font-bold">{program.volume}</span>
                      </div>
                      <span className="text-sm text-gray-400">
                        {program.name.replace('.py', '')}
                      </span>
                      {playingProgram === program.name ? (
                        <Badge variant="success" className="mt-2">
                          Playing...
                        </Badge>
                      ) : (
                        <Play className="w-4 h-4 mt-2 text-gray-500" />
                      )}
                    </button>
                  ))}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Volume Legend */}
      <Card>
        <CardHeader>
          <h2 className="font-semibold">Volume Guide</h2>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded bg-gray-700 flex items-center justify-center font-bold">50</span>
              <span className="text-gray-400">Quiet - Late night</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded bg-gray-700 flex items-center justify-center font-bold">65</span>
              <span className="text-gray-400">Low - Background</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded bg-gray-700 flex items-center justify-center font-bold">75</span>
              <span className="text-gray-400">Medium - Default</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-8 h-8 rounded bg-gray-700 flex items-center justify-center font-bold">85</span>
              <span className="text-gray-400">High - Announcements</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
