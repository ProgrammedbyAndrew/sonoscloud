import { useEffect, useState } from 'react';
import { Speaker as SpeakerIcon, Volume2, RefreshCw, Link2, Wifi } from 'lucide-react';
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
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      const [speakersData, layoutData] = await Promise.all([
        api.getSpeakers(),
        api.getSpeakerLayout(),
      ]);
      setSpeakers(speakersData as Speaker[]);
      setLayout(layoutData as SpeakerLayout);
    } catch (error) {
      console.error('Error fetching speakers:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
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
    } catch (error) {
      console.error('Error setting volume:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const getSpeakerByName = (name: string) => {
    return speakers.find((s) => s.name === name);
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
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Speaker Control</h1>
          <p className="text-gray-400">
            {onlineCount}/{speakers.length} speakers online
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="ghost" size="sm" onClick={fetchData}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Refresh
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={handleGroupAll}
            disabled={actionLoading === 'group'}
          >
            <Link2 className="w-4 h-4 mr-2" />
            Group All
          </Button>
        </div>
      </div>

      {/* Status */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Wifi className="w-8 h-8 text-green-500" />
                <div>
                  <p className="text-2xl font-bold">{onlineCount}</p>
                  <p className="text-sm text-gray-400">Online</p>
                </div>
              </div>
              <Badge variant={onlineCount === speakers.length ? 'success' : 'warning'}>
                {onlineCount === speakers.length ? 'All Online' : 'Some Offline'}
              </Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Link2 className="w-8 h-8 text-blue-500" />
                <div>
                  <p className="text-2xl font-bold">{allGrouped ? 'Yes' : 'No'}</p>
                  <p className="text-sm text-gray-400">All Grouped</p>
                </div>
              </div>
              <Badge variant={allGrouped ? 'success' : 'info'}>
                {allGrouped ? 'Synchronized' : 'Individual'}
              </Badge>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <SpeakerIcon className="w-8 h-8 text-orange-500" />
                <div>
                  <p className="text-2xl font-bold">{speakers.length}</p>
                  <p className="text-sm text-gray-400">Total Speakers</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Master Volume */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Volume2 className="w-5 h-5 text-orange-500" />
            <h2 className="font-semibold">Master Volume</h2>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-4">
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
            >
              Set All to {masterVolume}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Visual Layout */}
      {layout && (
        <Card>
          <CardHeader>
            <h2 className="font-semibold">Venue Layout</h2>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto">
              {layout.layout.flat().map((speakerName) => {
                const speaker = getSpeakerByName(speakerName);
                return (
                  <div
                    key={speakerName}
                    className={clsx(
                      'p-4 rounded-lg border text-center transition-colors',
                      speaker?.is_online
                        ? 'bg-gray-800 border-green-600'
                        : 'bg-gray-900 border-gray-700 opacity-50'
                    )}
                  >
                    <div className="flex items-center justify-center mb-2">
                      <SpeakerIcon
                        className={clsx(
                          'w-8 h-8',
                          speaker?.is_online ? 'text-green-500' : 'text-gray-600'
                        )}
                      />
                    </div>
                    <p className="text-sm font-medium">{speakerName.replace(/_/g, ' ')}</p>
                    <div className="flex items-center justify-center gap-1 mt-1">
                      <span
                        className={clsx(
                          'w-2 h-2 rounded-full',
                          speaker?.is_online ? 'bg-green-500' : 'bg-gray-600'
                        )}
                      />
                      <span className="text-xs text-gray-400">
                        {speaker?.is_online ? 'Online' : 'Offline'}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Individual Speaker Controls */}
      <Card>
        <CardHeader>
          <h2 className="font-semibold">Individual Controls</h2>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {speakers.map((speaker) => (
              <div
                key={speaker.id}
                className="flex items-center gap-4 p-3 bg-gray-800 rounded-lg"
              >
                <div className="flex items-center gap-3 w-48">
                  <SpeakerIcon
                    className={clsx(
                      'w-5 h-5',
                      speaker.is_online ? 'text-green-500' : 'text-gray-600'
                    )}
                  />
                  <div>
                    <p className="font-medium">{speaker.name.replace(/_/g, ' ')}</p>
                    <div className="flex gap-2">
                      <Badge
                        variant={speaker.is_online ? 'success' : 'danger'}
                      >
                        {speaker.is_online ? 'Online' : 'Offline'}
                      </Badge>
                      {speaker.is_grouped && (
                        <Badge variant="info">Grouped</Badge>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex-1">
                  <Slider
                    min={0}
                    max={100}
                    defaultValue={75}
                    disabled={!speaker.is_online}
                    label=""
                    showValue={false}
                  />
                </div>
                <div className="w-24 text-right">
                  <Button
                    variant="secondary"
                    size="sm"
                    disabled={!speaker.is_online || actionLoading === speaker.name}
                  >
                    Set
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
