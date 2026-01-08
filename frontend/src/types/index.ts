// Schedule Types
export interface ScheduleSlot {
  id: number;
  day_of_week: string;
  time: string;
  program_name: string;
  block_type: 'AM' | 'DAY' | 'PM_FIRE';
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface DaySchedule {
  day: string;
  slots: ScheduleSlot[];
}

export interface WeeklySchedule {
  monday: ScheduleSlot[];
  tuesday: ScheduleSlot[];
  wednesday: ScheduleSlot[];
  thursday: ScheduleSlot[];
  friday: ScheduleSlot[];
  saturday: ScheduleSlot[];
  sunday: ScheduleSlot[];
}

// Program Types
export interface Program {
  name: string;
  volume: number;
  program_type: string;
  script_exists: boolean;
}

export interface ProgramType {
  type: string;
  name: string;
  description: string;
}

// Speaker Types
export interface Speaker {
  id: string;
  name: string;
  is_online: boolean;
  is_grouped: boolean;
  volume?: number;
}

export interface SpeakerLayout {
  layout: string[][];
  speakers: Record<string, string>;
}

// Playback Types
export interface PlaybackStatus {
  is_playing: boolean;
  current_program: string | null;
  current_volume: number | null;
  group_id: string | null;
  next_scheduled: string | null;
  next_scheduled_time: string | null;
  track_name: string | null;
  artist: string | null;
  album: string | null;
  image_url: string | null;
  station: string | null;
  is_paused_until_midnight: boolean;
  paused_until: string | null;
}

// System Types
export interface FireShowModeStatus {
  enabled: boolean;
  next_reset: string | null;
  program: string;
  interval: string;
}

export interface SystemStatus {
  status: 'healthy' | 'degraded';
  sonos_connected: boolean;
  scheduler: {
    is_running: boolean;
    current_program: string | null;
    current_program_display: string | null;
    job_count: number;
    next_job: {
      program: string;
      display_name: string;
      time: string;
      day: string;
      datetime: string;
    } | null;
    fire_show_mode: FireShowModeStatus;
  };
  timezone: string;
  current_time: string;
  current_time_display: string;
}

// Favorite Types
export interface Favorite {
  id: string;
  name: string;
  type?: string;
}

// Execution Log Types
export interface ExecutionLog {
  id: number;
  program_name: string;
  executed_at: string;
  status: 'success' | 'error';
  error_message?: string;
}
