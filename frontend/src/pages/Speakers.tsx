import { useEffect, useState } from 'react';
import { Speaker as SpeakerIcon, Volume2, RefreshCw, Link2, Wifi, Flame } from 'lucide-react';
import { Card, CardHeader, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Slider } from '../components/ui/Slider';
import { api } from '../api/client';
import type { Speaker, SpeakerLayout } from '../types';
import { clsx } from 'clsx';

export function Speakers() {
  const [speakers, setSpeakers] = useState<Speaker[]>([]);
  const [layout, setLayout] = useState<SpeakerLayout | null>(null);
  const [loading, setLoading] = useState(true);
  const [masterVolume, setMasterVolume] = useState(75);
  const [speakerVolumes, setSpeakerVolumes] = useState<Record<string, number>>({});
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const [speakersData, layoutData] = await Promise.all([
        api.getSpeakers(),
        api.getSpeakerLayout(),
      ]);
      const speakersList = speakersData as Speaker[];
      setSpeakers(speakersList);
      setLayout(layoutData as SpeakerLayout);

      // Initialize volumes from speaker data
      const volumes: Record<string, number> = {};
      speakersList.forEach((s) => {
        volumes[s.name] = s.volume ?? 75;
      });
      setSpeakerVolumes(volumes);
    } catch (error) {
      console.error('Error fetching speakers:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // Auto-refresh every 5 seconds
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleGroupAll = async () => {
    setActionLoading('group');
    try {
      await api.groupAllSpeakers();
      await fetchData();
    } catch (error) {
      console.error('Error grouping speakers:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const handleSetMasterVolume = async () => {
    setActionLoading('volume');
    try {
      await api.setAllSpeakersVolume(masterVolume);
      // Update local state
      const newVolumes: Record<string, number> = {};
      speakers.forEach((s) => {
        newVolumes[s.name] = masterVolume;
      });
      setSpeakerVolumes(newVolumes);
      await fetchData();
    } catch (error) {
      console.error('Error setting volume:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const handleSetSpeakerVolume = async (speakerName: string) => {
    setActionLoading(speakerName);
    try {
      const volume = speakerVolumes[speakerName] ?? 75;
      await api.setSpeakerVolume(speakerName, volume);
      await fetchData();
    } catch (error) {
      console.error(`Error setting volume for ${speakerName}:`, error);
    } finally {
      setActionLoading(null);
    }
  };

  const handleSpeakerVolumeChange = (speakerName: string, volume: number) => {
    setSpeakerVolumes((prev) => ({
      ...prev,
      [speakerName]: volume,
    }));
  };

  const getSpeakerByName = (name: string) => {
    return speakers.find((s) => s.name === name);
  };

  // Check if speaker is muted (volume 1-5 is considered muted for fire show)
  const isMuted = (speaker: Speaker) => {
    const vol = speaker.volume ?? speakerVolumes[speaker.name] ?? 75;
    return vol <= 5;
  };

  const onlineCount = speakers.filter((s) => s.is_online).length;
  const allGrouped = speakers.every((s) => s.is_grouped);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <RefreshCw className="w-8 h-8 animate-spin text-orange-500" />
      </div>
    );
  }

  return (
    <div className="space-y-4 sm:space-y-6 pb-6">
      {/* Header */}
      <div className="flex items-start sm:items-center justify-between gap-2">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold">Speaker Control</h1>
          <p className="text-sm text-gray-400">
            {onlineCount}/{speakers.length} speakers online
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={fetchData} className="p-2">
            <RefreshCw className="w-4 h-4" />
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={handleGroupAll}
            disabled={actionLoading === 'group'}
          >
            <Link2 className="w-4 h-4 sm:mr-2" />
            <span className="hidden sm:inline">Group All</span>
          </Button>
        </div>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-3 gap-2 sm:gap-4">
        <Card>
          <CardContent className="py-3 sm:py-4">
            <div className="flex flex-col items-center sm:flex-row sm:justify-between">
              <div className="flex items-center gap-2 sm:gap-3">
                <Wifi className="w-6 h-6 sm:w-8 sm:h-8 text-green-500" />
                <div className="text-center sm:text-left">
                  <p className="text-xl sm:text-2xl font-bold">{onlineCount}</p>
                  <p className="text-xs sm:text-sm text-gray-400">Online</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="py-3 sm:py-4">
            <div className="flex flex-col items-center sm:flex-row sm:justify-between">
              <div className="flex items-center gap-2 sm:gap-3">
                <Link2 className="w-6 h-6 sm:w-8 sm:h-8 text-blue-500" />
                <div className="text-center sm:text-left">
                  <p className="text-xl sm:text-2xl font-bold">{allGrouped ? 'Yes' : 'No'}</p>
                  <p className="text-xs sm:text-sm text-gray-400">Grouped</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="py-3 sm:py-4">
            <div className="flex flex-col items-center sm:flex-row sm:justify-between">
              <div className="flex items-center gap-2 sm:gap-3">
                <SpeakerIcon className="w-6 h-6 sm:w-8 sm:h-8 text-orange-500" />
                <div className="text-center sm:text-left">
                  <p className="text-xl sm:text-2xl font-bold">{speakers.length}</p>
                  <p className="text-xs sm:text-sm text-gray-400">Total</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Master Volume */}
      <Card>
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Volume2 className="w-5 h-5 text-orange-500" />
              <h2 className="font-semibold text-sm sm:text-base">Master Volume</h2>
            </div>
            <span className="text-lg font-bold text-orange-500">{masterVolume}%</span>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3">
            <div className="flex-1">
              <Slider
                min={0}
                max={100}
                value={masterVolume}
                onChange={(e) => setMasterVolume(Number(e.target.value))}
              />
            </div>
            <Button
              onClick={handleSetMasterVolume}
              disabled={actionLoading === 'volume'}
              size="sm"
            >
              Set All
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Visual Layout */}
      {layout && (
        <Card>
          <CardHeader className="pb-2">
            <h2 className="font-semibold text-sm sm:text-base">Venue Layout</h2>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-2 sm:gap-4 max-w-2xl mx-auto">
              {layout.layout.flat().map((speakerName) => {
                const speaker = getSpeakerByName(speakerName);
                const volume = speaker?.volume ?? speakerVolumes[speakerName] ?? 75;
                const muted = speaker && isMuted(speaker);
                return (
                  <div
                    key={speakerName}
                    className={clsx(
                      'p-2 sm:p-4 rounded-lg border text-center transition-colors',
                      muted
                        ? 'bg-orange-950/50 border-orange-500'
                        : speaker?.is_online
                        ? 'bg-gray-800 border-green-600'
                        : 'bg-gray-900 border-gray-700 opacity-50'
                    )}
                  >
                    <div className="flex items-center justify-center mb-1 sm:mb-2">
                      {muted ? (
                        <Flame className="w-6 h-6 sm:w-8 sm:h-8 text-orange-500" />
                      ) : (
                        <SpeakerIcon
                          className={clsx(
                            'w-6 h-6 sm:w-8 sm:h-8',
                            speaker?.is_online ? 'text-green-500' : 'text-gray-600'
                          )}
                        />
                      )}
                    </div>
                    <p className="text-xs sm:text-sm font-medium truncate">
                      {speakerName.replace(/_/g, ' ')}
                    </p>
                    <p className={clsx(
                      'text-lg sm:text-xl font-bold',
                      muted ? 'text-orange-500' : 'text-white'
                    )}>
                      {volume}%
                    </p>
                    {muted && (
                      <Badge variant="warning" className="mt-1 text-xs">
                        Fire Muted
                      </Badge>
                    )}
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Individual Speaker Controls */}
      <Card>
        <CardHeader className="pb-2">
          <h2 className="font-semibold text-sm sm:text-base">Individual Controls</h2>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {speakers.map((speaker) => {
              const volume = speaker.volume ?? speakerVolumes[speaker.name] ?? 75;
              const muted = isMuted(speaker);
              return (
                <div
                  key={speaker.id}
                  className={clsx(
                    'flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 p-3 rounded-lg',
                    muted ? 'bg-orange-950/30 border border-orange-500/50' : 'bg-gray-800'
                  )}
                >
                  <div className="flex items-center gap-3 sm:w-48">
                    {muted ? (
                      <Flame className="w-5 h-5 text-orange-500" />
                    ) : (
                      <SpeakerIcon
                        className={clsx(
                          'w-5 h-5',
                          speaker.is_online ? 'text-green-500' : 'text-gray-600'
                        )}
                      />
                    )}
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-sm truncate">{speaker.name.replace(/_/g, ' ')}</p>
                      <div className="flex gap-1">
                        <Badge
                          variant={speaker.is_online ? 'success' : 'danger'}
                          className="text-xs"
                        >
                          {speaker.is_online ? 'Online' : 'Offline'}
                        </Badge>
                        {muted && (
                          <Badge variant="warning" className="text-xs">
                            Fire
                          </Badge>
                        )}
                      </div>
                    </div>
                    <span className={clsx(
                      'text-lg font-bold sm:hidden',
                      muted ? 'text-orange-500' : 'text-white'
                    )}>
                      {speakerVolumes[speaker.name] ?? volume}%
                    </span>
                  </div>
                  <div className="flex items-center gap-3 flex-1">
                    <div className="flex-1">
                      <Slider
                        min={0}
                        max={100}
                        value={speakerVolumes[speaker.name] ?? volume}
                        onChange={(e) => handleSpeakerVolumeChange(speaker.name, Number(e.target.value))}
                        disabled={!speaker.is_online}
                      />
                    </div>
                    <span className={clsx(
                      'w-12 text-right font-bold hidden sm:block',
                      muted ? 'text-orange-500' : 'text-white'
                    )}>
                      {speakerVolumes[speaker.name] ?? volume}%
                    </span>
                    <Button
                      variant={muted ? 'danger' : 'secondary'}
                      size="sm"
                      disabled={!speaker.is_online || actionLoading === speaker.name}
                      onClick={() => handleSetSpeakerVolume(speaker.name)}
                      className="min-w-[60px]"
                    >
                      {actionLoading === speaker.name ? '...' : 'Set'}
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
