import { useEffect, useState } from 'react';
import { Play, Pause, Volume2, RefreshCw, Clock, Speaker, Music, Flame, Power, Activity, CheckCircle, XCircle } from 'lucide-react';
import { Card, CardHeader, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Slider } from '../components/ui/Slider';
import { api } from '../api/client';
import type { SystemStatus, PlaybackStatus } from '../types';
import { clsx } from 'clsx';

interface LogEntry {
  id: number;
  program_name: string;
  executed_at: string;
  status: 'success' | 'error';
  error_message: string | null;
}

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

function formatTimeAgo(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

export function Dashboard() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [playbackStatus, setPlaybackStatus] = useState<PlaybackStatus | null>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [volume, setVolume] = useState(75);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [fireShowMode, setFireShowMode] = useState(false);

  const fetchStatus = async () => {
    try {
      const [system, playback, logsData] = await Promise.all([
        api.getSystemStatus(),
        api.getPlaybackStatus(),
        api.getLogs(15),
      ]);
      setSystemStatus(system as SystemStatus);
      setPlaybackStatus(playback as PlaybackStatus);
      setLogs((logsData as { logs: LogEntry[] }).logs || []);

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
    <div className="space-y-4 pb-6">
      {/* Header - Mobile optimized */}
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0 flex-1">
          <h1 className="text-xl sm:text-2xl font-bold">Dashboard</h1>
          <p className="text-sm text-gray-400 truncate">
            {systemStatus?.current_time_display || 'Loading...'}
          </p>
        </div>
        <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
          <Badge
            variant={systemStatus?.status === 'healthy' ? 'success' : 'warning'}
            className="text-xs whitespace-nowrap"
          >
            {systemStatus?.status === 'healthy' ? 'Online' : 'Degraded'}
          </Badge>
          <Button variant="ghost" size="sm" onClick={fetchStatus} className="p-2">
            <RefreshCw className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Fire Show Mode Toggle - Mobile optimized */}
      <Card
        variant="elevated"
        className={clsx(
          'border-2 transition-all',
          fireShowMode
            ? 'border-orange-500 bg-gradient-to-r from-orange-950/50 to-red-950/50'
            : 'border-gray-700'
        )}
      >
        <CardContent className="py-3 sm:py-4">
          <div className="flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-4">
            <div className="flex items-center gap-3 flex-1 min-w-0">
              <div className={clsx(
                'p-2 sm:p-3 rounded-full flex-shrink-0',
                fireShowMode ? 'bg-orange-500 animate-pulse' : 'bg-gray-700'
              )}>
                <Flame className={clsx('w-6 h-6 sm:w-8 sm:h-8', fireShowMode ? 'text-white' : 'text-gray-400')} />
              </div>
              <div className="min-w-0 flex-1">
                <h2 className="text-lg sm:text-xl font-bold">Fire Show Mode</h2>
                <p className="text-xs sm:text-sm text-gray-400 line-clamp-2">
                  {fireShowMode
                    ? 'Fire Show Ad (85%) every hour'
                    : 'Plays 85adfire.py hourly'}
                </p>
              </div>
            </div>
            <Button
              variant={fireShowMode ? 'danger' : 'primary'}
              size="lg"
              onClick={handleToggleFireShowMode}
              disabled={actionLoading === 'fireshow'}
              className="w-full sm:w-auto sm:min-w-[120px]"
            >
              <Power className="w-5 h-5 mr-2" />
              {fireShowMode ? 'Turn OFF' : 'Turn ON'}
            </Button>
          </div>
          {fireShowMode && (
            <div className="mt-3 p-2 sm:p-3 bg-orange-900/30 rounded-lg">
              <p className="text-xs sm:text-sm text-orange-300">
                <strong>Active:</strong> Resets at midnight
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Now Playing - Mobile optimized */}
      <Card variant="elevated">
        <CardHeader className="pb-2">
          <div className="flex items-center gap-2">
            <Music className="w-5 h-5 text-orange-500" />
            <h2 className="font-semibold">Now Playing</h2>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex gap-3 sm:gap-4">
            {/* Album Art - Smaller on mobile */}
            {playbackStatus?.image_url ? (
              <img
                src={playbackStatus.image_url}
                alt="Album art"
                className="w-16 h-16 sm:w-20 sm:h-20 rounded-lg object-cover flex-shrink-0"
              />
            ) : (
              <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-lg bg-gray-800 flex items-center justify-center flex-shrink-0">
                <Music className="w-8 h-8 sm:w-10 sm:h-10 text-gray-600" />
              </div>
            )}

            {/* Track Info */}
            <div className="flex-1 min-w-0 space-y-1">
              <div className="flex items-center gap-2">
                {playbackStatus?.is_playing ? (
                  <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse flex-shrink-0" />
                ) : (
                  <span className="w-2 h-2 rounded-full bg-gray-500 flex-shrink-0" />
                )}
                <span className="text-xs text-gray-400 uppercase">
                  {playbackStatus?.is_playing ? 'Playing' : 'Paused'}
                </span>
              </div>

              {playbackStatus?.track_name ? (
                <>
                  <p className="text-sm sm:text-base font-semibold truncate">{playbackStatus.track_name}</p>
                  {playbackStatus.artist && (
                    <p className="text-xs sm:text-sm text-gray-400 truncate">{playbackStatus.artist}</p>
                  )}
                  {playbackStatus.station && (
                    <p className="text-xs text-orange-500 truncate">{playbackStatus.station}</p>
                  )}
                </>
              ) : (
                <p className="text-sm sm:text-base font-medium text-gray-400">
                  {systemStatus?.scheduler.current_program
                    ? getProgramDisplayName(systemStatus.scheduler.current_program)
                    : 'Idle'}
                </p>
              )}

              <div className="flex gap-2 pt-1">
                <Button
                  size="sm"
                  onClick={handlePlay}
                  disabled={actionLoading === 'play'}
                  className="flex-1 sm:flex-none"
                >
                  <Play className="w-4 h-4 sm:mr-1" />
                  <span className="hidden sm:inline">Play</span>
                </Button>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={handlePause}
                  disabled={actionLoading === 'pause'}
                  className="flex-1 sm:flex-none"
                >
                  <Pause className="w-4 h-4 sm:mr-1" />
                  <span className="hidden sm:inline">Pause</span>
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Status Cards - Stack on mobile */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
        {/* Next Up */}
        <Card variant="elevated">
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <Clock className="w-5 h-5 text-orange-500" />
              <h2 className="font-semibold text-sm sm:text-base">Next Up</h2>
            </div>
          </CardHeader>
          <CardContent>
            {systemStatus?.scheduler.next_job ? (
              <div className="space-y-1">
                <p className="text-sm sm:text-base font-medium truncate">
                  {systemStatus.scheduler.next_job.display_name ||
                   getProgramDisplayName(systemStatus.scheduler.next_job.program)}
                </p>
                <p className="text-xs sm:text-sm text-gray-400">
                  {systemStatus.scheduler.next_job.day} @ {systemStatus.scheduler.next_job.time}
                </p>
              </div>
            ) : (
              <p className="text-sm text-gray-400">No upcoming programs</p>
            )}
          </CardContent>
        </Card>

        {/* Scheduler Status */}
        <Card variant="elevated">
          <CardHeader className="pb-2">
            <div className="flex items-center gap-2">
              <Speaker className="w-5 h-5 text-orange-500" />
              <h2 className="font-semibold text-sm sm:text-base">System</h2>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs sm:text-sm text-gray-400">Scheduler</span>
                <Badge variant={systemStatus?.scheduler.is_running ? 'success' : 'danger'} className="text-xs">
                  {systemStatus?.scheduler.is_running ? 'Running' : 'Stopped'}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs sm:text-sm text-gray-400">Sonos</span>
                <Badge variant={systemStatus?.sonos_connected ? 'success' : 'danger'} className="text-xs">
                  {systemStatus?.sonos_connected ? 'Connected' : 'Offline'}
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-xs sm:text-sm text-gray-400">Jobs</span>
                <span className="text-xs sm:text-sm font-medium">{systemStatus?.scheduler.job_count || 0}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Volume Control - Full width on mobile */}
        <Card className="sm:col-span-2 lg:col-span-1">
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Volume2 className="w-5 h-5 text-orange-500" />
                <h2 className="font-semibold text-sm sm:text-base">Volume</h2>
              </div>
              <span className="text-lg font-bold text-orange-500">{volume}%</span>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-3">
              <div className="flex-1">
                <Slider
                  min={0}
                  max={100}
                  value={volume}
                  onChange={(e) => handleVolumeChange(Number(e.target.value))}
                  onMouseUp={handleVolumeCommit}
                  onTouchEnd={handleVolumeCommit}
                  className="h-3"
                />
              </div>
              <Button
                variant="primary"
                size="sm"
                onClick={handleVolumeCommit}
                disabled={actionLoading === 'volume'}
                className="px-4"
              >
                Set
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions - 2x2 on mobile, 4 across on desktop */}
      <Card>
        <CardHeader className="pb-2">
          <h2 className="font-semibold text-sm sm:text-base">Quick Actions</h2>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 sm:gap-3">
            <Button
              variant="secondary"
              onClick={() => api.runProgram('75fm.py')}
              className="flex flex-col items-center py-3 sm:py-4 h-auto"
            >
              <Music className="w-5 h-5 sm:w-6 sm:h-6 mb-1 sm:mb-2" />
              <span className="text-xs sm:text-sm">Music 75%</span>
            </Button>
            <Button
              variant="secondary"
              onClick={() => api.runProgram('85ad.py')}
              className="flex flex-col items-center py-3 sm:py-4 h-auto"
            >
              <Volume2 className="w-5 h-5 sm:w-6 sm:h-6 mb-1 sm:mb-2" />
              <span className="text-xs sm:text-sm">Ad 85%</span>
            </Button>
            <Button
              variant="secondary"
              onClick={() => api.runProgram('75parking.py')}
              className="flex flex-col items-center py-3 sm:py-4 h-auto"
            >
              <Speaker className="w-5 h-5 sm:w-6 sm:h-6 mb-1 sm:mb-2" />
              <span className="text-xs sm:text-sm">Parking 75%</span>
            </Button>
            <Button
              variant="danger"
              onClick={handlePause}
              className="flex flex-col items-center py-3 sm:py-4 h-auto"
            >
              <Pause className="w-5 h-5 sm:w-6 sm:h-6 mb-1 sm:mb-2" />
              <span className="text-xs sm:text-sm">Pause All</span>
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Activity Log */}
      <Card>
        <CardHeader className="pb-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-orange-500" />
              <h2 className="font-semibold text-sm sm:text-base">Activity Log</h2>
            </div>
            <span className="text-xs text-gray-500">Last 15 events</span>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-1 max-h-64 overflow-y-auto">
            {logs.length === 0 ? (
              <p className="text-sm text-gray-500 text-center py-4">No activity yet</p>
            ) : (
              logs.map((log) => (
                <div
                  key={log.id}
                  className={clsx(
                    'flex items-center gap-2 px-2 py-1.5 rounded-lg text-sm',
                    log.status === 'success'
                      ? 'bg-green-500/10 border-l-2 border-green-500'
                      : 'bg-red-500/10 border-l-2 border-red-500'
                  )}
                >
                  {log.status === 'success' ? (
                    <CheckCircle className="w-4 h-4 text-green-500 flex-shrink-0" />
                  ) : (
                    <XCircle className="w-4 h-4 text-red-500 flex-shrink-0" />
                  )}
                  <span className="flex-1 truncate font-medium">
                    {getProgramDisplayName(log.program_name)}
                  </span>
                  <span className="text-xs text-gray-500 flex-shrink-0">
                    {formatTimeAgo(log.executed_at)}
                  </span>
                </div>
              ))
            )}
          </div>
          {logs.some(log => log.status === 'error') && (
            <div className="mt-3 p-2 bg-red-500/10 rounded-lg">
              <p className="text-xs text-red-400">
                <strong>Recent errors detected.</strong> Check Sonos connection.
              </p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
