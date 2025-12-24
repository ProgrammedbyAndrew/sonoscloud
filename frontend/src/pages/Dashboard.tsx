import { useEffect, useState } from 'react';
import { Play, Pause, Volume2, RefreshCw, Clock, Speaker, Music, Flame, Power } from 'lucide-react';
import { Card, CardHeader, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Slider } from '../components/ui/Slider';
import { api } from '../api/client';
import type { SystemStatus, PlaybackStatus } from '../types';
import { clsx } from 'clsx';

// Program type display names
const PROGRAM_TYPE_NAMES: Record<string, string> = {
  sm: 'Social Media Ad',
  ad: 'Business Ad',
  fm: 'Music',
  parking: 'Parking Announcement',
  adfire: 'Fire Show Ad',
  fireparking: 'Fire Show Parking',
  TIGS: 'Gift Shop Ad',
  pause: 'Pause',
};

function getProgramDisplayName(programName: string): string {
  if (!programName) return 'Idle';
  const cleaned = programName.replace('.py', '');
  const volumeMatch = cleaned.match(/^(\d+)/);
  const typeMatch = cleaned.match(/^\d+(.+)$/);

  const volume = volumeMatch ? volumeMatch[1] : '??';
  const type = typeMatch ? typeMatch[1] : cleaned;
  const typeName = PROGRAM_TYPE_NAMES[type] || type;

  return `${typeName} @ ${volume}%`;
}

export function Dashboard() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [playbackStatus, setPlaybackStatus] = useState<PlaybackStatus | null>(null);
  const [volume, setVolume] = useState(75);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [fireShowMode, setFireShowMode] = useState(false);

  const fetchStatus = async () => {
    try {
      const [system, playback] = await Promise.all([
        api.getSystemStatus(),
        api.getPlaybackStatus(),
      ]);
      setSystemStatus(system as SystemStatus);
      setPlaybackStatus(playback as PlaybackStatus);

      // Get fire show mode from system status
      const sysStatus = system as SystemStatus;
      if (sysStatus.scheduler?.fire_show_mode) {
        setFireShowMode(sysStatus.scheduler.fire_show_mode.enabled);
      }
    } catch (error) {
      console.error('Error fetching status:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handlePlay = async () => {
    setActionLoading('play');
    try {
      await api.play();
      await fetchStatus();
    } catch (error) {
      console.error('Error playing:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const handlePause = async () => {
    setActionLoading('pause');
    try {
      await api.pause();
      await fetchStatus();
    } catch (error) {
      console.error('Error pausing:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const handleVolumeChange = async (newVolume: number) => {
    setVolume(newVolume);
  };

  const handleVolumeCommit = async () => {
    setActionLoading('volume');
    try {
      await api.setVolume(volume);
    } catch (error) {
      console.error('Error setting volume:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const handleToggleFireShowMode = async () => {
    setActionLoading('fireshow');
    try {
      await api.toggleFireShowMode();
      await fetchStatus();
    } catch (error) {
      console.error('Error toggling fire show mode:', error);
    } finally {
      setActionLoading(null);
    }
  };

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
          <h1 className="text-2xl font-bold">Dashboard</h1>
          <p className="text-gray-400">
            {systemStatus?.current_time_display || 'Loading...'}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant={systemStatus?.status === 'healthy' ? 'success' : 'warning'}>
            {systemStatus?.status === 'healthy' ? 'System Online' : 'System Degraded'}
          </Badge>
          <Button variant="ghost" size="sm" onClick={fetchStatus}>
            <RefreshCw className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Fire Show Mode Toggle - Prominent Card */}
      <Card
        variant="elevated"
        className={clsx(
          'border-2 transition-all',
          fireShowMode
            ? 'border-orange-500 bg-gradient-to-r from-orange-950/50 to-red-950/50'
            : 'border-gray-700'
        )}
      >
        <CardContent className="py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={clsx(
                'p-3 rounded-full',
                fireShowMode ? 'bg-orange-500 animate-pulse' : 'bg-gray-700'
              )}>
                <Flame className={clsx('w-8 h-8', fireShowMode ? 'text-white' : 'text-gray-400')} />
              </div>
              <div>
                <h2 className="text-xl font-bold">Fire Show Mode</h2>
                <p className="text-sm text-gray-400">
                  {fireShowMode
                    ? 'Running Fire Show Ad (85%) every hour - Resets at midnight'
                    : 'Turn on for early fire show - Plays 85adfire.py hourly'}
                </p>
              </div>
            </div>
            <Button
              variant={fireShowMode ? 'danger' : 'primary'}
              size="lg"
              onClick={handleToggleFireShowMode}
              disabled={actionLoading === 'fireshow'}
              className="min-w-[140px]"
            >
              <Power className="w-5 h-5 mr-2" />
              {fireShowMode ? 'Turn OFF' : 'Turn ON'}
            </Button>
          </div>
          {fireShowMode && (
            <div className="mt-4 p-3 bg-orange-900/30 rounded-lg">
              <p className="text-sm text-orange-300">
                <strong>Active:</strong> Fire Show Ad @ 85% will play every hour.
                Mode will automatically reset to regular programming at midnight (12:00 AM).
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Now Playing */}
        <Card variant="elevated" className="md:col-span-2">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Music className="w-5 h-5 text-orange-500" />
              <h2 className="font-semibold">Now Playing</h2>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4">
              {/* Album Art */}
              {playbackStatus?.image_url ? (
                <img
                  src={playbackStatus.image_url}
                  alt="Album art"
                  className="w-24 h-24 rounded-lg object-cover"
                />
              ) : (
                <div className="w-24 h-24 rounded-lg bg-gray-800 flex items-center justify-center">
                  <Music className="w-10 h-10 text-gray-600" />
                </div>
              )}

              {/* Track Info */}
              <div className="flex-1 space-y-2">
                <div className="flex items-center gap-2">
                  {playbackStatus?.is_playing ? (
                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                  ) : (
                    <span className="w-2 h-2 rounded-full bg-gray-500" />
                  )}
                  <span className="text-xs text-gray-400 uppercase">
                    {playbackStatus?.is_playing ? 'Playing' : 'Paused'}
                  </span>
                </div>

                {playbackStatus?.track_name ? (
                  <>
                    <p className="text-lg font-semibold truncate">{playbackStatus.track_name}</p>
                    {playbackStatus.artist && (
                      <p className="text-sm text-gray-400 truncate">{playbackStatus.artist}</p>
                    )}
                    {playbackStatus.station && (
                      <p className="text-xs text-orange-500 truncate">{playbackStatus.station}</p>
                    )}
                  </>
                ) : (
                  <p className="text-lg font-medium text-gray-400">
                    {systemStatus?.scheduler.current_program
                      ? getProgramDisplayName(systemStatus.scheduler.current_program)
                      : 'Idle'}
                  </p>
                )}

                <div className="flex gap-2 pt-2">
                  <Button
                    size="sm"
                    onClick={handlePlay}
                    disabled={actionLoading === 'play'}
                  >
                    <Play className="w-4 h-4 mr-1" />
                    Play
                  </Button>
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={handlePause}
                    disabled={actionLoading === 'pause'}
                  >
                    <Pause className="w-4 h-4 mr-1" />
                    Pause
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Next Up */}
        <Card variant="elevated">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-orange-500" />
              <h2 className="font-semibold">Next Up</h2>
            </div>
          </CardHeader>
          <CardContent>
            {systemStatus?.scheduler.next_job ? (
              <div className="space-y-2">
                <p className="text-lg font-medium">
                  {systemStatus.scheduler.next_job.display_name ||
                   getProgramDisplayName(systemStatus.scheduler.next_job.program)}
                </p>
                <p className="text-sm text-gray-400">
                  {systemStatus.scheduler.next_job.day} at {systemStatus.scheduler.next_job.time}
                </p>
              </div>
            ) : (
              <p className="text-gray-400">No upcoming programs</p>
            )}
          </CardContent>
        </Card>

        {/* Scheduler Status */}
        <Card variant="elevated">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Speaker className="w-5 h-5 text-orange-500" />
              <h2 className="font-semibold">Scheduler</h2>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Status</span>
                <Badge variant={systemStatus?.scheduler.is_running ? 'success' : 'danger'}>
                  {systemStatus?.scheduler.is_running ? 'Running' : 'Stopped'}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Jobs Loaded</span>
                <span className="font-medium">{systemStatus?.scheduler.job_count || 0}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Sonos API</span>
                <Badge variant={systemStatus?.sonos_connected ? 'success' : 'danger'}>
                  {systemStatus?.sonos_connected ? 'Connected' : 'Disconnected'}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Volume Control */}
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
                value={volume}
                onChange={(e) => handleVolumeChange(Number(e.target.value))}
                onMouseUp={handleVolumeCommit}
                onTouchEnd={handleVolumeCommit}
              />
            </div>
            <Button
              variant="secondary"
              size="sm"
              onClick={handleVolumeCommit}
              disabled={actionLoading === 'volume'}
            >
              Set
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <h2 className="font-semibold">Quick Actions</h2>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <Button
              variant="secondary"
              onClick={() => api.runProgram('75fm.py')}
              className="flex flex-col items-center py-4"
            >
              <Music className="w-6 h-6 mb-2" />
              <span>Music @ 75%</span>
            </Button>
            <Button
              variant="secondary"
              onClick={() => api.runProgram('85ad.py')}
              className="flex flex-col items-center py-4"
            >
              <Volume2 className="w-6 h-6 mb-2" />
              <span>Business Ad @ 85%</span>
            </Button>
            <Button
              variant="secondary"
              onClick={() => api.runProgram('75parking.py')}
              className="flex flex-col items-center py-4"
            >
              <Speaker className="w-6 h-6 mb-2" />
              <span>Parking @ 75%</span>
            </Button>
            <Button
              variant="danger"
              onClick={handlePause}
              className="flex flex-col items-center py-4"
            >
              <Pause className="w-6 h-6 mb-2" />
              <span>Pause All</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
