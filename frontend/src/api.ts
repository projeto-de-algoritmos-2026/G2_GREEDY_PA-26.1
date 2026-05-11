const BASE = '/api';

export type Priority = 'tranquila' | 'normal' | 'importante';

export type Task = {
  id: string;
  name: string;
  duration: number;
  deadline: string;
  priority: Priority;
};

export type ScheduledTask = Task & {
  position: number;
  suggestedStart: Date;
  suggestedEnd: Date;
};

type BackendTask = {
  id: string;
  title: string;
  task_type: 'duration' | 'fixed';
  duration_minutes: number;
  deadline: string | null;
  priority: number;
  created_at: string;
};

type BackendScheduleItem = {
  task_id: string;
  title: string;
  start: string;
  end: string;
  lateness_minutes: number | null;
};

type BackendScheduleResponse = {
  algorithm: string;
  max_lateness_minutes: number;
  scheduled_tasks: BackendScheduleItem[];
};

function priorityFromInt(p: number): Priority {
  if (p >= 5) return 'importante';
  if (p >= 3) return 'normal';
  return 'tranquila';
}

function priorityToInt(p: Priority): number {
  if (p === 'importante') return 5;
  if (p === 'normal') return 3;
  return 1;
}

function mapBackendTask(t: BackendTask): Task {
  return {
    id: t.id,
    name: t.title,
    duration: t.duration_minutes,
    deadline: t.deadline ? t.deadline.slice(0, 16) : '',
    priority: priorityFromInt(t.priority),
  };
}

export async function fetchTasks(): Promise<Task[]> {
  const res = await fetch(`${BASE}/tasks`);
  if (!res.ok) throw new Error('Failed to fetch tasks');
  const data: BackendTask[] = await res.json();
  return data.map(mapBackendTask);
}

export async function createTask(task: Omit<Task, 'id'>): Promise<Task> {
  const res = await fetch(`${BASE}/tasks/duration`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: task.name,
      duration_minutes: task.duration,
      deadline: task.deadline || null,
      priority: priorityToInt(task.priority),
    }),
  });
  if (!res.ok) throw new Error('Failed to create task');
  const data: BackendTask = await res.json();
  return mapBackendTask(data);
}

export async function updateTask(id: string, task: Omit<Task, 'id'>): Promise<Task> {
  const res = await fetch(`${BASE}/tasks/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: task.name,
      duration_minutes: task.duration,
      deadline: task.deadline || null,
      priority: priorityToInt(task.priority),
    }),
  });
  if (!res.ok) throw new Error('Failed to update task');
  const data: BackendTask = await res.json();
  return mapBackendTask(data);
}

export async function deleteTask(id: string): Promise<void> {
  const res = await fetch(`${BASE}/tasks/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to delete task');
}

export async function fetchWorkweekSchedule(tasks: Task[]): Promise<ScheduledTask[]> {
  if (tasks.length === 0) return [];

  const now = new Date();
  const roundedMinutes = Math.ceil(now.getMinutes() / 15) * 15;
  now.setMinutes(roundedMinutes, 0, 0);

  const res = await fetch(`${BASE}/schedule/workweek`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start_time: now.toISOString() }),
  });
  if (!res.ok) throw new Error('Failed to fetch schedule');

  const data: BackendScheduleResponse = await res.json();
  const taskMap = new Map(tasks.map((t) => [t.id, t]));

  return data.scheduled_tasks
    .filter((item) => taskMap.has(item.task_id))
    .map((item, index) => ({
      ...taskMap.get(item.task_id)!,
      position: index + 1,
      suggestedStart: new Date(item.start),
      suggestedEnd: new Date(item.end),
    }));
}
