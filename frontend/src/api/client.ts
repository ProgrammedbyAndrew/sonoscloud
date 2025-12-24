const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw new Error(error.detail || `HTTP error ${response.status}`);
    }

    return response.json();
  }

  // Schedule endpoints
  async getSchedule() {
    return this.request<Record<string, unknown>>('/api/v1/schedule');
  }

  async getDaySchedule(day: string) {
    return this.request<{ day: string; slots: unknown[] }>(`/api/v1/schedule/${day}`);
  }

  async addScheduleSlot(day: string, slot: unknown) {
    return this.request(`/api/v1/schedule/${day}`, {
      method: 'POST',
      body: JSON.stringify(slot),
    });
  }

  async updateScheduleSlot(day: string, slotId: number, slot: unknown) {
    return this.request(`/api/v1/schedule/${day}/${slotId}`, {
      method: 'PUT',
      body: JSON.stringify(slot),
    });
  }

  async deleteScheduleSlot(day: string, slotId: number) {
    return this.request(`/api/v1/schedule/${day}/${slotId}`, {
      method: 'DELETE',
    });
  }

  async resetSchedule() {
    return this.request('/api/v1/schedule/reset', { method: 'POST' });
  }

  // Playback endpoints
  async getPlaybackStatus() {
    return this.request<unknown>('/api/v1/playback/status');
  }

  async play(programName?: string, favoriteId?: string) {
    return this.request('/api/v1/playback/play', {
      method: 'POST',
      body: JSON.stringify({ program_name: programName, favorite_id: favoriteId }),
    });
  }

  async playFavorite(favoriteId: string, volume: number = 75) {
    return this.request('/api/v1/playback/play-favorite', {
      method: 'POST',
      body: JSON.stringify({ favorite_id: favoriteId, volume }),
    });
  }

  async pause() {
    return this.request('/api/v1/playback/pause', { method: 'POST' });
  }

  async setVolume(volume: number) {
    return this.request('/api/v1/playback/volume', {
      method: 'POST',
      body: JSON.stringify({ volume }),
    });
  }

  async runProgram(programName: string) {
    return this.request(`/api/v1/playback/run-program/${programName}`, {
      method: 'POST',
    });
  }

  // Speaker endpoints
  async getSpeakers() {
    return this.request<unknown[]>('/api/v1/speakers');
  }

  async getSpeakerLayout() {
    return this.request<unknown>('/api/v1/speakers/config/layout');
  }

  async groupAllSpeakers() {
    return this.request('/api/v1/speakers/group', { method: 'POST' });
  }

  async setSpeakerVolume(speakerName: string, volume: number) {
    return this.request(`/api/v1/speakers/${speakerName}/volume`, {
      method: 'PUT',
      body: JSON.stringify({ speaker_id: speakerName, volume }),
    });
  }

  async setAllSpeakersVolume(volume: number) {
    return this.request('/api/v1/speakers/volume/all', {
      method: 'POST',
      body: JSON.stringify({ volume }),
    });
  }

  // Favorites endpoints
  async getFavorites() {
    return this.request<{ favorites: unknown[] }>('/api/v1/favorites');
  }

  async getKnownFavorites() {
    return this.request<{ known_favorites: unknown[] }>('/api/v1/favorites/known');
  }

  // Programs endpoints
  async getPrograms() {
    return this.request<{ programs: unknown[]; available_scripts: unknown[] }>('/api/v1/programs');
  }

  async getProgramTypes() {
    return this.request<{ types: unknown[] }>('/api/v1/programs/types');
  }

  async getVolumePresets() {
    return this.request<{ presets: number[]; descriptions: Record<string, string> }>('/api/v1/programs/volumes');
  }

  // System endpoints
  async getSystemStatus() {
    return this.request<unknown>('/api/v1/system/status');
  }

  async getExecutionLogs(limit: number = 50) {
    return this.request<{ logs: unknown[] }>(`/api/v1/system/logs?limit=${limit}`);
  }

  async restartScheduler() {
    return this.request('/api/v1/system/restart-scheduler', { method: 'POST' });
  }

  async getCurrentTime() {
    return this.request<unknown>('/api/v1/system/time');
  }

  // Fire Show Mode endpoints
  async getFireShowMode() {
    return this.request<{
      enabled: boolean;
      next_reset: string | null;
      program: string;
      interval: string;
    }>('/api/v1/system/fire-show-mode');
  }

  async enableFireShowMode() {
    return this.request<{ status: string; message: string }>(
      '/api/v1/system/fire-show-mode/enable',
      { method: 'POST' }
    );
  }

  async disableFireShowMode() {
    return this.request<{ status: string; message: string }>(
      '/api/v1/system/fire-show-mode/disable',
      { method: 'POST' }
    );
  }

  async toggleFireShowMode() {
    return this.request<{ status: string; message: string }>(
      '/api/v1/system/fire-show-mode/toggle',
      { method: 'POST' }
    );
  }
}

export const api = new ApiClient(API_BASE_URL);
