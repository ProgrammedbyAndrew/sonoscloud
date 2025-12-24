import { useEffect, useState } from 'react';
import { Calendar, Clock, Play, Trash2, RefreshCw, ChevronLeft, ChevronRight, Lock } from 'lucide-react';
import { Card, CardHeader, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import type { ScheduleSlot } from '../types';
import { clsx } from 'clsx';

const DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
const DAY_LABELS: Record<string, string> = {
  monday: 'Monday',
  tuesday: 'Tuesday',
  wednesday: 'Wednesday',
  thursday: 'Thursday',
  friday: 'Friday',
  saturday: 'Saturday',
  sunday: 'Sunday',
};

const BLOCK_COLORS: Record<string, string> = {
  AM: 'bg-blue-900/50 border-blue-700',
  DAY: 'bg-green-900/50 border-green-700',
  PM_FIRE: 'bg-orange-900/50 border-orange-700',
};

const BLOCK_LABELS: Record<string, string> = {
  AM: 'After Midnight',
  DAY: 'Day Program',
  PM_FIRE: 'Fire Show',
};

// Program type display names
const PROGRAM_TYPE_NAMES: Record<string, string> = {
  sm: 'Social Media',
  ad: 'Business Ad',
  fm: 'Flea Market',
  parking: 'Parking',
  adfire: 'Fire Ad',
  fireparking: 'Fire Parking',
  TIGS: 'Gift Shop',
  pause: 'Pause',
};

export function Schedule() {
  const { isLoggedIn } = useAuth();
  const [schedule, setSchedule] = useState<Record<string, ScheduleSlot[]>>({});
  const [selectedDay, setSelectedDay] = useState(() => {
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long' }).toLowerCase();
    return today;
  });
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<number | null>(null);

  const fetchSchedule = async () => {
    try {
      const data = await api.getSchedule();
      setSchedule(data as Record<string, ScheduleSlot[]>);
    } catch (error) {
      console.error('Error fetching schedule:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSchedule();
  }, []);

  const handleRunProgram = async (programName: string, slotId: number) => {
    setActionLoading(slotId);
    try {
      await api.runProgram(programName);
    } catch (error) {
      console.error('Error running program:', error);
    } finally {
      setActionLoading(null);
    }
  };

  const handleDeleteSlot = async (slotId: number) => {
    if (!confirm('Are you sure you want to delete this slot?')) return;

    try {
      await api.deleteScheduleSlot(selectedDay, slotId);
      await fetchSchedule();
    } catch (error) {
      console.error('Error deleting slot:', error);
    }
  };

  const navigateDay = (direction: 'prev' | 'next') => {
    const currentIndex = DAYS.indexOf(selectedDay);
    const newIndex = direction === 'prev'
      ? (currentIndex - 1 + DAYS.length) % DAYS.length
      : (currentIndex + 1) % DAYS.length;
    setSelectedDay(DAYS[newIndex]);
  };

  const daySlots = schedule[selectedDay] || [];

  // Group slots by block type
  const groupedSlots = daySlots.reduce((acc, slot) => {
    const block = slot.block_type;
    if (!acc[block]) acc[block] = [];
    acc[block].push(slot);
    return acc;
  }, {} as Record<string, ScheduleSlot[]>);

  const formatTime = (time: string) => {
    const [hours, minutes] = time.split(':').map(Number);
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const displayHours = hours % 12 || 12;
    return `${displayHours}:${minutes.toString().padStart(2, '0')} ${ampm}`;
  };

  const getProgramType = (name: string) => {
    const cleaned = name.replace('.py', '');
    const match = cleaned.match(/^\d+(.+)$/);
    const type = match ? match[1] : cleaned;
    return PROGRAM_TYPE_NAMES[type] || type;
  };

  const getVolume = (name: string) => {
    const match = name.match(/^(\d+)/);
    return match ? match[1] : '??';
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
          <h1 className="text-2xl font-bold">Schedule Manager</h1>
          <p className="text-gray-400">Manage weekly audio schedule</p>
        </div>
        <Button variant="ghost" size="sm" onClick={fetchSchedule}>
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </Button>
      </div>

      {/* Day Selector */}
      <Card>
        <CardContent className="py-3">
          <div className="flex items-center justify-between">
            <Button variant="ghost" size="sm" onClick={() => navigateDay('prev')}>
              <ChevronLeft className="w-5 h-5" />
            </Button>
            <div className="flex gap-2 overflow-x-auto">
              {DAYS.map((day) => (
                <button
                  key={day}
                  onClick={() => setSelectedDay(day)}
                  className={clsx(
                    'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
                    selectedDay === day
                      ? 'bg-orange-500 text-white'
                      : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                  )}
                >
                  {DAY_LABELS[day]}
                </button>
              ))}
            </div>
            <Button variant="ghost" size="sm" onClick={() => navigateDay('next')}>
              <ChevronRight className="w-5 h-5" />
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Schedule Blocks */}
      <div className="space-y-4">
        {['AM', 'DAY', 'PM_FIRE'].map((blockType) => {
          const slots = groupedSlots[blockType] || [];
          if (slots.length === 0) return null;

          return (
            <Card key={blockType} className={clsx('border-l-4', BLOCK_COLORS[blockType])}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Calendar className="w-5 h-5 text-orange-500" />
                    <h2 className="font-semibold">{BLOCK_LABELS[blockType]}</h2>
                    <Badge variant="info">{slots.length} slots</Badge>
                  </div>
                  <span className="text-sm text-gray-400">
                    {slots[0] && formatTime(slots[0].time)} - {slots[slots.length - 1] && formatTime(slots[slots.length - 1].time)}
                  </span>
                </div>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-2">
                  {slots.map((slot) => (
                    <div
                      key={slot.id}
                      className="flex items-center justify-between p-3 bg-gray-800 rounded-lg hover:bg-gray-750 group"
                    >
                      <div className="flex items-center gap-3">
                        <Clock className="w-4 h-4 text-gray-500" />
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="font-medium">{formatTime(slot.time)}</span>
                            <Badge variant="default">{getVolume(slot.program_name)}</Badge>
                          </div>
                          <span className="text-sm text-gray-400">
                            {getProgramType(slot.program_name)}
                          </span>
                        </div>
                      </div>
                      <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleRunProgram(slot.program_name, slot.id)}
                          disabled={actionLoading === slot.id || !isLoggedIn}
                          className="p-1"
                          title={!isLoggedIn ? 'Login required' : undefined}
                        >
                          {!isLoggedIn ? <Lock className="w-4 h-4" /> : <Play className="w-4 h-4" />}
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDeleteSlot(slot.id)}
                          disabled={!isLoggedIn}
                          className="p-1 text-red-400 hover:text-red-300"
                          title={!isLoggedIn ? 'Login required' : undefined}
                        >
                          {!isLoggedIn ? <Lock className="w-4 h-4" /> : <Trash2 className="w-4 h-4" />}
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Summary */}
      <Card>
        <CardContent>
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-400">
              Total slots for {DAY_LABELS[selectedDay]}: {daySlots.length}
            </span>
            <div className="flex gap-4">
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 rounded bg-blue-700" />
                AM: {groupedSlots['AM']?.length || 0}
              </span>
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 rounded bg-green-700" />
                DAY: {groupedSlots['DAY']?.length || 0}
              </span>
              <span className="flex items-center gap-2">
                <span className="w-3 h-3 rounded bg-orange-700" />
                PM_FIRE: {groupedSlots['PM_FIRE']?.length || 0}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
